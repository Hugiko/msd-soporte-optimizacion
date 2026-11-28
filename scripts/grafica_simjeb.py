"""Grafica del estudio de las soluciones publicadas (SimJEB) con NUESTRAS condiciones y posicion de nuestra pieza.

Lee estudio/estudio_simjeb.json (381 disenos calculados con 42 258 N en -X, pernos empotrados, misma metrica) y
runs/opt_42258N/MEJOR_GLOBAL.json (nuestra mejor pieza). Escribe figuras/comparativa_simjeb.png y
estudio/comparativa_simjeb.csv (tabla con lo representado)."""
import os, json, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TOP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIM, U_LIM = 215.0, 0.25
# colores (paleta de referencia validada: azul y naranja; gris neutro solo como contexto)
SURF, INK, INK2, INK3, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8c8b85", "#e4e3df"
OK, OURS, NO = "#2a78d6", "#eb6834", "#a9a8a2"

d = json.load(open(os.path.join(TOP, "estudio", "estudio_simjeb.json"), encoding="utf-8"))
best = json.load(open(os.path.join(TOP, "runs", "opt_42258N", "MEJOR_GLOBAL.json"), encoding="utf-8"))
ref = json.load(open(os.path.join(TOP, "cad", "referencia_original", "resultados_referencia.json"), encoding="utf-8"))
k_lin = 42258.0 / 37800.0                       # modelo lineal: la referencia del original esta calculada con 37 800 N
orig = dict(m=ref["mass_kg"], s=ref["vm_metric"] * k_lin, u=ref["u_max"] * k_lin)
ours = dict(m=best["mass_kg"], s=best["vm_metric"], u=best["u_max"], s_fino=best["verificacion"]["vm_metric"])
irr = None
st = json.load(open(os.path.join(TOP, "runs", "opt_42258N", "estado.json"), encoding="utf-8"))
for h in st["historia"]:
    if h["iter"] == 68 and h.get("m_cand"):
        irr = dict(m=h["m_cand"]["mass_kg"], s=h["m_cand"]["vm_metric"])

rows = [v for v in d.values() if v.get("veredicto") in ("valido", "no_cumple") and v.get("masa_kg") and v.get("tension_MPa")]
val = [v for v in rows if v["veredicto"] == "valido"]
nc_n = [v for v in rows if v["veredicto"] == "no_cumple" and v.get("fidelidad") == "normal"]
nc_r = [v for v in rows if v["veredicto"] == "no_cumple" and v.get("fidelidad") != "normal"]
n_inc = sum(1 for v in d.values() if v.get("veredicto") == "incompatible")
n_fal = sum(1 for v in d.values() if v.get("veredicto") == "fallido")
n_u = sum(1 for v in rows if v["veredicto"] == "no_cumple" and v["tension_MPa"] <= LIM and (v.get("desp_mm") or 0) > U_LIM)
val_sorted = sorted(val, key=lambda v: v["masa_kg"])
rank = 1 + sum(1 for v in val if v["masa_kg"] < ours["m"])

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": INK3, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.titlecolor": INK, "axes.titlesize": 11.5,
                     "axes.titleweight": "bold", "axes.titlelocation": "left"})
fig, (a1, a2) = plt.subplots(1, 2, figsize=(15, 7.4), dpi=150, facecolor=SURF)
fig.subplots_adjust(left=0.06, right=0.985, top=0.86, bottom=0.17, wspace=0.2)


def style(ax):
    ax.set_facecolor(SURF)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)


def dots(ax, vs, **kw):
    ax.scatter([v["masa_kg"] for v in vs], [v["tension_MPa"] for v in vs], **kw)


# ---------------- (a) todos los disenos calculados
style(a1)
a1.set_yscale("log")
a1.axhspan(10, LIM, color=OK, alpha=0.07, zorder=0, lw=0)
a1.axhline(LIM, color=INK2, lw=1.2, ls=(0, (5, 3)), zorder=1)
dots(a1, nc_r, s=26, facecolors="none", edgecolors=NO, linewidths=1.0, zorder=2,
     label=f"No cumple, descartado en la pasada rápida ({len(nc_r)})")
