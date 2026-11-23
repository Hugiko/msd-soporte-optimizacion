"""REGLAS DE DISENO: que modificar en la pieza, por que, y con que datos se respalda cada regla.

Cada regla tiene:
  - SI (condicion medida en el mapa de tensiones de la pieza actual),
  - HAGO (una operacion de scripts/operaciones.py: quitar o anadir material),
  - PORQUE (mecanica de solidos),
  - EVIDENCIA (estudio de las soluciones publicadas SimJEB con NUESTRA carga + nuestros calculos anteriores),
  - y su historial de aplicacion en el optimizador (aceptada / rechazada y cuanto cambiaron masa y tension).
Una regla que los datos CONTRADICEN se desactiva; una regla que se aplica 8 veces sin ninguna mejora se suspende.
El documento DESIGN_RULES.md se regenera desde aqui (python scripts/reglas.py).
"""
import os, sys, json, math, glob, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import fem
import geometry as G
import operaciones as O
import campo as CA

ROOT = fem.ROOT
EST = os.path.join(ROOT, "estudio")
RES = os.path.join(EST, "estudio_simjeb.json")
FEAT = os.path.join(EST, "caracteristicas.json")
EVID = os.path.join(EST, "evidencia.json")
WORK = os.path.join(ROOT, "datos_simjeb", "estudio")
DOC = os.path.join(ROOT, "DESIGN_RULES.md")
USER = json.load(open(os.path.join(ROOT, "config.json"), encoding="utf-8-sig"))
FORCE = float(USER.get("carga_N", 42258.0))
SIG_LIM = float(USER.get("sigma_y_MPa", 215.0)) * float(USER.get("margen_optimizacion", 1.0))
RHO = O.RHO_KG_MM3
TAUS = [float(t) for t in USER.get("umbrales_ocioso", [0.15, 0.25, 0.35])]
K_LOAD = FORCE / 37800.0          # los calculos antiguos (archivo) se hicieron con 37 800 N: el modelo es lineal

REGLAS = {
    "R1": dict(titulo="Aligeramiento pasante donde toda la columna de material esta ociosa", tipo="quitar",
               si="toda la columna vertical (radio del agujero + 3 mm de margen) trabaja por debajo del umbral de material ocioso",
               hago="agujero vertical pasante; paredes verticales (imprimible sin soportes); nunca en las zonas protegidas",
               porque="ese material no esta en el camino de la carga (bulon -> orejetas -> cuerpo -> pernos). Un agujero en una "
                      "zona a tension s multiplica la tension en su borde por Kt ~ 3 (placa con agujero circular, Kirsch): si todo "
                      "alrededor esta por debajo del umbral u, el borde queda por debajo de ~3u del limite y el pico no cambia.",
               espero="baja la masa; la tension maxima casi no cambia"),
    "R2": dict(titulo="Rebaje desde arriba de la capa ociosa", tipo="quitar",
               si="todo el material por encima de una cota zc, en un rectangulo (con 4 mm de margen), esta por debajo del umbral",
               hago=("rebaje desde arriba hasta zc (suelo horizontal: imprimible) con esquinas redondeadas de radio = 20 % de su lado "
                     "menor (3-8 mm); deja >= 5 mm de suelo y nunca una pared de menos de 5 mm al borde"),
               porque="material que no transmite carga: su tension es baja porque ni el momento de vuelco ni el cortante pasan "
                      "por ahi. Quitarlo desde arriba no deja voladizos y no corta el camino de carga.",
               espero="baja la masa; la tension maxima casi no cambia"),
    "R3": dict(titulo="Hueco interior en el nucleo ocioso (conservando las pieles)", tipo="quitar",
               si="un bloque interior, a >= 4 mm de cualquier superficie, trabaja por debajo del umbral",
               hago="hueco con techo a 45 grados y agujero de evacuacion D5 (impresion 3D)",
               porque="a flexion y torsion la tension crece con la distancia a la fibra neutra (s = M y / I, t = T r / J): el "
                      "nucleo apenas trabaja y la rigidez la dan las pieles. Por eso las vigas son en I o en cajon.",
               espero="baja la masa; la tension sube poco (las pieles siguen)"),
    "R4": dict(titulo="Collar de refuerzo en el perno donde esta el pico (y en su simetrico)", tipo="anadir",
               si="el pico de tension esta junto al alojamiento de la cabeza de un perno",
               hago="anillo de material alrededor del alojamiento (y del perno simetrico respecto al plano medio de las orejetas)",
               porque="la carga horizontal aplicada a 44,7 mm de altura crea un momento de vuelco (F x h ~ 1,9 kN m con 42 258 N) "
                      "que la pieza lleva a los pernos; alrededor del alojamiento la seccion es pequena. Mas seccion -> menos "
                      "tension (s ~ M / W). El soporte es simetrico respecto al plano medio de las orejetas (y ~ -75 mm): el "
                      "perno simetrico trabaja igual.",
               espero="baja la tension maxima; sube un poco la masa"),
    "R5": dict(titulo="Alojamiento de la cabeza mas ancho con acuerdo de fondo mayor", tipo="anadir",
               si="el pico esta en el acuerdo del fondo del alojamiento de un perno (entalla)",
               hago="alojamiento de radio mayor con acuerdo de fondo R - 8 mm",
               porque="hipotesis de partida: el factor de concentracion Kt baja al crecer el radio del acuerdo (Peterson). "
                      "PERO agrandar el alojamiento tambien quita seccion justo donde esta el pico.",
               espero="segun la teoria del acuerdo, baja la tension; segun la seccion, la sube: deciden los datos"),
    "R6": dict(titulo="Redondear las aristas entrantes junto al pico", tipo="anadir",
               si="el pico es una concentracion local (pico >= 1,8 veces la tension media a 12 mm) fuera de los alojamientos",
               hago="acuerdo (redondeo) de las aristas a menos de 6 mm del pico (nunca las de los 6 agujeros fijos)",
               porque="una arista viva entrante es una entalla: Kt crece al bajar el radio (Peterson). Un acuerdo reparte la "
                      "tension en mas material.",
               espero="baja la tension maxima con muy poca masa"),
    "R7": dict(titulo="Engrosar el anillo de las orejetas", tipo="anadir",
               si="el pico esta en las orejetas del bulon",
               hago="anillo de material alrededor del bulon en las dos orejetas (mismo espesor)",
               porque="el bulon empuja la orejeta en la direccion de la carga; el ligamento delante del agujero trabaja a "
                      "cortadura y aplastamiento (s ~ F / (2 t e)). Mas ligamento e -> menos tension.",
               espero="baja la tension en la orejeta; sube un poco la masa"),
    "R8": dict(titulo="Reponer material donde un corte anterior ha creado el pico", tipo="reponer",
               si="el pico esta a menos de 4 mm de un corte hecho antes",
               hago="se reduce ese corte (x0,6 de su tamano; si queda muy pequeno, se deshace)",
               porque="si el pico aparece en el borde de un corte, ese material SI estaba en el camino de carga: se devuelve "
                      "solo ese material en vez de reforzar en otro sitio.",
               espero="baja la tension maxima; sube un poco la masa"),
    "R9": dict(titulo="Cortar menos donde ya se rechazo un corte", tipo="meta",
               si="un corte se rechazo (tension por encima del limite o pieza peor)",
               hago="en esa zona solo se proponen cortes de como maximo 0,6 veces el tamano rechazado",
               porque="el rechazo dice que ahi hay material que trabaja; un corte menor puede ser aceptable (busqueda por "
                      "biseccion del tamano).",
               espero="evita repetir errores y aprovecha lo que si se pueda quitar"),
    "R10": dict(titulo="Subir el umbral de material ocioso cuando ya no queda donde quitar", tipo="meta",
                si="no hay ninguna zona por debajo del umbral actual donde quepa un corte",
                hago=f"se pasa al siguiente umbral ({', '.join(f'{t * 100:.0f} %' for t in TAUS)} del limite)",
                porque="se empieza por lo mas seguro (con Kt ~ 3, el borde de un corte en material al 15 % queda al ~45 %) y "
                       "solo despues se aprovecha material que trabaja algo mas.",
                espero="permite seguir aligerando con un riesgo controlado"),
    "R11": dict(titulo="Sustituir un bloque que trabaja poco por un nervio en la trayectoria de la carga (FORMA NUEVA)", tipo="sustituir",
                si=("un bloque trabaja por debajo del 45-60 % del limite (no es ocioso: lleva algo de carga) o un rebaje se rechazo "
                    "porque ese material si trabajaba"),
                hago=("se quita el bloque y se crean NERVIOS (paredes verticales, imprimibles, con acuerdo de 3 mm en la raiz): uno "
                      "por cada familia de la carga (traccion y compresion) en su direccion principal, dimensionado para llevarla al "
                      "50 % del limite"),
                porque=("Michell (1904): la estructura de volumen minimo que lleva una carga sigue las trayectorias de las tensiones "
                        "principales, y su volumen es la integral de |s| dV dividida por la tension de trabajo. En un bloque macizo "
                        "casi todo el material trabaja muy por debajo del limite; un nervio en la direccion de la carga lleva lo "
                        "mismo (traccion/compresion, que aprovecha toda la seccion) con mucho menos material."),
                espero="baja la masa (bloque menos nervio); la tension sube algo, pero el nervio trabaja por debajo del limite"),
}
TAU_NERVIO = (0.45, 0.6)        # bloques que trabajan "algo": candidatos a sustituirse por un nervio (R11)
SIG_TRABAJO = 0.5               # tension de trabajo de los nervios (fraccion del limite): margen para las uniones


