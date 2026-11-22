"""Graficas de cada familia: evolucion, importancia de parametros y comparacion con el original."""
import os, sys, json, glob, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fem

COL = {"valido": "#1a9850", "cerca_del_limite": "#fdae61", "descartado": "#d73027", "fallido": "#555555"}


def make(fam):
    from optimizer import category, SIG_OBJ, fit_gp, gp_lengthscales, score
    runs = fam.runs()
    if not runs:
        return
    gd = os.path.join(fam.out, "graficas"); os.makedirs(gd, exist_ok=True)

    # 1) evolucion
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))
    best, bx, by = None, [], []
    for r in runs:
        m = r["m"]; c = category(m); mass = m.get("mass_kg") or m.get("mass_cad_kg")
        if mass:
            ax[0].scatter(r["id"], mass, c=COL[c], s=26, zorder=3)
        if c == "valido" and (best is None or score(m) < best[0]):
            best = (score(m), m["mass_kg"])
        if best:
            bx.append(r["id"]); by.append(best[1])
        if m.get("vm_metric"):
            ax[1].scatter(r["id"], m["vm_metric"], c=COL[c], s=26, zorder=3)
    if bx:
        ax[0].step(bx, by, where="post", c="k", lw=2, label="mejor diseno (compromiso masa-seguridad)")
    ax[0].axhline(2.411, c="0.5", ls=":", label="original (2,411 kg)")
    for k, v in COL.items():
        ax[0].scatter([], [], c=v, label=k.replace("_", " "))
    ax[0].set_xlabel("Diseno n.o"); ax[0].set_ylabel("Masa (kg)"); ax[0].legend(fontsize=8); ax[0].grid(alpha=.3)
    ax[1].axhline(SIG_OBJ, c="#d73027", ls="--", label=f"limite {SIG_OBJ:.0f} MPa")
    ax[1].set_yscale("log"); ax[1].set_xlabel("Diseno n.o"); ax[1].set_ylabel("Tension de von Mises (MPa)")
    ax[1].legend(fontsize=8); ax[1].grid(alpha=.3, which="both")
    fig.suptitle(f"{fam.title}: evolucion del optimizador"); fig.tight_layout()
    fig.savefig(os.path.join(gd, "evolucion.png"), dpi=150); plt.close(fig)

    # 2) importancia de parametros (1 / longitud de escala de los procesos gaussianos)
    ok = [r for r in runs if r["m"].get("status") == "ok"]
    if len(ok) >= 8:
        X = np.array([fam.to_unit(r["p"]["params"]) for r in ok]); imp = {}
        for name, y in (("tension", [math.log(r["m"]["vm_metric"]) for r in ok]),
                        ("masa", [math.log(r["m"]["mass_kg"]) for r in ok])):
            try:
                ls = gp_lengthscales(fit_gp(X, y))
                if ls is not None:
                    imp[name] = (1 / ls) / np.sum(1 / ls)
            except Exception:
                pass
        if imp:
            fig, ax = plt.subplots(figsize=(10, 4.5)); idx = np.arange(fam.D); w = 0.4
            for j, (k, v) in enumerate(imp.items()):
                ax.bar(idx + (j - 0.5) * w, v, w, label=f"influencia en la {k}")
            ax.set_xticks(idx); ax.set_xticklabels(fam.names, rotation=30, ha="right")
            ax.set_ylabel("Importancia relativa (-)"); ax.legend(); ax.grid(alpha=.3, axis="y")
            ax.set_title(f"{fam.title}: que parametros importan mas")
            fig.tight_layout(); fig.savefig(os.path.join(gd, "importancia_parametros.png"), dpi=150); plt.close(fig)
            json.dump({k: dict(zip(fam.names, map(float, v))) for k, v in imp.items()},
                      open(os.path.join(gd, "importancia_parametros.json"), "w"), indent=1)

    # 3) original frente al mejor de la familia
    val = sorted([r for r in ok if category(r["m"]) == "valido"], key=lambda r: score(r["m"]))
    ref = os.path.join(fem.ROOT, "cad", "referencia_original", "resultados_referencia.json")
    if val and os.path.exists(ref):
        mb = json.load(open(ref)); mf = val[0]["m"]
        rows = [("Masa (kg)", mb["mass_kg"], mf["mass_kg"]), ("Tension (MPa)", mb["vm_metric"], mf["vm_metric"]),
                ("Coef. seguridad 215/tension", 215 / mb["vm_metric"], 215 / mf["vm_metric"]),
                ("Desplazamiento max. (mm)", mb["u_max"], mf["u_max"])]
        fig, ax = plt.subplots(figsize=(8, 2.6)); ax.axis("off")
        t = ax.table(cellText=[[a, f"{b:.3f}", f"{c:.3f}", f"{(c - b) / b * 100:+.1f} %"] for a, b, c in rows],
                     colLabels=["Magnitud", "Original", f"Mejor {fam.key} (#{val[0]['id']:03d})", "Cambio"], loc="center")
        t.scale(1, 1.6); t.auto_set_font_size(False); t.set_fontsize(10)
        fig.tight_layout(); fig.savefig(os.path.join(gd, "original_vs_mejor.png"), dpi=150); plt.close(fig)


if __name__ == "__main__":
    from optimizer import Family, CFG
    for k in CFG["families"]:
        make(Family(k))
