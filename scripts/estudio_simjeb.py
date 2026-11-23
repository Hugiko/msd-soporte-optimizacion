"""ESTUDIO DE LAS SOLUCIONES PUBLICADAS (SimJEB) CON NUESTRAS CONDICIONES.

SimJEB (Whalen, Beyene, Mueller, 2021; Harvard Dataverse doi:10.7910/DVN/XFUWJG) recoge los 381 disenos del
GE Jet Engine Bracket Challenge en el MISMO sistema de coordenadas que nuestro 0.stp (que es su diseno n.o 0).
Aqui cada diseno se calcula con NUESTRO modelo (37 800 N en -X por RBE3 en el bulon, pernos empotrados, metrica de
tension fuera de la singularidad de los pernos) y se compara con NUESTRO limite (coef. de seguridad >= 1 -> 215 MPa;
desplazamiento <= 0,25 mm).

Para ir rapido:
  1. pasada rapida (malla gruesa, h = 6 mm): si incumple claramente (> 1,5 veces el limite) se descarta ahi;
  2. si es prometedor, calculo normal (h = 4 mm, la malla validada en la Fase 2).
Los disenos cuyos agujeros no son los del enunciado (bulon macizo, agujeros de perno de otro tamano) se registran
como incompatibles. Se guarda el campo de tensiones de cada diseno (datos_simjeb/estudio/<id>/campos.npz) para
extraer despues las reglas de diseno (scripts/reglas.py) sin repetir ningun calculo.

Se puede interrumpir: al relanzarlo continua por el siguiente diseno.
Uso: python scripts/estudio_simjeb.py [--max N]
"""
import os, sys, csv, json, time, datetime, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fem

ROOT = fem.ROOT
DATA = os.path.join(ROOT, "datos_simjeb")
STEP_DIR = os.path.join(DATA, "stp")
WORK = os.path.join(DATA, "estudio")                  # carpetas de calculo (no se suben: pesadas)
OUT = os.path.join(ROOT, "estudio")                   # resumen (SI se sube a GitHub)
RES = os.path.join(OUT, "estudio_simjeb.json")
LOG = os.path.join(OUT, "estudio_simjeb.log")
USER = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
FORCE = float(USER.get("carga_N", 37800.0))
SIG_LIM = float(USER.get("sigma_y_MPa", 215.0)) * float(USER.get("margen_optimizacion", 1.0))
U_LIM = float(USER.get("desplazamiento_max_mm", 0.25))


def log(msg):
    fem.log(msg, LOG)


def metadata():
    out = []
    for r in csv.DictReader(open(os.path.join(DATA, "metadata.tab"), encoding="utf-8", errors="ignore")):
        try:
            i = int(r["id"])
        except (ValueError, KeyError):
            continue
        if not os.path.exists(os.path.join(STEP_DIR, f"{i}.stp")):
            continue
        out.append(dict(id=i, vol=float(r["volume"]), cat=r.get("category", ""), autor=r.get("author", ""),
                        genus=float(r.get("genus") or 0), hor_simjeb=float(r.get("max_hor_stress") or 0)))
    out.sort(key=lambda d: (d["vol"], d["id"]))          # primero los mas ligeros (los mas interesantes)
    return out


class SimJEBGeom:
    """Adaptador para evaluate(): carga el STEP publicado tal cual (el solido mayor). Agujeros detectados en la malla."""
    NAMES = []

    def __init__(self, d):
        self.d = d

    def build(self, p=None):
        import cadquery as cq
        shp = cq.importers.importStep(os.path.join(STEP_DIR, f"{self.d['id']}.stp")).val()
        sols = sorted(shp.Solids(), key=lambda s: s.Volume(), reverse=True)
        if not sols:
            raise RuntimeError("el archivo no contiene un solido")
        s = sols[0]
        return s, dict(volume_mm3=s.Volume(), mass_kg=s.Volume() * 7.85e-6, hueco=False, clamped=[],
                       holes={"deteccion": "en la malla"}, pin_half_width=None, auto_interfaces=True,
                       simjeb_id=self.d["id"], simjeb_categoria=self.d["cat"], simjeb_autor=self.d["autor"],
                       n_shells=len(s.Shells()))

    @staticmethod
    def export(solid, path):
        import cadquery as cq
        cq.exporters.export(cq.Workplane().add(solid), path)


def load_results():
    return json.load(open(RES, encoding="utf-8")) if os.path.exists(RES) else {}


