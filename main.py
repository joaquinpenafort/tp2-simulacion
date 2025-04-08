from libreria import *
import sys
import math
import scipy.stats as stats  # Necesario para las funciones de distribución

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

        n = int(input("Ingrese el número de datos a generar: "))
        alpha = 0.05

        if opcion == "1":
            a = float(input("Ingrese el valor mínimo (a): "))
            b = float(input("Ingrese el valor máximo (b): "))
            data = generate_uniform(a, b, n)
            bins = math.ceil(math.sqrt(n))
            expected = expected_uniform_frequencies(a, b, n, bins)

        elif opcion == "2":
            mu = float(input("Ingrese la media (μ) (0 si la desconoce): "))
            sigma = float(input("Ingrese la desviación estándar (σ) (1 si la desconoce): "))
            data = generate_normal(mu, sigma, n)
            a = min(data)
            b = max(data)
            bins = math.ceil(math.sqrt(n))
            expected = expected_normal_frequencies(mu, sigma, n, bins, a, b)

        elif opcion == "3":
            lambd = float(input("Ingrese el valor de λ: "))
            data = generate_exponential(lambd, n)
            a = min(data)
            b = max(data)
            bins = math.ceil(math.sqrt(n))
            expected = expected_exponential_frequencies(lambd, n, bins, a, b)

        elif opcion == "4":
            lambd = float(input("Ingrese el valor de λ: "))
            data = generate_poisson(lambd, n)
            a = int(min(data))
            b = int(max(data))
            bins = b - a + 1
            expected = expected_poisson_frequencies(lambd, n, bins, a)

        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        # Convertir a float nativo
        expected = [float(x) for x in expected]

        observed, _, _ = build_histogram(data, bins, a, b if opcion != "4" else b + 1)
        chi2 = chi_square_test(observed, expected)
        v = bins - 1  # Grados de libertad

        print("\n--- Resultados ---")
        print("Frecuencias observadas:", observed)
        print("Frecuencias esperadas:", [round(e, 2) for e in expected])
        print("Valor Chi-Cuadrado:", round(chi2, 4))
        print("Grados de libertad:", v)

        valor_critico = float(input(f"Ingrese el valor crítico de Chi-Cuadrado (α={alpha}, gl={v}): "))
        if chi2 <= valor_critico:
            print("✅ No se puede rechazar H₀: los datos siguen la distribución esperada.")
        else:
            print("❌ Se rechaza H₀: los datos NO siguen la distribución esperada.")

if __name__ == "__main__":
    main()
