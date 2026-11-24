"""ANALISIS DEL CAMPO DE TENSIONES de una pieza ya calculada en ANSYS.

Responde a las preguntas que usan las reglas de diseno:
  - que material TRABAJA y cual esta OCIOSO (tension muy por debajo del limite);
  - DONDE esta el pico de tension (alojamiento de un perno, orejeta, union...) y si es una concentracion local
    (entalla: se arregla con un acuerdo) o falta de seccion (se arregla anadiendo material);
  - como se reparte la masa y la tension por ZONAS (pernos delanteros/traseros, placa base, cuerpo, orejetas);
  - donde caben aligeramientos pasantes, rebajes desde arriba y huecos interiores en material ocioso.
Se usa igual para los disenos publicados (estudio SimJEB) y para la pieza que se esta optimizando.
"""
import math
import numpy as np
from scipy.spatial import cKDTree
import fem
import geometry as G

PIN_A = np.array(fem.HOLES["bulon"]["axis"], float); PIN_A /= np.linalg.norm(PIN_A)
PIN_P = np.mean(np.array(fem.HOLES["bulon"]["centers"], float), axis=0)
LOAD = np.array(fem.load_dir(), float)
R_POCKET0 = 10.541
ZONAS = ["pernos_del", "pernos_tra", "orejetas", "placa_base", "cuerpo_del", "cuerpo_tra"]
ZONA_TXT = {"pernos_del": "alrededor de los pernos delanteros", "pernos_tra": "alrededor de los pernos traseros",
            "orejetas": "orejetas del bulon", "placa_base": "placa base (z < 10 mm)",
            "cuerpo_del": "cuerpo, lado de las orejetas (x < 15 mm)", "cuerpo_tra": "cuerpo, lado trasero (x >= 15 mm)"}
R_ZONA_PERNO = 20.0
X_CORTE = 15.0


def pin_coords(xyz):
    v = np.asarray(xyz, float) - PIN_P
    t = v @ PIN_A
    perp = v - np.outer(t, PIN_A)
    return t, np.linalg.norm(perp, axis=1), perp


def zone_of(xyz):
    """Zona de cada punto (array de nombres)."""
    xyz = np.atleast_2d(np.asarray(xyz, float))
    out = np.where(xyz[:, 0] < X_CORTE, "cuerpo_del", "cuerpo_tra").astype(object)
    out[xyz[:, 2] < 10.0] = "placa_base"
    t, rho, _ = pin_coords(xyz)
    out[(rho < G.RP + 15.0) & (np.abs(t) < 26.0)] = "orejetas"
    for i, b in enumerate(G.BOLTS):
        near = (np.hypot(xyz[:, 0] - b["c"][0], xyz[:, 1] - b["c"][1]) < R_ZONA_PERNO) & (xyz[:, 2] < 30.0)
        out[near] = "pernos_del" if i in G.FRONT else "pernos_tra"
    return out


