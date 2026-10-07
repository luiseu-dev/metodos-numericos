"""
A) Planteamiento - Tanque esférico (R = 3 m, V = 30 m^3)

Volumen de un casquete esférico:  V = pi * h^2 * (3R - h) / 3
    f(h)   = pi * h^2 * (9 - h) / 3 - 30 = 0
    f'(h)  = pi * h * (6 - h)
    f''(h) = pi * (6 - 2h)
Dominio físico: 0 <= h <= 2R = 6. Como f'(h) > 0 en (0, 6), f es estrictamente
creciente: f(0) = -30 < 0 y f(6) = 36*pi - 30 > 0  =>  existe una ÚNICA raíz física.
"""
import math

from utils import buscar_intervalo

R = 3.0
V = 30.0
TOL = 0.5           # criterio de parada: error relativo aproximado < 0.5 %
MAX_ITER = 100
DOMINIO = (0.0, 2 * R)


def f(h):
    return math.pi * h**2 * (3 * R - h) / 3 - V


def df(h):
    return math.pi * h * (2 * R - h)


def d2f(h):
    return math.pi * (2 * R - 2 * h)


# Intervalo inicial: primer subintervalo de longitud 1 con cambio de signo -> [2, 3]
A0, B0 = buscar_intervalo(f, *DOMINIO, paso=1.0)
H0 = B0             # semilla para Newton-Raphson (extremo derecho del intervalo)