def rib_for_block(C, reg, lim):
    """Nervios que sustituyen al material del bloque 'reg' (rectangulo x0..x1, y0..y1 por encima de zc).
    Michell: la estructura minima tiene DOS familias de barras, a traccion y a compresion. Para cada familia que lleve al
    menos el 25 % de la carga del bloque se crea un nervio en su direccion principal dominante (trayectoria de carga),
    dimensionado para que su volumen sea la integral de |s| dV de esa familia / (0,5 x limite).
    Devuelve (lista de operaciones nervio, datos) o (None, motivo)."""
    c = C.cen
    m = ((c[:, 0] > reg["x0"]) & (c[:, 0] < reg["x1"]) & (c[:, 1] > reg["y0"]) & (c[:, 1] < reg["y1"]) &
         (c[:, 2] > reg["zc"]) & ~C.prot)
    if m.sum() < 10:
        return None, "bloque demasiado pequeno"
    if C.pdir is None:
        return None, "sin direcciones principales (calculo antiguo)"
    k = np.abs(C.pval).argmax(axis=1)
    sdom = C.pval[np.arange(len(k)), k]                      # tension principal dominante con signo
    w_all = float((np.abs(sdom[m]) * C.vol[m]).sum())
    V_block = float(C.vol[m].sum())
    ribs, fams = [], []
    for fam, mf in (("traccion", m & (sdom > 0)), ("compresion", m & (sdom < 0))):
        Sf = float((np.abs(sdom[mf]) * C.vol[mf]).sum())
        if mf.sum() < 6 or Sf < 0.25 * w_all:
            continue
        d, coh, cg, _ = C.load_path(mf)
        hp = float(np.hypot(d[0], d[1]))
        if hp < 0.35:
            continue                                          # esa familia trabaja casi en vertical
        dp = np.array([d[0], d[1]]) / hp
        ts = []
        for i, (lo, hi) in enumerate(((reg["x0"], reg["x1"]), (reg["y0"], reg["y1"]))):
            if abs(dp[i]) > 1e-9:
                ts += [(lo - cg[i]) / dp[i], (hi - cg[i]) / dp[i]]
        ts = sorted(ts)
        L_in = ts[2] - ts[1]
        if L_in < 10.0:
            continue
        P0 = cg[:2] + dp * (ts[1] - 8.0); P1 = cg[:2] + dp * (ts[2] + 8.0)   # 8 mm de anclaje en el material que queda

        def top_at(P):
            near = np.hypot(c[:, 0] - P[0], c[:, 1] - P[1]) < 6.0
            return float(c[near, 2].max() + 1.5) if near.any() else float(c[mf, 2].max())
        zt0, zt1 = top_at(P0), top_at(P1)
        h_eff = max((zt0 + zt1) / 2 - reg["zc"], 3.0)
        A = Sf / (L_in * SIG_TRABAJO * lim)
        t = A / h_eff
        if t > 14.0:
            return None, f"la familia a {fam} lleva demasiada carga para un nervio ({t:.0f} mm de espesor necesario)"
        t = float(max(t, 4.0))
        ribs.append(dict(tipo="nervio", x0=round(float(P0[0]), 2), y0=round(float(P0[1]), 2), x1=round(float(P1[0]), 2),
                         y1=round(float(P1[1]), 2), zt0=round(zt0, 2), zt1=round(zt1, 2), t=round(t, 2), zb=0.0))
        fams.append(dict(fam=fam, dir=d, coh=coh, S=Sf, share=Sf / w_all, A=A, t=t, h=h_eff, L=L_in, V=t * h_eff * L_in,
                         ang=float(np.degrees(np.arctan2(dp[1], dp[0])))))
    if not ribs:
        return None, "ninguna familia de la carga cruza el bloque en horizontal"
    V_rib = sum(f["V"] for f in fams)
    if V_rib > 0.6 * V_block:
        return None, "los nervios necesarios serian casi tan grandes como el bloque"
    return ribs, dict(fams=fams, V_block=V_block, V_rib=V_rib, util_max=float(C.smax[m].max() / lim), S=w_all)