class Campo:
    def __init__(self, nodes, tets4, vm, tris=None, sig_lim=215.0, peak_xyz=None, peak_vm=None, sig6=None, sym=False):
        nodes = np.asarray(nodes, float); tets4 = np.asarray(tets4, int); vm = np.asarray(vm, float)
        P = nodes[tets4]
        a, b, c, d = P[:, 0], P[:, 1], P[:, 2], P[:, 3]
        self.vol = np.abs(np.einsum("ij,ij->i", np.cross(b - a, c - a), d - a)) / 6.0
        self.cen = P.mean(axis=1)
        sv = vm[tets4]
        self.se = sv.mean(axis=1)                # tension media del elemento (nodos esquina)
        self.smax = sv.max(axis=1)               # la mayor de sus esquinas (criterio conservador)
        self.lim = float(sig_lim)
        self.nodes, self.vm = nodes, vm
        self.surf = nodes[np.unique(np.asarray(tris)[:, :3] - 1)] if tris is not None else None
        self.zona = zone_of(self.cen)
        self.peak_xyz = np.array(peak_xyz, float) if peak_xyz is not None else None
        self.peak_vm = peak_vm
        import operaciones as O
        self.prot = O.in_protected(self.cen)
        self._tree2 = None
        if sym:     # SIMETRIA: un material solo es "ocioso" si tambien lo es en el lado simetrico (y lo protegido, en los dos)
            cm = self.cen - 2.0 * ((self.cen - PIN_P) @ PIN_A)[:, None] * PIN_A
            dd, nn = cKDTree(self.cen).query(cm)
            ok = dd < 3.0
            self.smax = np.where(ok, np.maximum(self.smax, self.smax[nn]), self.smax)
            self.prot = self.prot | (ok & self.prot[nn])
        self.pval = self.pdir = None
        if sig6 is not None:                      # tensor medio de cada elemento -> tensiones y direcciones principales
            t = np.asarray(sig6, float)[tets4].mean(axis=1)
            T = np.empty((len(t), 3, 3))
            T[:, 0, 0], T[:, 1, 1], T[:, 2, 2] = t[:, 0], t[:, 1], t[:, 2]
            T[:, 0, 1] = T[:, 1, 0] = t[:, 3]; T[:, 1, 2] = T[:, 2, 1] = t[:, 4]; T[:, 0, 2] = T[:, 2, 0] = t[:, 5]
            self.pval, self.pdir = np.linalg.eigh(T)          # valores ascendentes; columnas = direcciones

    def load_path(self, mask):
        """Direccion DOMINANTE en la que trabaja el material de 'mask' (trayectoria de carga): media, ponderada por
        |s| x volumen, de la direccion principal de mayor |s| de cada elemento (tensor de orientacion, sin signo).
        Devuelve (direccion unitaria 3D, coherencia 0-1, centroide ponderado, 'traccion'/'compresion')."""
        if self.pdir is None or not mask.any():
            return None
        idx = np.flatnonzero(mask)
        k = np.abs(self.pval[idx]).argmax(axis=1)
        v = np.take_along_axis(self.pdir[idx], k[:, None, None].repeat(3, 1), 2)[:, :, 0]   # columna k de cada matriz
        sv = np.take_along_axis(self.pval[idx], k[:, None], 1)[:, 0]
        w = np.abs(sv) * self.vol[idx]
        M = np.einsum("i,ij,ik->jk", w, v, v) / max(w.sum(), 1e-12)
        ev, evec = np.linalg.eigh(M)
        d = evec[:, -1]
        c = (self.cen[idx] * w[:, None]).sum(0) / max(w.sum(), 1e-12)
        sign = "traccion" if (sv * w).sum() > 0 else "compresion"
        return d, float(ev[-1]), c, sign

    # ------------------------------------------------------------------ caracteristicas (estudio y reglas)
    def low(self, tau):
        return self.smax < tau * self.lim

    def features(self, tau=0.15):
        V = float(self.vol.sum())
        util = self.se / self.lim
        f = dict(volumen_cm3=V / 1e3, util_media=float((util * self.vol).sum() / V),
                 ocioso=float(self.vol[self.low(tau)].sum() / V), tau=tau)
        # material que trabaja a menos del tau x SU PROPIO pico: eficiencia del diseno, cumpla o no el limite
        pk = self.peak_vm if self.peak_vm is not None else float(self.se.max())
        f["ocioso_rel"] = float(self.vol[self.smax < tau * pk].sum() / V)
        for z in ZONAS:
            m = self.zona == z
            vz = float(self.vol[m].sum())
            f[f"V_{z}_cm3"] = vz / 1e3
            f[f"frac_{z}"] = vz / V
            f[f"util_{z}"] = float((util[m] * self.vol[m]).sum() / vz) if vz > 0 else None
            f[f"ocioso_{z}"] = float(self.vol[m & self.low(tau)].sum() / vz) if vz > 0 else None
        if self.peak_xyz is not None:
            f["zona_pico"] = str(zone_of(self.peak_xyz)[0])
            f.update({f"pico_{k}": v for k, v in self.peak_info().items() if k in ("en_alojamiento", "kt_aparente", "perno")})
        f.update(self.ligaments())
        f["altura_mm"] = float(self.nodes[:, 2].max())
        f["z_centroide_mm"] = float((self.cen[:, 2] * self.vol).sum() / V)
        f["frac_sobre_20mm"] = float(self.vol[self.cen[:, 2] > 20.0].sum() / V)
        return f

    def ligaments(self):
        """Material alrededor del bulon en las orejetas: delante (direccion de la carga) y encima."""
        t, rho, perp = pin_coords(self.cen)
        inlug = (np.abs(t) < 26.0) & (rho > G.RP) & (rho < 45.0)
        out = {}
        for name, u in (("ligamento_delante_mm", LOAD / np.linalg.norm(LOAD)), ("ligamento_encima_mm", np.array([0, 0, 1.0]))):
            cosang = (perp @ u) / np.maximum(rho, 1e-9)
            sect = inlug & (cosang > math.cos(math.radians(30)))
            out[name] = float(rho[sect].max() - G.RP) if sect.any() else 0.0
        return out

    # ------------------------------------------------------------------ el pico
    def peak_info(self):
        p = self.peak_xyz
        if p is None:
            i = int(np.argmax(self.se)); p = self.cen[i]
        dists = [math.hypot(p[0] - b["c"][0], p[1] - b["c"][1]) for b in G.BOLTS]
        k = int(np.argmin(dists))
        t, rho, _ = pin_coords(p[None, :])
        en_aloj = dists[k] < R_POCKET0 + 3.0 and G.Z1 - 0.5 < p[2] < G.Z1 + 8.0
        # concentracion local: pico / tension media del material en 12 mm alrededor (alto = entalla; bajo = seccion)
        near = np.linalg.norm(self.cen - p, axis=1) < 12.0
        ref = float((self.se[near] * self.vol[near]).sum() / max(self.vol[near].sum(), 1e-9)) if near.any() else 0.0
        peak = self.peak_vm if self.peak_vm is not None else float(self.se.max())
        return dict(xyz=[float(v) for v in p], zona=str(zone_of(p)[0]), perno=k, dist_perno=dists[k],
                    en_alojamiento=bool(en_aloj), en_orejeta=bool(rho[0] < G.RP + 15.0 and abs(t[0]) < 26.0),
                    kt_aparente=peak / max(ref, 1e-6), tension=peak)

    # ------------------------------------------------------------------ donde quitar material
    def columns(self, tau, radii=(15, 12, 10, 8, 6, 5, 4), margin=3.0, v_min=1500.0, n_max=6, veto=None):
        """Aligeramientos pasantes verticales: TODA la columna (r + margen) por debajo de tau x limite."""
        if self._tree2 is None:
            self._tree2 = cKDTree(self.cen[:, :2])
        tr = self._tree2
        low = self.low(tau)
        x0, y0 = self.cen[:, :2].min(axis=0); x1, y1 = self.cen[:, :2].max(axis=0)
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1e-9, 3.0), np.arange(y0, y1 + 1e-9, 3.0))
        pts = np.c_[gx.ravel(), gy.ravel()]
        d, _ = tr.query(pts)
        pts = pts[d < 3.0]
        cands = []
        for r in radii:
            outer = tr.query_ball_point(pts, r + margin)
            inner = tr.query_ball_point(pts, r)
            for p, io, ii in zip(pts, outer, inner):
                if not ii or not io:
                    continue
                io = np.asarray(io); ii = np.asarray(ii)
                if not low[io].all():
                    continue
                keep = ii[~self.prot[ii]]
                V = float(self.vol[keep].sum())
                if V >= v_min:
                    cands.append(dict(x=float(p[0]), y=float(p[1]), r=float(r), V=V,
                                      util_max=float(self.smax[io].max() / self.lim)))
        cands.sort(key=lambda c: -c["V"])
        sel = []
        for c in cands:
            if veto and veto(dict(tipo="agujero", x=c["x"], y=c["y"], r=c["r"])):
                continue
            if all(math.hypot(c["x"] - s["x"], c["y"] - s["y"]) >= c["r"] + s["r"] + 4.0 for s in sel):
                sel.append(c)
            if len(sel) >= n_max:
                break
        return sel

    def top_cuts(self, tau, b=4.0, z_floor=5.0, v_min=2000.0, n_max=6, veto=None):
        """Rebajes desde arriba: rectangulo en planta y cota de corte zc tal que TODO el material por encima de zc
        (con 4 mm de margen alrededor) esta por debajo de tau x limite. Deja siempre >= z_floor mm de suelo."""
        from numpy.lib.stride_tricks import sliding_window_view as swv
        from scipy.ndimage import maximum_filter
        c = self.cen
        x0, y0 = c[:, 0].min() - b, c[:, 1].min() - b
        ix = ((c[:, 0] - x0) // b).astype(int); iy = ((c[:, 1] - y0) // b).astype(int)
        nx, ny = ix.max() + 2, iy.max() + 2
        zlow = np.full((nx, ny), -1e9)
        hi = ~self.low(tau)
        np.maximum.at(zlow, (ix[hi], iy[hi]), c[hi, 2] + b)
        zlow = maximum_filter(zlow, size=3, mode="constant", cval=-1e9)     # margen de 1 celda (4 mm)
        dz = 2.0
        L = np.arange(z_floor, c[:, 2].max() + dz, dz)
        kz = np.clip(((c[:, 2] - z_floor) // dz).astype(int), -1, len(L) - 1)
        H = np.zeros((len(L), nx, ny))
        free = ~self.prot & (kz >= 0)
        np.add.at(H, (kz[free], ix[free], iy[free]), self.vol[free])
        A = np.cumsum(H[::-1], axis=0)[::-1]           # A[k] = volumen (no protegido) por encima de L[k]
        S = np.zeros((len(L), nx + 1, ny + 1))
        S[:, 1:, 1:] = A.cumsum(1).cumsum(2)
        cands = []
        for w in range(3, nx):
            for h in range(3, ny):
                zc = np.maximum(swv(zlow, (w, h)).max(axis=(-2, -1)), z_floor)
                k = np.ceil((zc - z_floor) / dz).astype(int)
                ok = k < len(L)
                if not ok.any():
                    continue
                I, J = np.nonzero(ok)
                kk = k[I, J]
                V = S[kk, I + w, J + h] - S[kk, I, J + h] - S[kk, I + w, J] + S[kk, I, J]
                best = np.argsort(-V)[:8]
                for q in best:
                    if V[q] >= v_min:
                        i, j = I[q], J[q]
                        cands.append(dict(x0=float(x0 + i * b), x1=float(x0 + (i + w) * b), y0=float(y0 + j * b),
                                          y1=float(y0 + (j + h) * b), zc=float(z_floor + kk[q] * dz), V=float(V[q])))
        cands.sort(key=lambda d: -d["V"])
        sel = []
        for cd in cands:
            self._open_slivers(cd)
            if veto and veto(dict(tipo="rebaje", **{k: cd[k] for k in ("x0", "x1", "y0", "y1", "zc")})):
                continue
            if all(_rect_overlap(cd, s) < 0.3 for s in sel):
                sel.append(cd)
            if len(sel) >= n_max:
                break
        return sel

    def bottom_cuts(self, tau, b=4.0, z_min=3.0, v_min=1200.0, n_max=6, veto=None, am_t=1.0):
        """Bolsillos desde la CARA DE APOYO (abajo): rectangulo en planta y altura zt tal que todo el material por DEBAJO
        de zt (con 4 mm de margen alrededor y encima) esta por debajo de tau x limite. Para imprimir sin soportes el techo
        es a cuatro aguas (45 grados): el lado menor del bolsillo no puede pasar de 2 x zt / tan + 3 mm (ranuras)."""
        from numpy.lib.stride_tricks import sliding_window_view as swv
        from scipy.ndimage import minimum_filter
        c = self.cen
        x0, y0 = c[:, 0].min() - b, c[:, 1].min() - b
        ix = ((c[:, 0] - x0) // b).astype(int); iy = ((c[:, 1] - y0) // b).astype(int)
        nx, ny = ix.max() + 2, iy.max() + 2
        zhi = np.full((nx, ny), 1e9)
        hi = ~self.low(tau) | self.prot
        np.minimum.at(zhi, (ix[hi], iy[hi]), c[hi, 2] - b)
        zhi = minimum_filter(zhi, size=3, mode="constant", cval=1e9)
        has = np.zeros((nx, ny), bool); has[ix, iy] = True
        dz = 1.0
        L = np.arange(z_min, 30.0, dz)
        H = np.zeros((len(L), nx, ny))
        free = ~self.prot
        for k, zt in enumerate(L):
            sel = free & (c[:, 2] < zt)
            np.add.at(H[k], (ix[sel], iy[sel]), self.vol[sel])
        S = np.zeros((len(L), nx + 1, ny + 1)); S[:, 1:, 1:] = H.cumsum(1).cumsum(2)
        cands = []
        for w in range(2, nx):
            for h in range(2, ny):
                zt = swv(zhi, (w, h)).min(axis=(-2, -1))
                full = swv(has.astype(int), (w, h)).sum(axis=(-2, -1)) >= w * h      # todo el rectangulo con material
                # altura REAL: el techo a 45 grados sube desde la cara de apoyo (z = -1) hasta la mitad del lado menor;
                # no puede pasar de zt (material que trabaja encima) -> el lado menor no puede pasar de 2 (zt + 1) / tan + 3
                zr = np.minimum(zt, -1.0 + min(w, h) * b / 2.0 * am_t)
                k = np.floor((zr - z_min) / dz).astype(int)
                okm = full & (k >= 0)
                k = np.clip(k, 0, len(L) - 1)
                zt_eff = z_min + k * dz
                okm &= min(w, h) * b <= 2.0 * (np.minimum(zt, 30.0) + 1.0) / am_t + 3.0   # sin tramo de techo plano
                I, J = np.nonzero(okm)
                if not len(I):
                    continue
                kk = k[I, J]
                V = 0.5 * (S[kk, I + w, J + h] - S[kk, I, J + h] - S[kk, I + w, J] + S[kk, I, J])   # forma de tienda ~ 1/2 de la caja
                for q in np.argsort(-V)[:6]:
                    if V[q] >= v_min:
                        i, j = I[q], J[q]
                        cands.append(dict(x0=float(x0 + i * b), x1=float(x0 + (i + w) * b), y0=float(y0 + j * b),
                                          y1=float(y0 + (j + h) * b), zt=float(zt_eff[i, j]), V=float(V[q])))
        cands.sort(key=lambda d: -d["V"])
        sel = []
        for cd in cands:
            if veto and veto(dict(tipo="hueco", x0=cd["x0"], x1=cd["x1"], y0=cd["y0"], y1=cd["y1"], z0=-1.0, z1=cd["zt"])):
                continue
            if all(_rect_overlap(cd, q) < 0.2 for q in sel):
                sel.append(cd)
            if len(sel) >= n_max:
                break
        return sel

    def _open_slivers(self, cd, wall=5.0):
        """Si al lado de un rebaje solo quedaria una pared de menos de 'wall' mm hasta el borde de la pieza, el rebaje se
        abre hasta el borde: una lamina fina se carga y concentra la tension (y apenas pesa)."""
        c = self.cen
        up = c[:, 2] > cd["zc"]
        by = up & (c[:, 1] > cd["y0"]) & (c[:, 1] < cd["y1"])
        bx = up & (c[:, 0] > cd["x0"]) & (c[:, 0] < cd["x1"])
        for ax, band, lo, hi in ((0, by, "x0", "x1"), (1, bx, "y0", "y1")):
            out_hi = c[band & (c[:, ax] >= cd[hi]), ax]
            if out_hi.size and out_hi.max() - cd[hi] < wall:
                cd[hi] = float(out_hi.max() + 4.0)
            out_lo = c[band & (c[:, ax] <= cd[lo]), ax]
            if out_lo.size and cd[lo] - out_lo.min() < wall:
                cd[lo] = float(out_lo.min() - 4.0)
        return cd

    def cavities(self, tau, b=4.0, wall=4.0, n_max=4, v_min=1500.0, veto=None):
        """Huecos interiores (caja) en material ocioso, a >= 'wall' mm de cualquier superficie."""
        if self.surf is None:
            return []
        c = self.cen
        o = c.min(axis=0) - b
        idx = ((c - o) // b).astype(int)
        n = idx.max(axis=0) + 2
        mat = np.zeros(n, bool); bad = np.zeros(n, bool)
        mat[tuple(idx.T)] = True
        nb = ~self.low(tau) | self.prot
        bad[tuple(idx[nb].T)] = True
        sidx = ((self.surf - o) // b).astype(int)
        sidx = sidx[(sidx >= 0).all(1) & (sidx < n).all(1)]
        surf = np.zeros(n, bool); surf[tuple(sidx.T)] = True
        good = mat & ~bad & ~surf
        S = np.zeros(tuple(n + 1)); S[1:, 1:, 1:] = good.astype(float).cumsum(0).cumsum(1).cumsum(2)

        def boxsum(i, j, k, w, h, d):
            return (S[i + w, j + h, k + d] - S[i, j + h, k + d] - S[i + w, j, k + d] - S[i + w, j + h, k]
                    + S[i, j, k + d] + S[i, j + h, k] + S[i + w, j, k] - S[i, j, k])
        cands = []
        for w in (3, 4, 5, 6, 8, 10, 12, 15):
            for h in (3, 4, 5, 6, 8, 10, 12, 15, 20):
                for d in (2, 3, 4, 5, 6, 8):
                    if w > n[0] or h > n[1] or d > n[2]:
                        continue
                    I, J, K = np.meshgrid(np.arange(n[0] - w + 1), np.arange(n[1] - h + 1), np.arange(n[2] - d + 1), indexing="ij")
                    full = boxsum(I, J, K, w, h, d) >= w * h * d - 0.5
                    for i, j, k in zip(I[full][:200], J[full][:200], K[full][:200]):
                        cands.append(dict(x0=float(o[0] + i * b), x1=float(o[0] + (i + w) * b), y0=float(o[1] + j * b),
                                          y1=float(o[1] + (j + h) * b), z0=float(o[2] + k * b), z1=float(o[2] + (k + d) * b),
                                          V=float(w * h * d * b ** 3)))
        cands.sort(key=lambda q: -q["V"])
        sel, tr = [], cKDTree(self.surf)
        for cd in cands:
            if cd["V"] < v_min:
                break
            if any(_box_overlap(cd, s) > 0 for s in sel):
                continue
            if veto and veto(dict(tipo="hueco", **{k: cd[k] for k in ("x0", "x1", "y0", "y1", "z0", "z1")})):
                continue
            # distancia real a la superficie (nodos de la malla) >= wall en toda la caja
            gx, gy, gz = np.meshgrid(np.linspace(cd["x0"], cd["x1"], 6), np.linspace(cd["y0"], cd["y1"], 6),
                                     np.linspace(cd["z0"], cd["z1"], 4), indexing="ij")
            dd, _ = tr.query(np.c_[gx.ravel(), gy.ravel(), gz.ravel()])
            if dd.min() < wall:
                continue
            sel.append(cd)
            if len(sel) >= n_max:
                break
        return sel


def _rect_overlap(a, b):
    ix = max(0.0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])); iy = max(0.0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    return ix * iy / max((a["x1"] - a["x0"]) * (a["y1"] - a["y0"]), 1e-9)


def _box_overlap(a, b):
    ix = max(0.0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"])); iy = max(0.0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]))
    iz = max(0.0, min(a["z1"], b["z1"]) - max(a["z0"], b["z0"]))
    return ix * iy * iz


def from_npz(path, sig_lim=215.0, metrics=None, sym=False):
    d = np.load(path)
    if "tets4" not in d:
        raise ValueError("campos.npz sin tetraedros (calculado con una version anterior)")
    m = metrics or {}
    return Campo(d["nodes"], d["tets4"], d["vm"], d["tris"], sig_lim, m.get("vm_metric_xyz"), m.get("vm_metric"),
                 d["sig6"] if "sig6" in d else None, sym=sym)
