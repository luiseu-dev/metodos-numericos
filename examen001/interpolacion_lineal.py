"""C) Método de Interpolación Lineal (Falsa Posición / Regula Falsi)."""
from problema import f, TOL, MAX_ITER, A0, B0
from utils import Resultado, error_rel, imprimir_tabla, imprimir_resultado, ENCABEZADOS_CERRADO


def interpolacion_lineal(a, b, tol=TOL, max_iter=MAX_ITER):
    fa, fb = f(a), f(b)
    evals = 2
    if fa * fb > 0:
        raise ValueError("f(a) y f(b) deben tener signos opuestos")
    res = Resultado("Interpolación Lineal", a)
    c_ant = None
    for i in range(1, max_iter + 1):
        c = b - fb * (a - b) / (fa - fb)
        fc = f(c)
        evals += 1
        err = None if c_ant is None else error_rel(c, c_ant)
        res.filas.append((i, a, b, c, fa, fc, err))
        if fc == 0 or (err is not None and err < tol):
            res.convergio = True
            break
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
        c_ant = c
    res.raiz, res.evaluaciones = c, evals
    return res


if __name__ == "__main__":
    res = interpolacion_lineal(A0, B0)
    imprimir_tabla("C) Método de Interpolación Lineal (Falsa Posición)", ENCABEZADOS_CERRADO, res.filas)
    imprimir_resultado(res)