# =============================================================================================== evidencia
def _spearman(a, b):
    from scipy.stats import spearmanr
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 6:
        return None, None
    r = spearmanr(a[ok], b[ok])
    return float(r.statistic), float(r.pvalue)


def study_rows():
    if not os.path.exists(RES):
        return {}
    return {k: r for k, r in json.load(open(RES, encoding="utf-8")).items() if r.get("fuerza_N") == FORCE}


def features(log=print):
    """Caracteristicas (zonas, material ocioso, pico, ligamentos) de cada diseno publicado calculado. Se guardan."""
    rows = study_rows()
    cache = json.load(open(FEAT, encoding="utf-8")) if os.path.exists(FEAT) else {}
    n_new = 0
    for k, r in rows.items():
        key = f"{k}|{r.get('fuerza_N')}|{r.get('fecha')}"
        if (cache.get(k, {}).get("_clave") == key and "ocioso_rel" in cache[k]) or r.get("tension_MPa") is None:
            continue
        wd = os.path.join(WORK, f"{int(k):03d}")
        try:
            m = json.load(open(os.path.join(wd, "metrics.json"), encoding="utf-8"))
            C = CA.from_npz(os.path.join(wd, "campos.npz"), SIG_LIM, m)
            f = C.features(TAUS[0]); f["_clave"] = key
            cache[k] = f; n_new += 1
        except Exception as e:
            cache[k] = dict(_clave=key, error=str(e)[:120])
    if n_new:
        os.makedirs(EST, exist_ok=True)
        json.dump(cache, open(FEAT, "w", encoding="utf-8"), indent=0)
        log(f"  caracteristicas de {n_new} disenos publicados calculadas")
    return rows, cache


ARCH_CSV = os.path.join(EST, "calculos_anteriores.csv")


