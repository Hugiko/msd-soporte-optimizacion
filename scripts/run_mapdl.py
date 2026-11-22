"""Lanzador de MAPDL en batch con timeout y progreso en consola.

Uso: python run_mapdl.py <carpeta> <entrada.inp> [--timeout 600] [--np 2] [--job file]
- Ejecuta MAPDL sin ventanas (-b), producto de licencia Student 'ansys'.
- Muestra en consola las fases del .out en tiempo real y las copia a progreso.log.
- Si supera el timeout, mata SOLO el arbol de procesos que ha lanzado (taskkill /T /PID).
"""
import argparse, os, subprocess, sys, time, datetime, re

MAPDL = r"C:\Program Files\ANSYS Inc\ANSYS Student\v261\ansys\bin\winx64\MAPDL.exe"
LICENSE_PRODUCT = "ansys"

# Lineas del .out que merece la pena mostrar como progreso
PATTERNS = [
    (re.compile(r"\*\*\*\*\* ROUTINE COMPLETED|ENTERING THE|/PREP7|/SOLU|/POST1", re.I), "fase"),
    (re.compile(r"NUMBER OF ELEMENTS|NUMBER OF NODES|Number of total nodes|Number of total elements", re.I), "malla"),
    (re.compile(r"SOLUTION IS DONE|EQUATION SOLVER|Sparse|PCG", re.I), "solver"),
    (re.compile(r"\*\*\* ERROR|LICENSE MANAGER ERROR|\*\*\* WARNING", re.I), "AVISO"),
]


def log(msg, logfile=None):
    line = f"[{datetime.datetime.now():%H:%M:%S}] {msg}"
    print(line, flush=True)
    if logfile:
        with open(logfile, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def run(workdir, inp, timeout=600, np_=2, job="file", out="solve.out", logfile=None):
    """Devuelve dict con estado: ok / timeout / error, tiempo y codigo."""
    workdir = os.path.abspath(workdir)
    logfile = logfile or os.path.join(workdir, "progreso.log")
    outpath = os.path.join(workdir, out)
    for stale in (os.path.join(workdir, f"{job}.lock"),):
        if os.path.exists(stale):
            try:
                os.remove(stale)
            except OSError:
                pass
    cmd = [MAPDL, "-b", "-p", LICENSE_PRODUCT, "-np", str(np_), "-j", job,
           "-i", inp, "-o", out, "-smp"]
    log(f"Lanzando MAPDL: {inp} (timeout {timeout}s)", logfile)
    t0 = time.time()
    flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    p = subprocess.Popen(cmd, cwd=workdir, creationflags=flags,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pos, status = 0, None
    while True:
        rc = p.poll()
        if os.path.exists(outpath):
            with open(outpath, "r", errors="ignore") as f:
                f.seek(pos)
                chunk = f.read()
                pos = f.tell()
            for ln in chunk.splitlines():
                for rx, tag in PATTERNS:
                    if rx.search(ln):
                        log(f"  [{tag}] {ln.strip()[:110]}", logfile)
                        break
        if rc is not None:
            status = "ok" if rc in (0, 8) else "error"  # 8 = terminado con avisos
            break
        if time.time() - t0 > timeout:
            log(f"  TIMEOUT tras {timeout}s: matando arbol de procesos PID {p.pid}", logfile)
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            status = "timeout"
            break
        time.sleep(1.0)
    dt = time.time() - t0
    if status != "ok" and os.path.exists(outpath):
        txt = open(outpath, errors="ignore").read()
        if "license not available" in txt.lower() or "licensed number" in txt.lower():
            status = "license"    # licencia ocupada (p. ej. Workbench abierto): no es un fallo del diseno
    log(f"MAPDL termino: estado={status} codigo={p.returncode} tiempo={dt:.1f}s", logfile)
    return {"status": status, "returncode": p.returncode, "seconds": dt}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("workdir")
    ap.add_argument("inp")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--np", type=int, default=2)
    ap.add_argument("--job", default="file")
    a = ap.parse_args()
    r = run(a.workdir, a.inp, a.timeout, a.np, a.job)
    sys.exit(0 if r["status"] == "ok" else 1)
