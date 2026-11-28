"""Verificacion aislada de un diseno (lista de operaciones): malla normal (h = 4 mm, con campos, STEP e imagenes) y malla fina
(h = 3,5 mm, la de los hitos). Uso: python scripts/verificar_diseno.py ops.json carpeta_salida
Se usa para comprobar disenos que el optimizador acepto pero nunca verifico (p. ej. la iteracion 77)."""
import sys, os, json, time
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import operaciones as O
import geometry as G
from evaluate import evaluate

if __name__ == "__main__":
    ops = json.load(open(sys.argv[1], encoding="utf-8"))
    out = sys.argv[2]
    os.makedirs(out, exist_ok=True)
    force = float(json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))["carga_N"])
    t0 = time.time()
    print(f"[{time.strftime('%H:%M:%S')}] reconstruyendo la pieza desde el 0.stp ({len(ops)} operaciones)", flush=True)
    for k, o in enumerate(ops, 1):
        print(f"   {k:2d}. {O.describe(o)}", flush=True)
    s, holes = O.build(ops)
    print(f"[{time.strftime('%H:%M:%S')}] masa CAD = {s.Volume() * 7.85e-6:.4f} kg ({time.time() - t0:.0f} s)", flush=True)
    res = {}
    for name, h, hmin, img in (("completa", 4.0, None, True), ("verificacion", 3.5, 1.0, False)):
        wd = os.path.join(out, name)
        kw = dict(h=h, hmin=hmin) if hmin else {}
        print(f"\n[{time.strftime('%H:%M:%S')}] ===== malla {name} (h = {h} mm) =====", flush=True)
        m = evaluate({}, wd, force=force, geom=O.Pieza(s, holes, ops), images=img, **kw)
        if m.get("status") != "ok":
            print(f"FALLO en {name}: {m.get('error')}", flush=True); sys.exit(1)
        if name == "completa":
            G.export(s, os.path.join(wd, "geometria.step"))
        res[name] = {k: m[k] for k in ("mass_kg", "mass_cad_kg", "vm_metric", "vm_metric_xyz", "u_max", "n_nodes",
                                       "vm_ex_b3_p2", "vm_ex_b3_p0", "vm_max_raw")}
        print(f"[{time.strftime('%H:%M:%S')}] {name}: {m['mass_kg']:.4f} kg | {m['vm_metric']:.1f} MPa en "
              f"{[round(v, 1) for v in m['vm_metric_xyz']]} | {m['u_max']:.3f} mm | {m['n_nodes']} nodos", flush=True)
    f = res["verificacion"]
    ok = f["vm_metric"] <= 215.0 and f["u_max"] <= 0.25
    res["cumple_malla_fina"] = ok
    res["ops"] = ops
    json.dump(res, open(os.path.join(out, "verificacion_resultado.json"), "w"), indent=1)
    print(f"\nRESULTADO: malla fina {f['vm_metric']:.1f} MPa, {f['u_max']:.3f} mm -> {'CUMPLE' if ok else 'NO CUMPLE'} "
          f"(cociente fina/normal {f['vm_metric'] / res['completa']['vm_metric']:.3f}) | total {time.time() - t0:.0f} s", flush=True)
