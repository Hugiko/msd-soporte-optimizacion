"""Evaluacion completa de UN diseno: parametros -> geometria -> malla -> MAPDL -> metricas -> imagenes.

Nunca lanza excepciones hacia fuera: devuelve siempre un dict con 'status':
  ok | geom_fail | mesh_fail | solve_fail | post_fail
y deja en la carpeta del diseno: params.json, metrics.json, geometria.step/.png, vonmises.png, solve.out
"""
import os, sys, json, time, glob, traceback
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import geometry, fem, render
from run_mapdl import run

NODE_LIMIT = 125000          # licencia Student: 128 000 nodos (margen de seguridad)
MESH_H, MESH_HMIN = 4.0, 1.0  # malla de optimizacion (verificada en la Fase 2)
PRE_H, PRE_HMIN = 6.0, 1.5    # malla de la pasada rapida (cribado)
MESH_TIMEOUT_EXT = 180        # s por intento para disenos externos (SimJEB): geometrias mas complejas
MESH_TIMEOUT = 60             # s por intento: un mallado normal tarda < 25 s; si gmsh se cuelga se corta y se prueba otra estrategia


def _mesh_worker(q, step, hh, hmin, algo, heal, logfile):
    try:
        q.put(("ok", fem.mesh_step(step, hh, hmin=hmin, logfile=logfile, algo3d=algo, heal=heal)))
    except Exception as e:
        q.put(("err", f"{type(e).__name__}: {e}"))


def mesh_with_timeout(step, hh, hmin, algo, heal, logfile=None, timeout=MESH_TIMEOUT):
    """fem.mesh_step en un proceso aparte con tiempo maximo."""
    import multiprocessing as mp, queue
    ctx = mp.get_context("spawn")
    q = ctx.Queue()
    pr = ctx.Process(target=_mesh_worker, args=(q, step, hh, hmin, algo, heal, logfile), daemon=True)
    pr.start()
    t0 = time.time()
    while True:
        try:
            status, val = q.get(timeout=1.0)
            break
        except queue.Empty:
            if not pr.is_alive():                       # gmsh se cerro de golpe: no esperar al limite
                raise RuntimeError(f"el proceso de mallado se cerro inesperadamente (codigo {pr.exitcode})")
            if time.time() - t0 > timeout:
                pr.kill(); pr.join(5)
                raise RuntimeError(f"el mallado supero {timeout} s (gmsh colgado): se aborta")
    pr.join(10)
    if status != "ok":
        raise RuntimeError(val)
    return val


BIG_FILES = ("*.rst", "*.full", "*.esav", "*.emat", "*.osav", "*.page", "*.mntr", "*.ldhi", "*.r00x", "*.lock", "*.db", "*.dbb")


