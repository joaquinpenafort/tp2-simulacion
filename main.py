from libreria import *
import sys
import math
import scipy.stats as stats
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference


def expected_uniform_frequencies(a, b, n, bins):
    return [n / bins] * bins

def expected_normal_frequencies(mu, sigma, n, bins, min_val, max_val):
    width = (max_val - min_val) / bins
    expected = []
    for i in range(bins):
        a = min_val + i * width
        b = a + width
        prob = stats.norm.cdf(b, mu, sigma) - stats.norm.cdf(a, mu, sigma)
        expected.append(n * prob)
    return expected

def expected_exponential_frequencies(lambd, n, bins, min_val, max_val):
    width = (max_val - min_val) / bins
    expected = []
    for i in range(bins):
        a = min_val + i * width
        b = a + width
        prob = stats.expon.cdf(b, scale=1/lambd) - stats.expon.cdf(a, scale=1/lambd)
        expected.append(n * prob)
    return expected

def expected_poisson_frequencies(lambd, n, bins, min_val):
    expected = []
    for k in range(min_val, min_val + bins):
        prob = stats.poisson.pmf(k, lambd)
        expected.append(n * prob)
    return expected

def main():
    while True:
        print("\n--- Generador de Distribuciones Aleatorias ---")
        print("1. Distribución Uniforme")
        print("2. Distribución Normal")
        print("3. Distribución Exponencial")
        print("4. Distribución de Poisson")
        print("5. Salir")

        opcion = input("Seleccione una opción (1-5): ")

        if opcion == "5":
            print("¡Hasta luego!")
            sys.exit()

        try:
            n = int(input("Ingrese el número de datos a generar: "))
            if n <= 0:
                print("❌ El número de datos debe ser mayor que 0.")
                continue

            intervalos = int(input("Ingrese la cantidad de intervalos que desea (0 si desea omitir, se usará √n):"))
            if intervalos < 0:
                print("❌ La cantidad de intervalos no puede ser negativa.")
                continue
        except ValueError:
            print("❌ Entrada inválida. Ingrese valores numéricos.")
            continue

        alpha = float(input("Ingrese el nivel de significancia (α): "))
        while alpha < 0:
            print("Alpha no puede ser negativo, ingreselo nuevamente")
            alpha = float(input("Ingrese el nivel de significancia (α): "))



        if opcion == "1":
            try:
                a = float(input("Ingrese el valor mínimo (a): "))
                b = float(input("Ingrese el valor máximo (b): "))
                if b <= a:
                    print("❌ El valor máximo debe ser mayor que el valor mínimo.")
                    continue
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            data = generate_uniform(a, b, n)
            bins = math.ceil(math.sqrt(n)) if intervalos == 0 else intervalos
            expected = expected_uniform_frequencies(a, b, n, bins)

        elif opcion == "2":
            try:
                mu = float(input("Ingrese la media (μ) (0 si la desconoce): "))
                sigma = float(input("Ingrese la desviación estándar (σ) (1 si la desconoce): "))
                if sigma <= 0:
                    print("❌ La desviación estándar debe ser mayor que 0.")
                    continue
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            data = generate_normal(mu, sigma, n)
            a = min(data)
            b = max(data)
            bins = math.ceil(math.sqrt(n)) if intervalos == 0 else intervalos
            expected = expected_normal_frequencies(mu, sigma, n, bins, a, b)

        elif opcion == "3":
            try:
                lambd = float(input("Ingrese el valor de λ: "))
                if lambd <= 0:
                    print("❌ λ debe ser mayor que 0.")
                    continue
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            data = generate_exponential(lambd, n)
            a = min(data)
            b = max(data)
            bins = math.ceil(math.sqrt(n)) if intervalos == 0 else intervalos
            expected = expected_exponential_frequencies(lambd, n, bins, a, b)

        elif opcion == "4":
            try:
                lambd = float(input("Ingrese el valor de λ: "))
                if lambd <= 0:
                    print("❌ λ debe ser mayor que 0.")
                    continue
            except ValueError:
                print("❌ Entrada inválida.")
                continue

            data = generate_poisson(lambd, n)
            a = int(min(data))
            b = int(max(data))
            bins = b - a + 1 if intervalos == 0 else intervalos
            expected = expected_poisson_frequencies(lambd, n, bins, a)

        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        expected = [float(x) for x in expected]

        observed, _, _ = build_histogram(data, bins, a, b if opcion != "4" else b + 1)
        chi2 = chi_square_test(observed, expected)
        v = bins - 1  # Grados de libertad

        print("\n--- Resultados ---")
        print("Frecuencias observadas:", observed)
        print("Frecuencias esperadas:", [round(e, 2) for e in expected])
        print("Valor Chi-Cuadrado:", round(chi2, 4))
        print("Grados de libertad:", v)

        try:
            valor_critico = float(input(f"Ingrese el valor crítico de Chi-Cuadrado (α={alpha}, gl={v}): "))
        except ValueError:
            print("❌ Entrada inválida para el valor crítico.")
            continue

        if chi2 <= valor_critico:
            print("✅ No se puede rechazar H₀: los datos siguen la distribución esperada.")
        else:
            print("❌ Se rechaza H₀: los datos NO siguen la distribución esperada.")

        # -------------------------------
        # Exportar a Excel con gráfico
        # -------------------------------
        nombre_archivo = input("Ingrese el nombre del archivo Excel de salida (ej. salida.xlsx): ")
        wb = Workbook()
        ws = wb.active
        ws.title = "Distribución"

        ws.append(["Bin / Valor", "Frecuencia Observada", "Frecuencia Esperada"])
        for i in range(len(observed)):
            label = (
                f"[{round(a + i * (b - a)/bins, 2)}, {round(a + (i + 1) * (b - a)/bins, 2)})"
                if opcion != "4" else str(a + i)
            )
            ws.append([label, observed[i], round(expected[i], 2)])

        chart = BarChart()
        chart.title = "Frecuencias Observadas vs Esperadas"
        chart.x_axis.title = "Intervalo"
        chart.y_axis.title = "Frecuencia"
        chart.type = "col"
        chart.style = 10
        chart.width = 20
        chart.height = 10

        data = Reference(ws, min_col=2, max_col=3, min_row=1, max_row=len(observed)+1)
        cats = Reference(ws, min_col=1, min_row=2, max_row=len(observed)+1)
        chart.add_data(data, titles_from_data=True)
        chart.set_categories(cats)
        ws.add_chart(chart, "E2")

        wb.save(nombre_archivo+".xlsx")
        print(f"📊 Archivo con gráfico guardado como: {nombre_archivo}")

if __name__ == "__main__":
    main()
