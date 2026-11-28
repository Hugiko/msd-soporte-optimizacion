"""Adopta como mejor diseno uno que el optimizador acepto pero perdio al deshacer una verificacion fallida posterior, una vez
comprobado con malla fina por scripts/verificar_diseno.py (que deja verificacion_resultado.json en la carpeta de salida).

Uso: python scripts/adoptar_verificado.py <carpeta_de_verificar_diseno> <iteracion>

Hace lo mismo que el optimizador con un hito: anota la calibracion fina/normal, pone el diseno como mejor, verificado y
actual, quita de los rechazos los cambios que ese diseno contiene (se habian anotado por la verificacion fallida de la
iteracion siguiente) y registra el hito (historial con STEP, operaciones y proyecto Workbench)."""
import sys, os, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import optimizer as OP
import discord_notify

if __name__ == "__main__":
    out, it = sys.argv[1], int(sys.argv[2])
    res = json.load(open(os.path.join(out, "verificacion_resultado.json"), encoding="utf-8"))
    if not res.get("cumple_malla_fina"):
        sys.exit("el diseno NO cumple con la malla fina: no se adopta")
    st = OP.load_state()
    ops = res["ops"]
    wd = os.path.join(out, "completa")
    m = json.load(open(os.path.join(wd, "metrics.json"), encoding="utf-8"))
    fv = res["verificacion"]
    st.setdefault("k_fino", []).append([round(fv["vm_metric"] / m["vm_metric"], 4), round(fv["u_max"] / m["u_max"], 4)])
    OP.K_FINO[:] = OP.k_fino(st)
    h = next((x for x in st["historia"] if x["iter"] == it), {})
    rec = dict(ops=ops, dir=wd, m=OP.summ(m), iter=it, galeria=h.get("galeria"),
               verif=dict(vm_metric=fv["vm_metric"], u_max=fv["u_max"], n_nodes=fv["n_nodes"], ok=True))
    prev = st["mejor"]
    if prev and rec["m"]["mass_kg"] >= prev["m"]["mass_kg"]:
        sys.exit(f"no mejora al mejor actual ({rec['m']['mass_kg']:.4f} frente a {prev['m']['mass_kg']:.4f} kg): no se adopta")
    n0 = len(st["rechazos"])
    st["rechazos"] = [r for r in st["rechazos"] if not (r.get("regla") == "verificacion" and r.get("op") in ops)]
    st["mejor"] = rec
    st["actual"] = dict(ops=ops, dir=wd, m=rec["m"], rapida=None, galeria=rec.get("galeria"))
    st["inversiones"] = 0; st["inversion_desde"] = None; st["sin_mejora"] = 0
    OP.DISCORD = discord_notify.make(ROOT, OP.TOP, OP.log)
    OP.REPO_URL = OP._repo_url()
    OP.log(f"RECUPERACION de la iteracion {it}: la aceptaron las reglas ({m['mass_kg']:.4f} kg, {m['vm_metric']:.1f} MPa) pero se perdio al "
           f"deshacer la verificacion fallida de la iteracion siguiente; comprobada aparte con malla fina: {fv['vm_metric']:.1f} MPa, "
           f"{fv['u_max']:.3f} mm -> CUMPLE. Pasa a ser el mejor diseno (antes {prev['m']['mass_kg']:.4f} kg, iteracion {prev['iter']}); "
           f"se quitan de los rechazos {n0 - len(st['rechazos'])} cambios que contiene.")
    OP.register_best(st, OP.GitSync(False))       # verificacion ya hecha -> hito: historial + STEP + proyecto Workbench
    OP.save_state(st)
    try:
        OP.write_dashboard(st, "DETENIDO (al relanzar optimizar.bat continua)")
    except Exception as e:
        OP.log(f"  (panel: {e!r})")
    OP.DISCORD.alert(f"Recuperada la iteracion {it}: {m['mass_kg']:.4f} kg | {m['vm_metric']:.1f} MPa (malla fina {fv['vm_metric']:.1f} MPa, "
                     f"CS {215 / fv['vm_metric']:.3f}). Nuevo mejor diseno verificado (antes {prev['m']['mass_kg']:.4f} kg).")
    OP.DISCORD.flush(120)
    print("adoptado")