dots(a1, nc_n, s=30, c=NO, edgecolors=SURF, linewidths=0.8, zorder=3, label=f"No cumple, malla completa ({len(nc_n)})")
dots(a1, val, s=46, c=OK, edgecolors=SURF, linewidths=1.0, zorder=4, label=f"Cumple: σ ≤ 215 MPa y u ≤ 0,25 mm ({len(val)})")
a1.scatter([orig["m"]], [orig["s"]], s=90, marker="D", facecolors=SURF, edgecolors=INK, linewidths=1.6, zorder=5,
           label="Soporte original del enunciado (0.stp)")
a1.scatter([ours["m"]], [ours["s"]], s=260, marker="*", c=OURS, edgecolors=SURF, linewidths=1.0, zorder=6,
           label=f"Nuestra pieza (iteración {best['iter']})")
a1.set_ylim(100, 10000)
xmax = max(v["masa_kg"] for v in rows) * 1.05
a1.set_xlim(0, xmax)
a1.text(0.05, LIM * 1.06, "Límite: 215 MPa (CS = 1)", ha="left", va="bottom", color=INK2, fontsize=9)
a1.set_xlabel("Masa en acero S235 (kg)")
a1.set_ylabel("Tensión de von Mises máxima, métrica del proyecto (MPa, escala log.)")
a1.set_title(f"(a) Las {len(rows)} soluciones publicadas calculables")
a1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:,.0f}".replace(",", ".")))
leg = a1.legend(loc="upper right", fontsize=8.6, frameon=True, facecolor=SURF, edgecolor=GRID, labelcolor=INK2)


# ---------------- (b) ampliacion de la zona que cumple
style(a2)
x0, x1, y0, y1 = 1.85, 3.75, 140, 260
a2.axhspan(0, LIM, color=OK, alpha=0.07, zorder=0, lw=0)
a2.axhline(LIM, color=INK2, lw=1.2, ls=(0, (5, 3)), zorder=1)
win = lambda vs: [v for v in vs if x0 <= v["masa_kg"] <= x1 and y0 <= v["tension_MPa"] <= y1]
dots(a2, win(nc_r), s=30, facecolors="none", edgecolors=NO, linewidths=1.0, zorder=2)
dots(a2, win(nc_n), s=36, c=NO, edgecolors=SURF, linewidths=0.8, zorder=3)
dots(a2, val, s=60, c=OK, edgecolors=SURF, linewidths=1.2, zorder=4)
# frente de Pareto de los que cumplen (menos masa para cada tension)
pf, smin = [], 1e9
for v in val_sorted:
    if v["tension_MPa"] < smin:
        pf.append(v); smin = v["tension_MPa"]
for v in val:
    if v["id"] in (492, 411, 475):
        a2.annotate(f"n.º {v['id']}", (v["masa_kg"], v["tension_MPa"]), xytext=(7, -3), textcoords="offset points",
                    fontsize=7.8, color=INK3)
a2.scatter([orig["m"]], [orig["s"]], s=100, marker="D", facecolors=SURF, edgecolors=INK, linewidths=1.6, zorder=5)
a2.annotate(f"Original\n{orig['m']:.3f} kg · {orig['s']:.0f} MPa (CS {LIM / orig['s']:.2f})", (orig["m"], orig["s"]),
            xytext=(12, 2), textcoords="offset points", fontsize=8.6, color=INK)
if irr:
    a2.scatter([irr["m"]], [irr["s"]], s=110, marker="*", facecolors=SURF, edgecolors=OURS, linewidths=1.3, zorder=5)
    a2.annotate(f"Vaciado irregular (it. 68)\n{irr['m']:.3f} kg · {irr['s']:.0f} MPa", (irr["m"], irr["s"]),
                xytext=(1.875, 205.5), textcoords="data", fontsize=8.0, color=INK2, ha="left",
                arrowprops=dict(arrowstyle="-", color=INK3, lw=0.7))
a2.scatter([ours["m"]], [ours["s"]], s=330, marker="*", c=OURS, edgecolors=SURF, linewidths=1.0, zorder=6)
a2.annotate(f"Nuestra pieza (formas puras, it. {best['iter']})\n{ours['m']:.3f} kg · {ours['s']:.1f} MPa (malla fina {ours['s_fino']:.1f})\n"
            f"{rank}.ª más ligera de las {len(val) + 1} que cumplen", (ours["m"], ours["s"]), xytext=(2.6, 202),
            textcoords="data", fontsize=8.8, color=INK, fontweight="bold",
            arrowprops=dict(arrowstyle="-", color=INK3, lw=0.8))