def archive_runs():
    """Calculos anteriores (familias vaciado/refuerzo, 37 800 N): params + metricas.
    Se leen de estudio/calculos_anteriores.csv (en GitHub); si no existe, se crea desde runs/archivo/ (solo en el PC)."""
    import csv
    out = []
    if os.path.exists(ARCH_CSV):
        for r in csv.DictReader(open(ARCH_CSV, encoding="utf-8")):
            p = {k[2:]: float(v) for k, v in r.items() if k.startswith("p_") and v not in ("", None)}
            out.append((r["familia"], p, dict(vm_metric=float(r["tension_MPa"]), mass_kg=float(r["masa_kg"]),
                                             u_max=float(r["desp_mm"]) if r.get("desp_mm") else None)))
        return out
    rows = []
    for d in sorted(glob.glob(os.path.join(ROOT, "runs", "archivo", "*familias*", "*", "[0-9][0-9][0-9]"))):
        fam = os.path.basename(os.path.dirname(d))
        if fam not in ("refuerzo", "vaciado"):
            continue
        try:
            m = json.load(open(os.path.join(d, "metrics.json"), encoding="utf-8"))
            p = json.load(open(os.path.join(d, "params.json"), encoding="utf-8"))
        except Exception:
            continue
        if m.get("status") == "ok" and m.get("vm_metric"):
            out.append((fam, p, m))
            rows.append(dict(familia=fam, diseno=os.path.basename(d), carga_N=37800, masa_kg=m["mass_kg"],
                             tension_MPa=m["vm_metric"], desp_mm=m.get("u_max"), **{f"p_{k}": v for k, v in p.items()}))
    if rows:
        os.makedirs(EST, exist_ok=True)
        cols = list(dict.fromkeys(k for r in rows for k in r))
        with open(ARCH_CSV, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    return out


def evidence(log=print):
    """Evalua cada regla con los datos. Devuelve {regla: {respaldo: True/False/None, texto, tabla(md)}} y lo guarda."""
    rows, feat = features(log)
    ok = {k: r for k, r in rows.items() if k != "0" and r.get("veredicto") == "valido" and "error" not in feat.get(k, {"error": 1})
          and str(r.get("fidelidad", "")).startswith("normal")}             # el n.o 0 es el propio original
    valid = sorted(ok, key=lambda k: rows[k]["masa_kg"])
    # grupo de referencia: los validos; si cumplen menos de 5 (se disenaron para titanio, sy ~ 900 MPa), los
    # calculados con malla completa mas cercanos a cumplir (se dice explicitamente en el documento)
    if len(valid) >= 5:
        G, glabel = valid, f"los {len(valid)} disenos publicados VALIDOS"
    else:
        near = sorted((k for k, r in rows.items() if k != "0" and str(r.get("fidelidad", "")).startswith("normal")
                       and r.get("tension_MPa") and "error" not in feat.get(k, {"error": 1})),
                      key=lambda k: rows[k]["tension_MPa"])[:15]
        G = sorted(set(near) | set(valid), key=lambda k: rows[k]["masa_kg"])
        glabel = (f"los {len(G)} disenos publicados mas cercanos a cumplir (solo {len(valid)} cumplen con acero S235 y "
                  f"{FORCE:.0f} N: se disenaron para titanio)")
    light = G[: max(1, len(G) // 2)]
    allf = {k: feat[k] for k in rows if k in feat and "error" not in feat[k]}
    orig = feat.get("0") if "error" not in feat.get("0", {"error": 1}) else None
    med = lambda keys, f: float(np.median([feat[k][f] for k in keys if feat[k].get(f) is not None])) if keys else None
    E = {}
    n_tot = len(rows)
    cnt = {v: sum(1 for r in rows.values() if r["veredicto"] == v) for v in ("valido", "no_cumple", "incompatible", "fallido")}
    E["_resumen"] = dict(n=n_tot, **cnt, n_validos_con_campo=len(valid), referencia=glabel, carga=FORCE, limite=SIG_LIM,
                         fecha=datetime.datetime.now().isoformat(timespec="minutes"))
    pct = lambda x: "-" if x is None else f"{100 * x:.0f} %"

    # --- R1-R3: material ocioso (respecto al pico de cada diseno: mide la eficiencia, cumpla o no)
    if len(G) >= 3 and orig:
        o_or, o_v, o_l = orig["ocioso_rel"], med(G, "ocioso_rel"), med(light, "ocioso_rel")
        rho, p = _spearman([rows[k]["masa_kg"] for k in G], [feat[k]["ocioso_rel"] for k in G])
        tab = [f"Referencia: {glabel}.", "",
               "| | material ocioso (< " + f"{TAUS[0] * 100:.0f} % de su propio pico) | masa |", "|---|---|---|",
               f"| pieza original (SimJEB n.o 0) | {pct(o_or)} | {rows['0']['masa_kg']:.3f} kg |",
               f"| mediana del grupo de referencia ({len(G)}) | {pct(o_v)} | {med(G, 'volumen_cm3') * 7.85e-3:.3f} kg |",
               f"| mediana de su mitad mas ligera ({len(light)}) | {pct(o_l)} | {med(light, 'volumen_cm3') * 7.85e-3:.3f} kg |"]
        zt = ["", "Donde esta el material (cm3) - original frente a la mitad mas ligera del grupo de referencia:", "",
              "| zona | original | referencia ligera (mediana) | exceso del original |", "|---|---|---|---|"]
        exc = {}
        for z in CA.ZONAS:
            a, b = orig[f"V_{z}_cm3"], med(light, f"V_{z}_cm3")
            exc[z] = a - b
            zt.append(f"| {CA.ZONA_TXT[z]} | {a:.0f} | {b:.0f} | {a - b:+.0f} |")
        # comparacion INDIRECTA (disenos distintos): puede respaldar la regla o no ser concluyente, pero no la
        # desactiva; la prueba directa es su aplicacion en el optimizador (se suspende si falla 8 veces)
        sup = True if (o_l is not None and o_l < o_or - 0.03) else None
        txt = ("" if sup else "NO CONCLUYENTE: ") + (f"en {glabel}, la mitad mas ligera tiene un {pct(o_l)} de material ocioso (por debajo del {TAUS[0] * 100:.0f} % de su "
               f"pico) frente al {pct(o_or)} del original" + (f"; en ese grupo, a mas material ocioso "
               f"{'mas' if rho > 0 else 'menos'} masa (Spearman {rho:+.2f})" if rho is not None else ""))
        base = dict(respaldo=sup, texto=txt, tabla=tab + zt, exceso_zonas=exc)
        E["R1"] = dict(base); E["R2"] = dict(base); E["R3"] = dict(base)
        rg, pg = _spearman([rows[k]["masa_kg"] for k in G], [rows[k]["genus"] for k in G])
        if rg is not None:
            E["R1"]["texto"] += (f". Agujeros pasantes: en ese grupo, a mas agujeros pasantes (genus de la malla) "
                                 f"{'menos' if rg < 0 else 'mas'} masa (Spearman {rg:+.2f}, p = {pg:.2g})")
        nsh = sum(1 for k in G if (rows[k].get("n_shells") or 1) > 1)
        E["R3"]["texto"] += (f". Huecos interiores cerrados en ese grupo: {nsh} de {len(G)} "
                             "(en el concurso no se podian dejar cavidades cerradas; aqui se dejan con evacuacion)")
    else:
        for r in ("R1", "R2", "R3"):
            E[r] = dict(respaldo=None, texto="estudio de SimJEB aun incompleto: regla basada en la mecanica (Kirsch, flexion)",
                        tabla=[])

    # --- R4 / R5: nuestros calculos anteriores (familias refuerzo / vaciado, escalados linealmente a la carga actual)
    arch = archive_runs()
    ref = [(p, m) for f, p, m in arch if f == "refuerzo"]
    rc, pc = _spearman([p["t_col_del"] for p, m in ref], [m["vm_metric"] for p, m in ref]) if ref else (None, None)
    r4_txt = (f"prueba directa en ANSYS sobre el original (bitacora 22/11): collares de 6 mm -> pico de {212.9 * K_LOAD:.0f} "
              f"a {181.2 * K_LOAD:.0f} MPa (-15 %) con +159 g (escalado lineal a {FORCE:.0f} N)")
    if rc is not None:
        r4_txt += f"; en {len(ref)} disenos de la familia refuerzo, mas collar delantero -> menos tension (Spearman {rc:+.2f}, p = {pc:.2g})"
    if len(G) >= 3 and orig:
        a, b = orig["V_pernos_del_cm3"], med(G, "V_pernos_del_cm3")
        npk = sum(1 for k in allf if allf[k].get("zona_pico", "").startswith("pernos"))
        r4_txt += (f"; material junto a los pernos delanteros: original {a:.0f} cm3, mediana del grupo de referencia {b:.0f} cm3; "
                   f"en {npk} de {len(allf)} disenos publicados calculados el pico esta junto a un perno")
    E["R4"] = dict(respaldo=True, texto=r4_txt, tabla=[])        # la prueba directa en ANSYS la respalda
    allr = [(p, m) for f, p, m in arch if "R_pocket" in p]
    rp, pp = _spearman([p["R_pocket"] for p, m in allr], [m["vm_metric"] for p, m in allr]) if allr else (None, None)
    big = [m["vm_metric"] * K_LOAD for p, m in allr if p["R_pocket"] > 11.0]
    small = [m["vm_metric"] * K_LOAD for p, m in allr if p["R_pocket"] < 10.6]
    E["R5"] = dict(respaldo=(None if rp is None else bool(rp < 0)),
                   texto=(f"en {len(allr)} disenos anteriores, alojamiento mas ancho -> MAS tension (Spearman {rp:+.2f}, p = {pp:.2g}; "
                          f"mediana {np.median(big):.0f} MPa con R > 11 mm frente a {np.median(small):.0f} MPa con el del original): "
                          "pesa mas la seccion que se pierde que el acuerdo que se gana. Regla DESACTIVADA por los datos."
                          if rp is not None and rp >= 0 else
                          (f"en {len(allr)} disenos anteriores, alojamiento mas ancho -> menos tension (Spearman {rp:+.2f})" if rp is not None
                           else "sin datos")), tabla=[])
    E["R6"] = dict(respaldo=None, texto="no se puede medir en las mallas publicadas (radios de acuerdo); regla basada en la teoria "
                                        "(Peterson) y en los resultados del propio optimizador", tabla=[])
    if len(G) >= 3 and orig:
        lo, lv = orig["ligamento_delante_mm"], med(G, "ligamento_delante_mm")
        lug_peak = [k for k in allf if allf[k].get("zona_pico") == "orejetas"]
        lp = med(lug_peak, "ligamento_delante_mm") if lug_peak else None
        E["R7"] = dict(respaldo=(True if ((lv is not None and lv >= lo * 0.9) or (lp is not None and lp < lv)) else None),
                       texto=(f"ligamento delante del bulon: original {lo:.1f} mm, mediana de {glabel}: {lv:.1f} mm"
                              + (f", y {lp:.1f} mm en los {len(lug_peak)} disenos cuyo pico esta en la orejeta" if lp else "")), tabla=[])
    else:
        E["R7"] = dict(respaldo=None, texto="estudio aun incompleto: regla basada en la mecanica (aplastamiento/cortadura)", tabla=[])
    for r in ("R8", "R9", "R10"):
        E[r] = dict(respaldo=None, texto="regla de procedimiento: se juzga por sus resultados en el optimizador", tabla=[])
    full = [k for k in allf if k != "0" and str(rows[k].get("fidelidad", "")).startswith("normal")]
    ribs = [k for k in full if rows[k].get("categoria") in ("beam", "arch", "butterfly")]
    blocks = [k for k in full if rows[k].get("categoria") == "block"]
    if len(ribs) >= 3 and len(blocks) >= 3:
        orb, obl = med(ribs, "ocioso_rel"), med(blocks, "ocioso_rel")
        mrb, mbl = float(np.median([rows[k]["masa_kg"] for k in ribs])), float(np.median([rows[k]["masa_kg"] for k in blocks]))
        E["R11"] = dict(respaldo=(True if orb < obl - 0.03 else None),
                        texto=(("" if orb < obl - 0.03 else "NO CONCLUYENTE: ") +
                               f"entre los disenos publicados calculados con malla completa, los de nervios / arcos / vigas ({len(ribs)}) "
                               f"tienen de mediana un {pct(orb)} de material ocioso y {mrb:.3f} kg, frente al {pct(obl)} y {mbl:.3f} kg "
                               f"de los tipo bloque ({len(blocks)}). Teoria: Michell (1904), estructuras de volumen minimo"), tabla=[])
    else:
        E["R11"] = dict(respaldo=None, texto=("teoria de Michell (1904): el volumen minimo para llevar una carga sigue las trayectorias "
                                              "principales; comparacion con SimJEB cuando el estudio tenga disenos de nervios y de bloque "
                                              "calculados con malla completa"), tabla=[])
    # disenos publicados validos (tabla general)
    E["_validos"] = [dict(id=int(k), masa=rows[k]["masa_kg"], tension=rows[k]["tension_MPa"], desp=rows[k]["desp_mm"],
                          categoria=rows[k]["categoria"], autor=rows[k]["autor"], ocioso=feat[k].get("ocioso"),
                          zona_pico=feat[k].get("zona_pico")) for k in valid]
    os.makedirs(EST, exist_ok=True)
    json.dump(E, open(EVID, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return E


def load_evidence():
    return json.load(open(EVID, encoding="utf-8")) if os.path.exists(EVID) else {}


def activa(rid, E, stats):
    """(activa, motivo)."""
    if E.get(rid, {}).get("respaldo") is False:
        return False, "desactivada: los datos la contradicen"
    s = stats.get(rid, {})
    if s.get("intentos", 0) >= 8 and s.get("aceptadas", 0) == 0:
        return False, f"suspendida: {s['intentos']} intentos sin ninguna mejora"
    return True, ""


# =============================================================================================== propuestas
def symmetric_bolt(k):
    ym = float(O.PIN_P[1]); x, y = G.BOLTS[k]["c"]
    return int(np.argmin([abs(b["c"][0] - x) + abs(b["c"][1] - (2 * ym - y)) if j != k else 1e9 for j, b in enumerate(G.BOLTS)]))


def corner_r(reg):
    """Radio de las esquinas de un vaciado: 20 % de su lado menor (entre 3 y 8 mm). La carga que rodea el vaciado se
    concentra en sus esquinas y el factor de concentracion baja al crecer r respecto al tamano del vaciado (Peterson)."""
    return round(float(np.clip(0.2 * min(reg["x1"] - reg["x0"], reg["y1"] - reg["y0"]), 3.0, 8.0)), 1)


def _overlap_rect(a, b):
    ix = max(0.0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])); iy = max(0.0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    return ix * iy / max((a["x1"] - a["x0"]) * (a["y1"] - a["y0"]), 1e-9)


def make_veto(rechazos):
    def veto(op):
        for rj in rechazos:
            o = rj["op"]
            if o["tipo"] != op["tipo"]:
                continue
            if all(o.get(k) == v for k, v in op.items()):
                return True                     # exactamente la misma modificacion ya se probo y no sirvio
            f = 0.6 if rj["motivo_tipo"] == "tension" else 0.9
            if op["tipo"] == "agujero":
                close = math.hypot(op["x"] - o["x"], op["y"] - o["y"]) < op["r"] + o["r"]
            else:
                close = O.overlap(op, o) > 0.3 or O.overlap(o, op) > 0.3
            if close and O.size(op) > f * O.size(o):
                return True
        return False
    return veto


def _expect(rid, stats, default):
    d = stats.get(rid, {}).get("dsig", [])
    if len(d) >= 2:
        return float(np.median(d)), f"mediana de las {len(d)} veces que se ha aplicado: {np.median(d):+.1f} %"
    return default, None


def shrink(op, f=0.6):
    """Version de una operacion de quitar con ~f veces su tamano (None si queda demasiado pequena)."""
    op = dict(op)
    if op["tipo"] == "agujero":
        op["r"] = round(op["r"] * f, 2)
        return op if op["r"] >= 3.0 else None
    s = math.sqrt(f)
    for a, b in (("x0", "x1"), ("y0", "y1")):
        c, h = (op[a] + op[b]) / 2, (op[b] - op[a]) / 2 * s
        op[a], op[b] = round(c - h, 2), round(c + h, 2)
    return op if min(op["x1"] - op["x0"], op["y1"] - op["y0"]) >= 8.0 else None


def propose(C, m, ops, st, E, stats, n_max=3):
    """Lista de modificaciones candidatas, cada una con su regla, su porque (con datos) y lo esperado.
    Candidato: dict(regla, titulo, ops_nuevas (lista completa de operaciones de la pieza), op (la nueva), porque, espero)."""
    lim = C.lim; sig = m["vm_metric"]; ratio = sig / lim
    pk = C.peak_info()
    zona = CA.ZONA_TXT.get(pk["zona"], pk["zona"])
    veto = make_veto(st.get("rechazos", []))
    reinf, rem = [], []
    notes = []

    def ok(rid):
        a, why = activa(rid, E, stats)
        if not a and rid not in st.setdefault("_avisadas", []):
            notes.append(f"{rid} ({REGLAS[rid]['titulo']}) {why}")
            st["_avisadas"].append(rid)
        return a

    def ev(rid):
        t = E.get(rid, {}).get("texto")
        return f" Evidencia: {t}." if t else ""

    if ratio > 0.97:
        # ---------------- R8: el pico esta en el borde de un corte anterior
        for k, op in enumerate(ops):
            if op["tipo"] in O.QUITA and O.dist_to_op(pk["xyz"], op) < 4.0 and ok("R8"):
                new = shrink(op)
                nops = ops[:k] + ([new] if new else []) + ops[k + 1:]
                reinf.append(dict(regla="R8", op=new or dict(tipo="deshacer", de=op), ops_nuevas=nops, reconstruir=True,
                                  titulo=("reducir" if new else "deshacer") + f" la operacion {k + 1} ({O.describe(op)})",
                                  porque=(f"El pico ({sig:.0f} MPa) esta a {O.dist_to_op(pk['xyz'], op):.1f} mm del corte {k + 1} "
                                          f"({O.describe(op)}): ese material SI estaba en el camino de carga. Se "
                                          + ("reduce el corte a 0,6 veces su tamano." if new else "deshace el corte.") + ev("R8")),
                                  espero=dict(dsig_pct=-5.0, txt="baja el pico (vuelve material a donde trabaja)")))
        # ---------------- R4: collar en el perno del pico (+ simetrico)
        if pk["zona"] in ("pernos_del", "pernos_tra") and ok("R4"):
            k = pk["perno"]; ks = symmetric_bolt(k)
            prev = {int(o["perno"]): o for o in ops if o["tipo"] == "collar"}
            for t in (4.0, 6.0):
                tt = prev[k]["t"] + t / 2 if k in prev else t
                if tt > 9.0:
                    continue
                new_ops = [o for o in ops if not (o["tipo"] == "collar" and int(o["perno"]) in (k, ks))]
                add = [dict(tipo="collar", perno=b, t=tt, z=22.0) for b in (k, ks)]
                if any(veto(a) for a in add):
                    continue
                d, hist = _expect("R4", stats, -2.5 * tt)
                reinf.append(dict(regla="R4", op=add[0], ops_nuevas=new_ops + add, reconstruir=bool(prev),
                                  titulo=f"collar de {tt:.0f} mm en los pernos {k + 1} y {ks + 1}",
                                  porque=(f"El pico ({sig:.0f} MPa, {ratio * 100:.0f} % del limite) esta junto al alojamiento del perno "
                                          f"{k + 1} (concentracion local x{pk['kt_aparente']:.1f}). El momento de vuelco de la carga "
                                          f"(F x 44,7 mm) llega a los pernos por una seccion pequena alrededor del alojamiento: un collar "
                                          f"de {tt:.0f} mm aumenta esa seccion. El perno {ks + 1} es su simetrico respecto al plano medio "
                                          f"de las orejetas y trabaja igual." + ev("R4")),
                                  espero=dict(dsig_pct=d, txt=hist or f"del orden de {d:.0f} % (collares anteriores: -15 % con 6 mm)")))
        # ---------------- R5: alojamiento mas ancho (solo si los datos no la contradicen)
        if pk["en_alojamiento"] and pk["kt_aparente"] > 1.8 and ok("R5"):
            op = dict(tipo="alojamiento", perno=pk["perno"], R=11.5)
            if not veto(op):
                reinf.append(dict(regla="R5", op=op, ops_nuevas=ops + [op], titulo=O.describe(op),
                                  porque=f"El pico esta en el acuerdo del fondo del alojamiento (entalla, x{pk['kt_aparente']:.1f})." + ev("R5"),
                                  espero=dict(dsig_pct=-5.0, txt="incierto")))
        # ---------------- R7: orejetas
        if pk["en_orejeta"] and ok("R7"):
            lig = C.ligaments()["ligamento_delante_mm"]
            prev = [o for o in ops if o["tipo"] == "orejeta"]
            ro = (prev[-1]["ro"] if prev else G.RP + lig) + 3.0
            op = dict(tipo="orejeta", ro=round(ro, 2))
            if not veto(op):
                d = (lig / (lig + 3.0) - 1) * 100
                reinf.append(dict(regla="R7", op=op, ops_nuevas=[o for o in ops if o["tipo"] != "orejeta"] + [op],
                                  reconstruir=bool(prev), titulo=O.describe(op),
                                  porque=(f"El pico ({sig:.0f} MPa) esta en la orejeta. Delante del bulon hay {lig:.1f} mm de "
                                          f"ligamento; la tension de aplastamiento/cortadura va como 1/e: +3 mm la reduce ~{-d:.0f} %."
                                          + ev("R7")),
                                  espero=dict(dsig_pct=d, txt=f"~{d:.0f} % (s ~ 1/e)")))
        # ---------------- R6: redondeo de aristas junto al pico
        if pk["kt_aparente"] > 1.8 and not pk["en_alojamiento"] and ok("R6"):
            x, y, z = pk["xyz"]
            op = dict(tipo="redondeo", x=round(x, 2), y=round(y, 2), z=round(z, 2), r=3.0)
            if not any(o["tipo"] == "redondeo" and math.dist((o["x"], o["y"], o["z"]), (x, y, z)) < 4 for o in
                       [r["op"] for r in st.get("rechazos", [])] + ops):
                d, hist = _expect("R6", stats, -8.0)
                reinf.append(dict(regla="R6", op=op, ops_nuevas=ops + [op], titulo=O.describe(op),
                                  porque=(f"El pico ({sig:.0f} MPa, en {zona}) es {pk['kt_aparente']:.1f} veces la tension media "
                                          f"a su alrededor: es una entalla, no falta de seccion. Un acuerdo de 3 mm reduce Kt." + ev("R6")),
                                  espero=dict(dsig_pct=d, txt=hist or "-5 a -15 % (Peterson)")))
    if ratio <= 1.0:
        # ---------------- R1-R3 quitar material ocioso (umbral progresivo, R10)
        ti = st.get("tau_idx", 0)
        while ti < len(TAUS):
            tau = TAUS[ti]
            cols = C.columns(tau, veto=veto) if ok("R1") else []
            cuts = C.top_cuts(tau, veto=veto) if ok("R2") else []
            cavs = C.cavities(tau, veto=veto) if ok("R3") else []
            if cols or cuts or cavs:
                break
            ti += 1
        if ti != st.get("tau_idx", 0) and ti < len(TAUS):
            notes.append(f"R10: ya no queda material por debajo del {TAUS[st.get('tau_idx', 0)] * 100:.0f} % del limite donde "
                         f"quepa un corte -> se pasa al umbral del {TAUS[ti] * 100:.0f} %")
            st["tau_idx"] = ti
        if ti < len(TAUS):
            far = lambda xyz: math.dist(xyz, pk["xyz"])
            for c in cols:
                op = dict(tipo="agujero", x=round(c["x"], 2), y=round(c["y"], 2), r=c["r"])
                d, hist = _expect("R1", stats, 0.0)
                rem.append(dict(regla="R1", op=op, ops_nuevas=ops + [op], titulo=O.describe(op), V=c["V"],
                                porque=(f"Toda la columna en ({c['x']:.0f}, {c['y']:.0f}) hasta {c['r'] + 3:.0f} mm de radio trabaja como "
                                        f"maximo al {c['util_max'] * 100:.0f} % del limite (umbral de material ocioso: {tau * 100:.0f} %): no "
                                        f"esta en el camino de la carga. Con Kt ~ 3 el borde del agujero quedaria por debajo del "
                                        f"~{min(3 * c['util_max'], 1) * 100:.0f} %; el pico ({sig:.0f} MPa, en {zona}) esta a "
                                        f"{far((c['x'], c['y'], pk['xyz'][2])):.0f} mm." + ev("R1")),
                                espero=dict(dm_g=-c["V"] * RHO * 1000, dsig_pct=d, txt=hist or "la tension maxima casi no cambia")))
            for c in cuts:
                op = dict(tipo="rebaje", **{k: round(c[k], 2) for k in ("x0", "x1", "y0", "y1", "zc")}, rr=corner_r(c))
                d, hist = _expect("R2", stats, 0.0)
                rem.append(dict(regla="R2", op=op, ops_nuevas=ops + [op], titulo=O.describe(op), V=c["V"],
                                porque=(f"Todo el material por encima de z = {c['zc']:.0f} mm en esa zona (y 4 mm alrededor) trabaja "
                                        f"por debajo del {tau * 100:.0f} % del limite: ni el momento de vuelco ni el cortante pasan por "
                                        f"ahi. El rebaje deja un suelo horizontal (imprimible) y acuerdos redondeados." + ev("R2")),
                                espero=dict(dm_g=-c["V"] * RHO * 1000, dsig_pct=d, txt=hist or "la tension maxima casi no cambia")))
            for c in cavs:
                op = dict(tipo="hueco", **{k: round(c[k], 2) for k in ("x0", "x1", "y0", "y1", "z0", "z1")})
                d, hist = _expect("R3", stats, 1.0)
                rem.append(dict(regla="R3", op=op, ops_nuevas=ops + [op], titulo=O.describe(op), V=c["V"],
                                porque=(f"El nucleo de esa zona (a mas de 4 mm de cualquier superficie) trabaja por debajo del "
                                        f"{tau * 100:.0f} % del limite: en flexion la tension crece con la distancia a la fibra neutra, asi "
                                        f"que vaciarlo conserva las pieles, que son las que trabajan." + ev("R3")),
                                espero=dict(dm_g=-c["V"] * 0.6 * RHO * 1000, dsig_pct=d, txt=hist or "la tension sube poco")))
        # ---------------- R11: sustituir bloques que trabajan poco por nervios en la trayectoria de la carga
        if ok("R11") and C.pdir is not None:
            vrn = lambda op: veto(dict(op, tipo="rebaje_nervio"))
            regs = [dict(rj["op"], origen="rechazo") for rj in st.get("rechazos", [])
                    if rj["op"]["tipo"] == "rebaje" and rj["motivo_tipo"] == "tension" and not vrn(rj["op"])]
            for tau2 in TAU_NERVIO:
                regs += [dict(r_, origen=f"umbral {tau2 * 100:.0f} %") for r_ in C.top_cuts(tau2, veto=vrn, n_max=3)]
            seen = []
            for reg in regs:
                if any(_overlap_rect(reg, q) > 0.5 for q in seen):
                    continue
                seen.append(reg)
                ribs, info = rib_for_block(C, reg, lim)
                if ribs is None:
                    continue
                cut = dict(tipo="rebaje", **{k: round(reg[k], 2) for k in ("x0", "x1", "y0", "y1", "zc")}, rr=corner_r(reg))
                net = info["V_block"] - info["V_rib"]
                d, hist = _expect("R11", stats, 3.0)
                desc = "; ".join(f"a {f['fam']}: {f['share'] * 100:.0f} % de la carga, direccion ({f['dir'][0]:+.2f}, {f['dir'][1]:+.2f}, "
                                 f"{f['dir'][2]:+.2f}), coherencia {f['coh'] * 100:.0f} % -> nervio de {f['t']:.1f} mm x {f['h']:.0f} mm "
                                 f"({f['A']:.0f} mm2)" for f in info["fams"])
                rem.append(dict(regla="R11", op=dict(cut, tipo="rebaje_nervio"), ops_nuevas=ops + [cut] + ribs, V=net,
                                titulo=(f"sustituir el bloque x {reg['x0']:.0f}..{reg['x1']:.0f}, y {reg['y0']:.0f}..{reg['y1']:.0f} "
                                        f"(por encima de z = {reg['zc']:.0f}) por {len(ribs)} nervio(s) en la trayectoria de la carga"),
                                porque=(f"Ese bloque ({info['V_block'] / 1e3:.0f} cm3) trabaja como maximo al {info['util_max'] * 100:.0f} % del limite"
                                        + (" y quitarlo entero se rechazo (si llevaba carga)" if reg.get("origen") == "rechazo" else "")
                                        + f". Su carga (integral de |s| dV = {info['S'] / 1e3:.0f} kN mm) se reparte asi: {desc}. "
                                        f"Michell: la estructura minima lleva cada familia (traccion y compresion) por su trayectoria; "
                                        f"cada nervio se dimensiona para trabajar al {SIG_TRABAJO * 100:.0f} % del limite: "
                                        f"{info['V_rib'] / 1e3:.1f} cm3 en lugar de {info['V_block'] / 1e3:.0f}. Acuerdo de 3 mm en su raiz." + ev("R11")),
                                espero=dict(dm_g=-net * RHO * 1000, dsig_pct=d, txt=hist or "baja la masa; la tension sube algo")))
    # ---------------- seleccion: diversidad de reglas
    sel = []
    if ratio > 0.97:
        sel += reinf[: max(1, n_max - (1 if ratio <= 1.0 else 0))]
    by_rule = {}
    for c in sorted(rem, key=lambda c: -c["V"]):
        by_rule.setdefault(c["regla"], []).append(c)
    while len(sel) < n_max and any(by_rule.values()):
        for rid in sorted(by_rule, key=lambda r: -(by_rule[r][0]["V"] if by_rule[r] else 0)):
            if by_rule[rid] and len(sel) < n_max:
                sel.append(by_rule[rid].pop(0))
    if not sel and ratio > 1.0 and reinf:
        sel = reinf[:n_max]
    return sel, notes, pk


# =============================================================================================== documento
def write_doc(E=None, stats=None, log=print):
    """DESIGN_RULES.md: reglas, evidencia y resultados de aplicarlas."""
    E = E if E is not None else load_evidence()
    stats = stats or {}
    rs = E.get("_resumen", {})
    L = ["# Reglas de diseno del soporte (DESIGN_RULES)", "",
         f"Actualizado: {datetime.datetime.now():%d/%m/%Y %H:%M}. Generado por `scripts/reglas.py` a partir de:",
         "", f"1. **Estudio de las soluciones publicadas** (SimJEB: los 381 disenos del GE Jet Engine Bracket Challenge, "
             "Whalen et al. 2021, doi:10.7910/DVN/XFUWJG) calculados con **nuestra** carga "
             f"({FORCE:.0f} N en -X por el bulon, pernos empotrados) y **nuestro** limite ({SIG_LIM:.0f} MPa, coef. de seguridad >= 1; "
             f"desplazamiento <= {USER.get('desplazamiento_max_mm', 0.25)} mm). Resultados: `estudio/estudio_simjeb.json`.",
         "2. **Nuestros calculos anteriores** (familias vaciado y refuerzo, 294 disenos con 37 800 N; el modelo es lineal y se "
         f"escalan x{K_LOAD:.3f}). Datos: `estudio/calculos_anteriores.csv`.",
         "3. **Lo que pasa al aplicarlas** en el optimizador (cada aplicacion: tension y masa antes/despues). "
         "Una regla que los datos de un cambio DIRECTO contradicen se DESACTIVA (las comparaciones con SimJEB, entre disenos "
         "distintos, pueden respaldarla o ser no concluyentes, pero no la desactivan); una que falla 8 veces sin ninguna mejora "
         "en el optimizador se SUSPENDE.", ""]
    if rs:
        L += ["## Estudio de las soluciones publicadas", "",
              f"{rs.get('n', 0)} disenos calculados: **{rs.get('valido', 0)} cumplen**, {rs.get('no_cumple', 0)} no cumplen, "
              f"{rs.get('incompatible', 0)} no tienen los agujeros del enunciado (bulon macizo o agujeros de otro tamano), "
              f"{rs.get('fallido', 0)} fallaron (malla). Los que superaban 1,5 veces el limite en la pasada rapida (malla gruesa) "
              "se descartaron sin calculo fino.", ""]
        vals = E.get("_validos", [])
        if vals:
            L += ["Los mas ligeros que cumplen (son la referencia de lo que se puede conseguir; NO se copian: la pieza final "
                  "sale del original modificado paso a paso):", "",
                  "| SimJEB | masa | tension | desplaz. | tipo | material ocioso | pico en |", "|---|---|---|---|---|---|---|"]
            for v in vals[:12]:
                L.append(f"| {v['id']} ({v['autor']}) | {v['masa']:.3f} kg | {v['tension']:.0f} MPa | {v['desp']:.3f} mm | {v['categoria']} | "
                         f"{(v['ocioso'] or 0) * 100:.0f} % | {CA.ZONA_TXT.get(v['zona_pico'], v['zona_pico'] or '-')} |")
            L.append("")
            imgs = [v for v in vals[:6] if os.path.exists(os.path.join(EST, "img", f"simjeb_{v['id']}.png"))]
            if imgs:
                L += [" ".join(f"<img src=\"estudio/img/simjeb_{v['id']}.png\" width=\"260\" title=\"SimJEB {v['id']}\">" for v in imgs), ""]
    L += ["## Reglas", ""]
    for rid, R in REGLAS.items():
        e = E.get(rid, {}); s = stats.get(rid, {})
        a, why = activa(rid, E, stats)
        estado = "ACTIVA" if a else why.upper()
        resp = {True: "respaldada por los datos", False: "CONTRADICHA por los datos", None: "basada en la teoria / en sus resultados"}[e.get("respaldo")]
        L += [f"### {rid}. {R['titulo']}  ({estado})", "",
              f"- **Si:** {R['si']}.", f"- **Hago:** {R['hago']}.", f"- **Porque:** {R['porque']}",
              f"- **Espero:** {R['espero']}.", f"- **Evidencia ({resp}):** {e.get('texto', 'pendiente del estudio')}."]
        if s.get("intentos"):
            ds = s.get("dsig", []); dm = s.get("dm", [])
            L.append(f"- **Aplicada en el optimizador:** {s.get('intentos', 0)} veces ({s.get('descartadas_rapido', 0)} descartadas en la "
                     f"evaluacion rapida, {s.get('aceptadas', 0)} aceptadas, {s.get('rechazadas', 0)} rechazadas)"
                     + (f"; tension {np.median(ds):+.1f} % (mediana), masa {np.median(dm):+.0f} g (mediana)" if ds else "") + ".")
            dp = s.get("dsig_prev", [])
            if dp and ds:
                L.append(f"  - calibracion de la evaluacion rapida (malla gruesa): cambio de tension previsto {np.median(dp):+.1f} % "
                         f"frente a {np.median(ds[-len(dp):]):+.1f} % real (mediana de {len(dp)})")
            for ex in s.get("ejemplos", [])[-4:]:
                L.append(f"  - iteracion {ex[0]}: {ex[1]}")
        if e.get("tabla"):
            L += [""] + e["tabla"]
        L.append("")
    L += ["---", "Las reglas R9 y R10 son de procedimiento (como aplicar las demas). La lista completa de iteraciones, con el "
          "antes y el despues de cada cambio, esta en `runs/opt_<carga>N/ITERACIONES.md`."]
    open(DOC, "w", encoding="utf-8").write("\n".join(L) + "\n")


def render_valid_images(E, n=6, log=print):
    import render
    os.makedirs(os.path.join(EST, "img"), exist_ok=True)
    for v in E.get("_validos", [])[:n]:
        png = os.path.join(EST, "img", f"simjeb_{v['id']}.png")
        if os.path.exists(png):
            continue
        try:
            d = np.load(os.path.join(WORK, f"{v['id']:03d}", "campos.npz"))
            render.results_png(d["nodes"], d["tris"], d["vm"], png, f"SimJEB {v['id']}: {v['masa']:.3f} kg, {v['tension']:.0f} MPa")
        except Exception as e:
            log(f"  (imagen SimJEB {v['id']}: {e})")


if __name__ == "__main__":
    E = evidence()
    render_valid_images(E)
    write_doc(E)
    print(json.dumps(E.get("_resumen"), indent=1))
    for r in REGLAS:
        print(r, E.get(r, {}).get("respaldo"), "|", (E.get(r, {}).get("texto") or "")[:160])