def save_results(res):
    os.makedirs(OUT, exist_ok=True)
    tmp = RES + ".tmp"
    json.dump(res, open(tmp, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    os.replace(tmp, RES)


def pending():
    """Disenos sin calcular o calculados con OTRA carga (se recalculan)."""
    res = load_results()
    def todo(r):
        return (r is None or r.get("fuerza_N") != FORCE
                or (r.get("veredicto") == "fallido" and not r.get("reintentado")))   # un fallo de malla se reintenta 1 vez
    return [d for d in metadata() if todo(res.get(str(d["id"])))]


def verdict(m):
    if m.get("status") != "ok":
        err = m.get("error") or ""
        if "InterfaceError" in err or "agujero" in err or "orejetas" in err:
            return "incompatible"
        return "fallido"
    ok = m["vm_metric"] <= SIG_LIM and (U_LIM <= 0 or m["u_max"] <= U_LIM)
    return "valido" if ok else "no_cumple"


CSV = os.path.join(OUT, "estudio_simjeb.csv")
SENT = os.path.join(OUT, "discord_enviados.json")
VTXT = {"valido": "CUMPLE", "no_cumple": "no cumple", "incompatible": "INCOMPATIBLE (agujeros distintos a los del enunciado)",
        "fallido": "FALLO (malla)"}
VCAT = {"valido": "valido", "no_cumple": "descartado", "incompatible": "filtrado", "fallido": "fallido"}


def write_csv(res=None):
    """Tabla legible (Excel) con todos los disenos calculados con la carga actual."""
    import csv as _csv
    res = res if res is not None else load_results()
    cols = ["id", "categoria", "autor", "veredicto", "fidelidad", "masa_kg", "tension_MPa", "cs", "desp_mm",
            "tension_simjeb_MPa", "genus", "error", "fecha"]
    rows = sorted((r for r in res.values() if r.get("fuerza_N") == FORCE), key=lambda r: (r.get("masa_kg") or 9e9, r["id"]))
    with open(CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = _csv.DictWriter(f, fieldnames=cols, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.4f}".replace(".", ",") if isinstance(v, float) else v) for k, v in r.items()})
    return CSV


def _sent():
    return set(json.load(open(SENT, encoding="utf-8"))) if os.path.exists(SENT) else set()


def _mark_sent(ids):
    s = _sent() | {str(i) for i in ids}
    json.dump(sorted(s, key=int), open(SENT, "w", encoding="utf-8"))


def _why(r):
    if r["veredicto"] == "valido":
        return f"cumple con nuestra carga: {r['tension_MPa']:.0f} MPa <= {SIG_LIM:.0f} MPa y {r['desp_mm']:.3f} mm <= {U_LIM} mm"
    if r["veredicto"] == "no_cumple":
        v = r["tension_MPa"] / SIG_LIM
        if str(r.get("fidelidad", "")).startswith("rapida (descartado"):
            return f"supera claramente el limite ({v:.1f} veces) ya en la pasada rapida (malla gruesa): no se calcula con malla fina"
        return f"supera el limite: {r['tension_MPa']:.0f} MPa ({v:.2f} veces {SIG_LIM:.0f} MPa)" + (
            f" o el desplazamiento ({r['desp_mm']:.3f} mm)" if r.get("desp_mm") and r["desp_mm"] > U_LIM else "")
    return (r.get("error") or "")[:300]


def notify_design(notify, r, k, total, wd):
    """Un mensaje por diseno publicado calculado (con la imagen de tensiones si se calculo con malla completa)."""
    img = None
    if r.get("tension_MPa") is not None and str(r.get("fidelidad", "")).startswith("normal"):
        try:
            import render
            d = np.load(os.path.join(wd, "campos.npz"))
            img = os.path.join(wd, "vonmises.png")
            render.results_png(d["nodes"], d["tris"], d["vm"], img,
                               f"SimJEB {r['id']}: {r['masa_kg']:.3f} kg, {r['tension_MPa']:.0f} MPa", marker=r.get("tension_xyz"))
        except Exception:
            img = None
    f = [dict(name="Resultado", value=VTXT[r["veredicto"]], inline=True),
         dict(name="Tipo / autor", value=f"{r['categoria']} / {r['autor']}"[:100], inline=True)]
    if r.get("tension_MPa") is not None:
        f += [dict(name="Masa (acero)", value=f"{r['masa_kg']:.3f} kg", inline=True),
              dict(name="Tension", value=f"{r['tension_MPa']:.0f} MPa (CS {215.0 / r['tension_MPa']:.2f})", inline=True),
              dict(name="Desplazamiento", value=f"{r['desp_mm']:.3f} mm", inline=True),
              dict(name="Calculo", value=str(r.get("fidelidad")), inline=True)]
    notify.design(f"Estudio SimJEB {k}/{total}: diseno publicado n.o {r['id']}", VCAT[r["veredicto"]], f,
                  f"Con NUESTRA carga ({FORCE:.0f} N) y NUESTRO limite ({SIG_LIM:.0f} MPa). Motivo: {_why(r)}", img)


def progress_text(res=None):
    res = {k: r for k, r in (res if res is not None else load_results()).items() if r.get("fuerza_N") == FORCE}
    c = {v: sum(1 for r in res.values() if r["veredicto"] == v) for v in VTXT}
    vals = sorted((r for r in res.values() if r["veredicto"] == "valido"), key=lambda r: r["masa_kg"])
    near = sorted((r for r in res.values() if r.get("tension_MPa") and str(r.get("fidelidad", "")).startswith("normal")),
                  key=lambda r: r["tension_MPa"] / SIG_LIM)[:5]
    t = (f"**{len(res)} de {len(metadata())} disenos calculados** con {FORCE:.0f} N: {c['valido']} cumplen, {c['no_cumple']} no cumplen, "
         f"{c['incompatible']} incompatibles, {c['fallido']} fallos de malla.")
    if vals:
        t += "\nMas ligeros que cumplen: " + ", ".join(f"n.o {r['id']} ({r['masa_kg']:.3f} kg, {r['tension_MPa']:.0f} MPa)" for r in vals[:5])
    if near:
        t += "\nMas cercanos a cumplir: " + ", ".join(f"n.o {r['id']} ({r['masa_kg']:.3f} kg, {r['tension_MPa']:.0f} MPa)" for r in near)
    return t


def backfill(notify, checkpoint=None):
    """Lo ya calculado que aun no se envio a Discord: un resumen con la tabla completa adjunta (CSV)."""
    res = load_results()
    sent = _sent()
    pend = [r for r in res.values() if r.get("fuerza_N") == FORCE and str(r["id"]) not in sent]
    if not pend:
        return
    write_csv(res)
    lines = [f"n.o {r['id']:>3}: {VTXT[r['veredicto']].split(' (')[0]}"
             + (f", {r['masa_kg']:.3f} kg, {r['tension_MPa']:.0f} MPa" if r.get("tension_MPa") else "")
             for r in sorted(pend, key=lambda r: (r.get("masa_kg") or 9e9))]
    txt = (progress_text(res) + f"\n\nDisenos ya calculados que aun no estaban en Discord ({len(pend)}); tabla completa en el CSV adjunto:\n"
           + "\n".join(lines))
    notify.file("Estudio de las soluciones publicadas: lo calculado hasta ahora", txt, CSV)
    _mark_sent(r["id"] for r in pend)
    if checkpoint:
        checkpoint(f"Estudio SimJEB: {len(res)} disenos calculados (guardado y enviado a Discord)")


def run(max_n=None, stop_flag=None, notify=None, checkpoint=None):
    """Calcula los disenos pendientes. Devuelve True si el estudio esta completo.
    notify: avisos a Discord (un mensaje por diseno + resumen cada 20); checkpoint(msg): guardar en GitHub."""
    from evaluate import evaluate
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    todo = pending()
    total = len(metadata())
    if notify:
        try:
            backfill(notify, checkpoint)
        except Exception as e:
            log(f"  (Discord, resumen de lo ya calculado: {e!r})")
    if not todo:
        return True
    log(f"ESTUDIO SimJEB: {total - len(todo)}/{total} disenos ya calculados con {FORCE:.0f} N; quedan {len(todo)}"
        f" (limite {SIG_LIM:.0f} MPa, {FORCE:.0f} N)")
    t_start = time.time(); done_now = 0
    for d in todo[: max_n or len(todo)]:
        if stop_flag and stop_flag():
            break
        res = load_results()
        k = total - len(todo) + done_now + 1
        print("\n" + "-" * 86)
        eta = ""
        if done_now:
            per = (time.time() - t_start) / done_now
            eta = f" | quedan ~{per * (len(todo) - done_now) / 3600:.1f} h"
        log(f"[estudio {k}/{total}] SimJEB n.o {d['id']} ({d['cat']}, {d['autor']}) | "
            f"{d['vol'] * 7.85e-6:.3f} kg de acero{eta}")
        wd = os.path.join(WORK, f"{d['id']:03d}")
        t0 = time.time()
        prev = res.get(str(d["id"]))
        retry = bool(prev and prev.get("fuerza_N") == FORCE and prev.get("veredicto") == "fallido")
        if retry:
            log("  reintento con todas las estrategias de malla (incluida la reparacion de la geometria)")
        try:
            m = evaluate({}, wd, force=FORCE, geom=SimJEBGeom(d), prescreen=1.5, log=LOG, images=False,
                         mesh_timeout=120, n_strategies=None if retry else 3)
        except Exception as e:
            m = dict(status="error", error=f"{type(e).__name__}: {e}")
        v = verdict(m)
        row = dict(id=d["id"], fuerza_N=FORCE, limite_MPa=SIG_LIM, categoria=d["cat"], autor=d["autor"], genus=d["genus"], veredicto=v,
                   fidelidad=m.get("fidelidad"), masa_kg=m.get("mass_kg"), tension_MPa=m.get("vm_metric"),
                   tension_xyz=m.get("vm_metric_xyz"), desp_mm=m.get("u_max"),
                   cs=(215.0 / m["vm_metric"]) if m.get("vm_metric") else None, nodos=m.get("n_nodes"),
                   tension_simjeb_MPa=d["hor_simjeb"], n_shells=m.get("n_shells"),
                   error=(m.get("error") or "")[:200] or None, tiempo_s=round(time.time() - t0, 1),
                   fecha=datetime.datetime.now().isoformat(timespec="seconds"))
        old = res.get(str(d["id"]))
        if old and old.get("fuerza_N") == FORCE and old.get("veredicto") == "fallido":
            row["reintentado"] = True
        res[str(d["id"])] = row
        save_results(res)
        for f in glob.glob(os.path.join(wd, "*")):        # solo se conservan los datos y el campo de tensiones
            if not f.endswith(("metrics.json", "campos.npz")):
                try:
                    os.remove(f)
                except OSError:
                    pass
        txt = {"valido": "CUMPLE", "no_cumple": "no cumple", "incompatible": "INCOMPATIBLE (agujeros distintos)",
               "fallido": "FALLO"}[v]
        if m.get("status") == "ok":
            log(f"  -> {txt}: {m['mass_kg']:.3f} kg | {m['vm_metric']:.0f} MPa | {m['u_max']:.3f} mm"
                f" | {m.get('fidelidad')} | {time.time() - t0:.0f} s")
        else:
            log(f"  -> {txt}: {(m.get('error') or '')[:120]} | {time.time() - t0:.0f} s")
        done_now += 1
        if notify:
            try:
                notify_design(notify, row, k, total, wd)
                _mark_sent([d["id"]])
            except Exception as e:
                log(f"  (Discord: {e!r})")
        if done_now % 20 == 0:          # resumen y guardado cada 20 disenos
            write_csv()
            if notify:
                notify.file(f"Estudio SimJEB: resumen ({k}/{total})", progress_text(), CSV)
            if checkpoint:
                checkpoint(f"Estudio SimJEB: {k}/{total} disenos calculados")
    write_csv()
    if notify and not pending():
        notify.file("Estudio SimJEB TERMINADO", progress_text() + "\nAhora se sacan las reglas de diseno (DESIGN_RULES.md).", CSV, "top")
    if checkpoint:
        checkpoint("Estudio SimJEB: " + ("terminado" if not pending() else "guardado parcial"))
    return not pending()


def summary():
    res = {k: r for k, r in load_results().items() if r.get("fuerza_N") == FORCE}
    vals = [r for r in res.values() if r["veredicto"] == "valido"]
    out = {k: sum(1 for r in res.values() if r["veredicto"] == k) for k in ("valido", "no_cumple", "incompatible", "fallido")}
    out["total"] = len(res)
    out["mas_ligeros_validos"] = sorted(((r["masa_kg"], r["id"]) for r in vals))[:10]
    return out


LOCK = os.path.join(OUT, "EN_EJECUCION.lock")


def lock_alive(path):
    """True si el fichero de bloqueo pertenece a un proceso python que sigue vivo."""
    import subprocess
    if not os.path.exists(path):
        return False
    try:
        pid = int(open(path).read().split()[0])
        r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}"], capture_output=True, text=True)
        return str(pid) in r.stdout and "python" in r.stdout.lower()
    except (ValueError, OSError, IndexError):
        return False


if __name__ == "__main__":
    n = None
    if "--max" in sys.argv:
        n = int(sys.argv[sys.argv.index("--max") + 1])
    os.makedirs(OUT, exist_ok=True)
    opt_lock = os.path.join(ROOT, "runs", f"opt_{int(round(FORCE))}N", "EN_EJECUCION.lock")
    if lock_alive(LOCK) or lock_alive(opt_lock):
        print("Ya hay un estudio u optimizador en marcha (la licencia de ANSYS solo admite una sesion). Se cierra.")
        time.sleep(8); sys.exit(2)
    open(LOCK, "w").write(f"{os.getpid()} {datetime.datetime.now().isoformat()}")
    print("=" * 86)
    print("  ESTUDIO DE LAS SOLUCIONES PUBLICADAS (SimJEB) CON NUESTRA CARGA Y NUESTRO LIMITE")
    print("  Se puede cerrar esta ventana: al relanzarlo continua por el siguiente diseno.")
    print("=" * 86)
    import discord_notify
    notify = discord_notify.make(ROOT, OUT, log)
    try:
        complete = run(n, notify=notify if notify.enabled else None)
        print(json.dumps(summary(), indent=1))
        print("ESTUDIO COMPLETO" if complete else "estudio parcial (quedan disenos)")
    finally:
        try:
            notify.flush(60)
        except Exception:
            pass
        try:
            os.remove(LOCK)
        except OSError:
            pass
