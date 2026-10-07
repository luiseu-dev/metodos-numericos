"""D) Método de Newton-Raphson."""
from problema import f, df, TOL, MAX_ITER, H0, DOMINIO
from utils import Resultado, error_rel, imprimir_tabla, imprimir_resultado

ENCABEZADOS_NR = ["Iter", "h_i", "f(h_i)", "f'(h_i)", "h_i+1", "Error (%)"]
EPS_DERIVADA = 1e-12


def newton_raphson(h, tol=TOL, max_iter=MAX_ITER):
    res = Resultado("Newton-Raphson", h)
    evals = 0
    for i in range(1, max_iter + 1):
        fh, dfh = f(h), df(h)
        evals += 2
        if abs(dfh) < EPS_DERIVADA:
            raise ZeroDivisionError(f"f'(h) ≈ 0 en h = {h}, elija otra semilla")
        h_sig = h - fh / dfh
        if not DOMINIO[0] <= h_sig <= DOMINIO[1]:
            raise ValueError(f"h = {h_sig:.6f} sale del dominio físico {DOMINIO}, elija otra semilla")
        err = error_rel(h_sig, h)
        res.filas.append((i, h, fh, dfh, h_sig, err))
        h = h_sig
        if err < tol:
            res.convergio = True
            break
    res.raiz, res.evaluaciones = h, evals
    return res


if __name__ == "__main__":
    res = newton_raphson(H0)
    imprimir_tabla(f"D) Método de Newton-Raphson (h0 = {H0})", ENCABEZADOS_NR, res.filas)
    imprimir_resultado(res)
