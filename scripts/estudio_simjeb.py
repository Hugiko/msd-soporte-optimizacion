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


def run(max_n=None, stop_flag=None):
    """Calcula los disenos pendientes. Devuelve True si el estudio esta completo."""
    from evaluate import evaluate
    os.makedirs(WORK, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    todo = pending()
    total = len(metadata())
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
        try:
            m = evaluate({}, wd, force=FORCE, geom=SimJEBGeom(d), prescreen=1.5, log=LOG, images=False,
                         mesh_timeout=120, n_strategies=3)
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
    try:
        complete = run(n)
        print(json.dumps(summary(), indent=1))
        print("ESTUDIO COMPLETO" if complete else "estudio parcial (quedan disenos)")
    finally:
        try:
            os.remove(LOCK)
        except OSError:
            pass
