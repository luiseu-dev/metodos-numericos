"""
Proyecto: Aplicación de Métodos Numéricos - Tanque esférico
Universidad Monteávila - Prof. Boris Bossio

Ejecuta los tres métodos, la verificación con NumPy/SciPy y la conclusión (E).
"""
from problema import f, df, d2f, TOL, A0, B0, H0
from utils import imprimir_tabla, imprimir_resultado, ENCABEZADOS_CERRADO
from biseccion import biseccion
from interpolacion_lineal import interpolacion_lineal
from newton_raphson import newton_raphson, ENCABEZADOS_NR
from verificacion import (raiz_referencia, iterados, orden_convergencia, ejecutar_metodos,
                          graficar, TOL_ESTRICTA)


def main():
    print("A) f(h) = pi*h^2*(9 - h)/3 - 30 = 0")
    print("   f'(h) = pi*h*(6 - h)   (> 0 en 0 < h < 6  =>  raíz única en el dominio físico)")
    print(f"   Intervalo inicial [{A0}, {B0}]: f(a) = {f(A0):.4f}, f(b) = {f(B0):.4f}")

    bis = biseccion(A0, B0)
    imprimir_tabla("B) Método de Bisección", ENCABEZADOS_CERRADO, bis.filas)
    imprimir_resultado(bis)

    fp = interpolacion_lineal(A0, B0)
    imprimir_tabla("C) Método de Interpolación Lineal (Falsa Posición)", ENCABEZADOS_CERRADO, fp.filas)
    imprimir_resultado(fp)

    nr = newton_raphson(H0)
    imprimir_tabla(f"D) Método de Newton-Raphson (h0 = {H0})", ENCABEZADOS_NR, nr.filas)
    imprimir_resultado(nr)

    # ---------------- Verificación independiente ----------------
    r_poly, r_brent, r_scipy_nr = raiz_referencia()
    raiz = r_brent
    print("\nVerificación (NumPy / SciPy)")
    print(f"   numpy.roots (cúbica)     : h* = {r_poly:.12f}")
    print(f"   scipy.optimize.brentq    : h* = {r_brent:.12f}")
    print(f"   scipy.optimize.newton    : h* = {r_scipy_nr:.12f}")

    resultados = [bis, fp, nr]
    print(f"\n   {'Método':<22}{'Iter':>6}{'Evals f':>9}{'h aprox':>12}{'Err. verdadero (%)':>21}")
    for res in resultados:
        ev = abs(res.raiz - raiz) / raiz * 100
        print(f"   {res.nombre:<22}{res.iteraciones:>6}{res.evaluaciones:>9}{res.raiz:>12.6f}{ev:>21.2e}")

    # ---------------- Comportamiento asintótico ----------------
    estrictos = ejecutar_metodos(TOL_ESTRICTA)
    print(f"\n   Con tolerancia estricta ({TOL_ESTRICTA:g} %), comportamiento asintótico:")
    print(f"   {'Método':<22}{'Iter':>6}{'Evals f':>9}{'Orden p empírico':>19}")
    for res in estrictos:
        p = orden_convergencia(iterados(res), raiz)
        print(f"   {res.nombre:<22}{res.iteraciones:>6}{res.evaluaciones:>9}{p:>19.2f}")
    png = graficar(estrictos, raiz)
    if png:
        print(f"   Gráfica de convergencia guardada en: {png}")

    # ---------------- E) Conclusión ----------------
    mejor_iter = min(resultados, key=lambda r: (r.iteraciones, r.evaluaciones))
    mejor_asint = min(estrictos, key=lambda r: r.evaluaciones)
    extremo_fijo = len({fila[2] for fila in fp.filas}) == 1 or len({fila[1] for fila in fp.filas}) == 1
    n_bis, n_fp, n_nr = (r.iteraciones for r in resultados)

    print("\nE) Conclusión")
    for res in resultados:
        print(f"   {res.nombre:<22}: {res.iteraciones} iteraciones, {res.evaluaciones} evaluaciones")
    print(f"""
   Con el criterio exigido (Error < {TOL} %), el método más eficiente fue
   {mejor_iter.nombre} ({mejor_iter.iteraciones} iteraciones, {mejor_iter.evaluaciones} evaluaciones de función).

   ¿Por qué? La raíz (h* ≈ {raiz:.4f}) está muy cerca de a = {A0} (|f(a)| = {abs(f(A0)):.3f}
   frente a f(b) = {f(B0):.2f}) y en [{A0}, {B0}] la curvatura es pequeña (f'' ≤ {d2f(A0):.2f} frente a f' ≈ {df(raiz):.1f}),
   así que la recta secante cae prácticamente sobre la raíz desde la 1ª iteración;
   la 2ª solo confirma que el error aproximado ya es < {TOL} %.
   Bisección ({n_bis} it.) ignora los valores de f y solo divide el intervalo a la
   mitad: convergencia lineal con razón 1/2, independiente de la forma de f.
   Newton-Raphson ({n_nr} it.) arrancó en h0 = {H0}, lejos de la raíz, y además su
   criterio de parada necesita una iteración extra para comparar iterados.""")
    if extremo_fijo:
        print(f"""   Nota: como f''(h) > 0 en el intervalo, la Falsa Posición mantiene un extremo
   fijo (b = {B0}) y su convergencia es solo LINEAL.""")
    print(f"""
   Sin embargo, la eficiencia real se mide asintóticamente: con tolerancia
   {TOL_ESTRICTA:g} % el más eficiente es {mejor_asint.nombre} (convergencia cuadrática, p ≈ 2:
   los dígitos correctos se duplican en cada paso), mientras que Bisección y
   Falsa Posición convergen linealmente (p ≈ 1).
   => Para este problema con 0.5 % gana {mejor_iter.nombre}; como método general,
      con f'(h) analítica disponible y una semilla razonable, Newton-Raphson es el
      más eficiente, y Bisección el más robusto (convergencia garantizada).

   Profundidad del agua para V = 30 m^3:  h ≈ {raiz:.4f} m""")


if __name__ == "__main__":
    main()
