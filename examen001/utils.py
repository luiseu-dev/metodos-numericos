"""Utilidades comunes: error relativo, búsqueda de intervalo, resultado y tablas."""
import math
from dataclasses import dataclass, field


@dataclass
class Resultado:
    """Salida uniforme de cada método numérico."""
    nombre: str
    raiz: float
    filas: list = field(default_factory=list)
    evaluaciones: int = 0       # nº de evaluaciones de f y f' (costo real)
    convergio: bool = False

    @property
    def iteraciones(self):
        return len(self.filas)


def error_rel(nuevo, viejo):
    """Error relativo aproximado en %: |(x_nuevo - x_viejo) / x_nuevo| * 100."""
    if nuevo == 0:
        return math.inf
    return abs((nuevo - viejo) / nuevo) * 100


def buscar_intervalo(f, inicio, fin, paso=1.0):
    """Primer subintervalo [x, x + paso] dentro de [inicio, fin] con cambio de signo."""
    x = inicio
    fx = f(x)
    while x < fin:
        x_sig = min(x + paso, fin)
        fx_sig = f(x_sig)
        if fx * fx_sig <= 0:
            return x, x_sig
        x, fx = x_sig, fx_sig
    raise ValueError(f"No hay cambio de signo de f en [{inicio}, {fin}] con paso {paso}")


def imprimir_tabla(titulo, encabezados, filas):
    print(f"\n{titulo}")
    print(" | ".join(f"{e:>10}" for e in encabezados))
    print("-" * (13 * len(encabezados)))
    for fila in filas:
        celdas = [f"{fila[0]:>10d}"]
        for v in fila[1:]:
            celdas.append(f"{'---':>10}" if v is None else f"{v:>10.6f}")
        print(" | ".join(celdas))


def imprimir_resultado(res, unidad="m"):
    estado = "" if res.convergio else "  (¡NO convergió en el máximo de iteraciones!)"
    print(f"   h ≈ {res.raiz:.6f} {unidad} en {res.iteraciones} iteraciones "
          f"({res.evaluaciones} evaluaciones de función){estado}")


ENCABEZADOS_CERRADO = ["Iter", "a", "b", "c", "f(a)", "f(c)", "Error (%)"]
