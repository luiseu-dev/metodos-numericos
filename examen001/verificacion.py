"""
Verificación independiente con NumPy/SciPy y análisis de convergencia.

- Raíz "exacta" de referencia: raíces del polinomio cúbico (NumPy) y Brent (SciPy).
- Error verdadero de cada método respecto a la referencia.
- Orden de convergencia empírico p: pendiente de log(e_{k+1}) frente a log(e_k).
- Experimento con tolerancia estricta para ver el comportamiento asintótico.
"""
import math

import numpy as np
from scipy import optimize

from problema import f, df, R, V, DOMINIO, A0, B0, H0
from biseccion import biseccion
from interpolacion_lineal import interpolacion_lineal
from newton_raphson import newton_raphson

TOL_ESTRICTA = 1e-10    # % (≈ 1e-12 relativo, cerca de la precisión de double)


def raiz_referencia():
    # pi*h^2*(3R - h)/3 - V = -(pi/3) h^3 + pi*R h^2 - V
    coef = [-math.pi / 3, math.pi * R, 0.0, -V]
    raices = np.roots(coef)
    reales = [r.real for r in raices if abs(r.imag) < 1e-12 and DOMINIO[0] <= r.real <= DOMINIO[1]]
    r_poly = reales[0]
    r_brent = optimize.brentq(f, A0, B0, xtol=1e-15, rtol=4 * np.finfo(float).eps)
    r_newton = optimize.newton(f, H0, fprime=df, tol=1e-15)
    return r_poly, r_brent, r_newton


def iterados(res):
    """Sucesión de aproximaciones generada por el método."""
    col = 4 if res.nombre == "Newton-Raphson" else 3
    return [fila[col] for fila in res.filas]


def orden_convergencia(xs, raiz, piso=1e-13):
    """Pendiente de la regresión log(e_{k+1}) vs log(e_k): robusta frente a errores no monótonos."""
    e = np.array([abs(x - raiz) for x in xs])
    e = e[e > piso]
    if len(e) < 3:
        return float("nan")
    p, _ = np.polyfit(np.log(e[:-1]), np.log(e[1:]), 1)
    return p


def ejecutar_metodos(tol):
    return [biseccion(A0, B0, tol=tol), interpolacion_lineal(A0, B0, tol=tol), newton_raphson(H0, tol=tol)]


def graficar(resultados, raiz, archivo="convergencia.png"):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return None
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for res in resultados:
        err = [max(abs(x - raiz) / raiz * 100, 1e-16) for x in iterados(res)]
        ax.semilogy(range(1, len(err) + 1), err, marker="o", ms=4, label=res.nombre)
    ax.axhline(0.5, color="gray", ls="--", lw=1, label="Criterio 0.5 %")
    ax.set_xlabel("Iteración")
    ax.set_ylabel("Error relativo verdadero (%)")
    ax.set_title("Convergencia hacia h* (tanque esférico, V = 30 m³)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(archivo, dpi=150)
    plt.close(fig)
    return archivo