def evaluate(params, wd, force=None, geom=None, prescreen=None, h=MESH_H, hmin=MESH_HMIN, timeout=1200, log=None, images=True, keep_big=False):
    os.makedirs(wd, exist_ok=True)
    geom = geom or geometry
    if force is None:
        force = float(json.load(open(os.path.join(fem.ROOT, "config.json"), encoding="utf-8-sig"))["carga_N"])
    L = lambda m: fem.log(m, log)
    _cfg = json.load(open(os.path.join(fem.ROOT, "config.json"), encoding="utf-8-sig"))
    lim_s = float(_cfg.get("sigma_y_MPa", 215)) * float(_cfg.get("margen_optimizacion", 1.0))
    lim_u = float(_cfg.get("desplazamiento_max_mm", 0.25))
    t0 = time.time()
    res = dict(status="ok", params={k: float(params[k]) for k in geom.NAMES}, force=force)
    json.dump(res["params"], open(os.path.join(wd, "params.json"), "w"), indent=1)
    stage = "geometria"
    try:
        L("  [1/5] geometria parametrica (cadquery)")
        solid, ginfo = geom.build(params)
        step = os.path.join(wd, "geometria.step")
        geom.export(solid, step)
        res.update(mass_cad_kg=ginfo["mass_kg"], volume_cad_mm3=ginfo["volume_mm3"], hueco=ginfo["hueco"],
                   clamped=ginfo["clamped"], holes_check=ginfo["holes"])
        res.update({k: v for k, v in ginfo.items() if k.startswith("simjeb_") or k in ("aligeramientos", "sin_modificar")})
        L(f"        masa CAD = {ginfo['mass_kg']:.4f} kg | agujeros OK {ginfo['holes']} | hueco={ginfo['hueco']}"
          + (f" | ajustes: {ginfo['clamped']}" if ginfo["clamped"] else ""))
        if images:
            render.geometry_png(step, os.path.join(wd, "geometria.png"),
                                f"{os.path.basename(wd)}   masa {ginfo['mass_kg']:.3f} kg")

        def level(h0, hmin0, tag, quick=False):
            """Malla -> ANSYS -> resultados, con reintentos de malla. Devuelve todo lo necesario."""
            nonlocal stage
            strategies = [(10, h0, False), (1, h0, False), (10, h0 * 0.9, False), (4, h0, False), (10, h0, True), (1, h0 * 1.1, True)]
            if quick:                                   # pasada rapida: solo 2 intentos (es opcional)
                strategies = strategies[:2]
            attempt_log = []
            for k, (algo, hh, heal) in enumerate(strategies):
                stage = "malla"
                L(f"  [2/5] malla {tag} tet10 (gmsh, algoritmo {algo}, h={hh:.2f} mm)" + (f"  [reintento {k}]" if k else ""))
                try:
                    for _ in range(4):
                        nodes, tets, tris = mesh_with_timeout(step, hh, hmin0, algo, heal, logfile=log,
                                                              timeout=30 if quick else
                                                              (MESH_TIMEOUT_EXT if ginfo.get("auto_interfaces") else MESH_TIMEOUT))
                        if len(nodes) <= NODE_LIMIT:
                            break
                        L(f"        {len(nodes)} nodos > limite Student: engrosando malla")
                        hh *= 1.15
                    else:
                        raise RuntimeError("no se consigue una malla por debajo del limite de nodos")
                    if ginfo.get("auto_interfaces"):    # diseno externo: agujeros detectados en la malla
                        fem.IFACE = fem.detect_interfaces(nodes, tris)
                    info = fem.write_inp(os.path.join(wd, "model.inp"), nodes, tets, tris, force=force,
                                         pin_half=ginfo["pin_half_width"])
                except fem.InterfaceError:
                    raise                               # agujeros no reconocibles: el diseno no sirve tal cual
                except Exception as e:
                    attempt_log.append(f"malla alg{algo} h{hh:.2f}: {e}")
                    L(f"        fallo de malla: {e}")
                    continue
                stage = "solucion"
                L(f"  [3/5] ANSYS MAPDL {tag} ({info['n_nodes']} nodos, {info['n_elems']} elementos)")
                for f in glob.glob(os.path.join(wd, "res_*.txt")):
                    os.remove(f)
                r = run(wd, "model.inp", timeout=timeout, np_=4, job="file", logfile=log)
                waited = 0
                while r["status"] == "license":
                    # la licencia Student solo admite UNA sesion de ANSYS: esperar a que se libere (no es fallo del diseno)
                    if waited % 5 == 0:
                        L("  *** LICENCIA DE ANSYS OCUPADA: hay otra sesion abierta (Workbench / Mechanical / APDL).")
                        L("  *** Cierra esa ventana de ANSYS y el calculo continuara solo. Reintento cada minuto...")
                    time.sleep(60); waited += 1
                    r = run(wd, "model.inp", timeout=timeout, np_=4, job="file", logfile=log)
                if waited:
                    L(f"  licencia libre de nuevo tras ~{waited} min: calculo reanudado")
                if r["status"] == "ok" and os.path.exists(os.path.join(wd, "res_nod.txt")):
                    break
                err = open(os.path.join(wd, "file.err"), errors="ignore").read() if os.path.exists(os.path.join(wd, "file.err")) else ""
                reason = "elementos con forma no valida" if "shape error" in err else f"{r['status']} codigo {r['returncode']}"
                attempt_log.append(f"MAPDL alg{algo} h{hh:.2f}: {reason}")
                L(f"        ANSYS rechazo el calculo ({reason}): se vuelve a mallar")
                if r["status"] == "timeout":
                    raise RuntimeError("MAPDL: timeout")
            else:
                raise RuntimeError("todas las estrategias de malla/solucion fallaron: " + " | ".join(attempt_log))
            stage = "post"
            m, s, u = fem.read_results(wd, nodes, force=force, excl=(), pin_half=ginfo["pin_half_width"])
            if m["reaction_err_pct"] > 0.1:
                raise RuntimeError(f"equilibrio no satisfecho: error de reaccion {m['reaction_err_pct']:.3f} %")
            return dict(nodes=nodes, tris=tris, info=info, r=r, m=m, s=s, u=u, hh=hh, algo=algo, log=attempt_log)

        out = None
        if prescreen:
            # PASADA RAPIDA (malla gruesa): si el diseno ya incumple claramente, no se gasta la malla fina.
            # Es OPCIONAL: si su malla falla se pasa directamente a la malla normal.
            try:
                out = level(PRE_H, PRE_HMIN, "rapida", quick=True)
            except Exception as e:
                L(f"        pasada rapida no disponible ({str(e)[:80]}) -> malla normal")
                out = None
                prescreen = None
        if prescreen and out is not None:
            v = out["m"]["vm_metric"] / lim_s
            if lim_u > 0:
                v = max(v, out["m"]["u_max"] / lim_u)
            if v > prescreen:
                L(f"        pasada rapida: incumple claramente ({v:.1f} x el limite) -> se descarta sin malla fina")
                res["fidelidad"] = "rapida (descartado en la pasada rapida)"
            else:
                L(f"        pasada rapida: prometedor ({v:.2f} x el limite) -> calculo con la malla normal")
                out = None
        if out is None:
            out = level(h, hmin, "normal")
            res["fidelidad"] = "normal"
        nodes, tris, info, r, m, s, u = (out[k] for k in ("nodes", "tris", "info", "r", "m", "s", "u"))
        res.update(mesh_h=out["hh"], mesh_algo=out["algo"], mesh_retries=out["log"], solve_s=r["seconds"],
                   n_nodes=info["n_nodes"], n_elems=info["n_elems"],
                   nodes_per_bolt=info["nodes_per_bolt"], nodes_per_lug=info["nodes_per_lug"])
        L("  [4/5] resultados")
        res.update(m)
        res["mass_kg"] = m["mass_kg"]
        np.savez_compressed(os.path.join(wd, "campos.npz"), nodes=nodes, tris=tris, vm=s.astype(np.float32),
                            u=u.astype(np.float32))
        if images:
            L("  [5/5] imagenes")
            render.results_png(nodes, tris, s, os.path.join(wd, "vonmises.png"),
                               f"{os.path.basename(wd)}  masa {m['mass_kg']:.3f} kg  |  metrica {m['vm_metric']:.0f} MPa",
                               marker=m["vm_metric_xyz"])
            try:   # ficha 2x2 (geometria, von Mises, desplazamiento, datos); si falla no afecta al calculo
                cfg = json.load(open(os.path.join(fem.ROOT, "config.json"), encoding="utf-8-sig"))
                sy = float(cfg.get("sigma_y_MPa", 215)); lim = sy * float(cfg.get("margen_optimizacion", 1.0))
                ulim = float(cfg.get("desplazamiento_max_mm", 0.25))
                ok_s = m["vm_metric"] <= lim; ok_u = ulim <= 0 or m["u_max"] <= ulim
                ok_txt = "CUMPLE" if ok_s else "NO CUMPLE"
                lines = [f"Masa             {m['mass_kg']:.3f} kg   (original 2,411 kg)",
                         f"Tension (metrica) {m['vm_metric']:.1f} MPa  -> {ok_txt} (limite {lim:.0f})",
                         f"Coef. seguridad  {sy / m['vm_metric']:.2f}  (minimo exigido {sy / lim:.2f})",
                         f"Tension bruta    {m['vm_max_raw']:.0f} MPa (singular, borde perno)",
                         f"Desplaz. maximo  {m['u_max']:.4f} mm  -> " + ("CUMPLE" if ok_u else "NO CUMPLE") + (f" (limite {ulim:.2f})" if ulim > 0 else ""),
                         "VEREDICTO        " + ("VALIDO" if (ok_s and ok_u) else "NO VALIDO"),
                         f"   ux {m['ux_max']:.4f}  uy {m['uy_max']:.4f}  uz {m['uz_max']:.4f}",
                         f"Carga            {force:.0f} N en -X",
                         f"Malla            {res.get('n_nodes')} nodos (SOLID187)", "", "Parametros:"]
                if res.get("simjeb_id") is not None:
                    lines[-1:-1] = [f"Base             diseno SimJEB n.o {res['simjeb_id']} ({res.get('simjeb_autor', '')})"
                                    + ("  -> REFERENCIA sin modificar" if res.get("sin_modificar") else "  + modificaciones")]
                lines += [f"  {k:9s} = {v:g}" for k, v in res["params"].items()]
                render.panel4(wd, f"{os.path.basename(os.path.dirname(wd))} / diseno {os.path.basename(wd)}", lines)
            except Exception as e:
                L(f"        (ficha resumen no generada: {e})")
    except Exception as e:
        res["status"] = {"geometria": "geom_fail", "malla": "mesh_fail", "solucion": "solve_fail", "post": "post_fail"}[stage]
        res["error"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()[-2000:]
        L(f"  !! fallo en {stage}: {res['error']}")
    finally:
        if fem.IFACE is not None:
            res["interfaces"] = fem.IFACE
            fem.IFACE = None
        if not keep_big:
            for pat in BIG_FILES:
                for f in glob.glob(os.path.join(wd, pat)):
                    try:
                        os.remove(f)
                    except OSError:
                        pass
    res["total_s"] = time.time() - t0
    with open(os.path.join(wd, "metrics.json"), "w") as f:
        json.dump(res, f, indent=1)
    return res


if __name__ == "__main__":
    p = geometry.default_params()
    wd = sys.argv[1] if len(sys.argv) > 1 else os.path.join(fem.ROOT, "tests", "eval_defecto")
    for a in sys.argv[2:]:
        k, v = a.split("="); p[k] = float(v)
    r = evaluate(p, wd, log=os.path.join(wd, "progreso.log") if False else None)
    print(json.dumps({k: r.get(k) for k in ("status", "mass_kg", "mass_cad_kg", "vm_metric", "vm_max_raw", "u_max",
                                            "reaction_err_pct", "n_nodes", "total_s", "error")}, indent=1))