a2.annotate("", xy=(ours["m"], ours["s"]), xytext=(orig["m"], orig["s"]),
            arrowprops=dict(arrowstyle="->", color=OURS, lw=1.4, alpha=0.75, connectionstyle="arc3,rad=-0.2"), zorder=4)
lb = val_sorted[0]
a2.annotate(f"n.º {lb['id']}: el publicado más ligero\nque cumple, {lb['masa_kg']:.3f} kg · {lb['tension_MPa']:.0f} MPa",
            (lb["masa_kg"], lb["tension_MPa"]), xytext=(1.875, 170), textcoords="data", fontsize=8.0, color=INK2,
            arrowprops=dict(arrowstyle="-", color=INK3, lw=0.7))
a2.set_xlim(x0, x1); a2.set_ylim(y0, y1)
a2.text(x1 - 0.02, LIM + 2, "No cumple (σ > 215 MPa)", ha="right", va="bottom", color=INK2, fontsize=8.8)
a2.text(x1 - 0.02, y0 + 2, "Cumple (CS ≥ 1)", ha="right", va="bottom", color=INK2, fontsize=8.8)
a2.set_xlabel("Masa en acero S235 (kg)")
a2.set_ylabel("Tensión de von Mises máxima (MPa)")
a2.set_title("(b) Ampliación junto al límite: dónde queda nuestra pieza")
fig.text(0.06, 0.02, "Mismo modelo para todos: acero S235, 42 258 N en −X repartidos por RBE3 en el bulón, superficies de los 4 pernos empotradas,\n"
         "tetraedros de 2.º orden de 4 mm (pasada rápida: 6 mm), von Mises máximo sin 5 mm alrededor de los pernos ni 2 mm alrededor del bulón.\n"
         f"No se representan {n_inc} diseños incompatibles (sin los agujeros del enunciado) ni {n_fal} cuya geometría no se pudo mallar. "
         f"Ninguno de los {len(nc_n) + len(nc_r)} que no cumplen falla solo por desplazamiento (límite 0,25 mm). Datos: estudio/comparativa_simjeb.csv.",
         fontsize=8.3, color=INK3, va="bottom")
fig.suptitle("Soluciones publicadas (SimJEB, 381 diseños) calculadas con las condiciones del Soporte 6",
             x=0.06, y=0.965, ha="left", fontsize=13.5, fontweight="bold", color=INK)
out = os.path.join(TOP, "figuras", "comparativa_simjeb.png")
fig.savefig(out, facecolor=SURF)
print(out)

# ---------------- tabla con lo representado (vista de tabla)
with open(os.path.join(TOP, "estudio", "comparativa_simjeb.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["id", "categoria", "autor", "veredicto", "fidelidad", "masa_kg", "tension_MPa", "cs", "desp_mm"])
    w.writerow(["original", "", "enunciado (0.stp)", "no_cumple", "normal (37 800 N x 1,118)", f"{orig['m']:.4f}", f"{orig['s']:.1f}",
                f"{LIM / orig['s']:.3f}", f"{orig['u']:.4f}"])
    w.writerow([f"nuestra (it. {best['iter']})", "formas puras", "grupo 831_MSD_13_B", "valido", "normal (fina: %.1f MPa)" % ours["s_fino"],
                f"{ours['m']:.4f}", f"{ours['s']:.1f}", f"{LIM / ours['s']:.3f}", f"{ours['u']:.4f}"])
    for v in sorted(rows, key=lambda v: (v["veredicto"] != "valido", v["masa_kg"])):
        w.writerow([v["id"], v.get("categoria"), v.get("autor"), v["veredicto"], v.get("fidelidad"), f"{v['masa_kg']:.4f}",
                    f"{v['tension_MPa']:.1f}", f"{LIM / v['tension_MPa']:.3f}", f"{v.get('desp_mm') or 0:.4f}"])
print(f"cumplen {len(val)} | no cumplen {len(nc_n) + len(nc_r)} ({len(nc_r)} en la pasada rapida; {n_u} solo por desplazamiento) | "
      f"incompatibles {n_inc} | fallidos {n_fal} | nuestra pieza: {rank}.a mas ligera de {len(val) + 1}")
print("cumplen:", [(v["id"], round(v["masa_kg"], 3), round(v["tension_MPa"], 1)) for v in val_sorted])
