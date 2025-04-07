from libreria import *
import sys

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

        bins = math.ceil(math.sqrt(n))  # Número de intervalos para el histograma
        alpha = 0.05
        v = bins - 1  # Grados de libertad
        a, b = 0, 10  # valores por defecto para uniforme

        if opcion == "1":
            a = float(input("Ingrese el valor mínimo (a): "))
            b = float(input("Ingrese el valor máximo (b): "))
            data = generate_uniform(a, b, n)
            expected = expected_uniform_frequencies(a, b, n, bins)

        elif opcion == "2":
            mu = float(input("Ingrese la media (μ) (0 si la desconoce): "))
            sigma = float(input("Ingrese la desviación estándar (σ) (1 si la desconoce4): "))
            data = generate_normal(mu, sigma, n)
            a = min(data)
            b = max(data)
            expected = expected_uniform_frequencies(a, b, n, bins)

        elif opcion == "3":
            lambd = float(input("Ingrese el valor de λ: "))
            data = generate_exponential(lambd, n)
            a = min(data)
            b = max(data)
            expected = expected_uniform_frequencies(a, b, n, bins)

        elif opcion == "4":
            lambd = float(input("Ingrese el valor de λ: "))
            data = generate_poisson(lambd, n)
            a = min(data)
            b = max(data)
            expected = expected_uniform_frequencies(a, b, n, bins)

        else:
            print("Opción no válida. Intente de nuevo.")
            continue

        observed, _, _ = build_histogram(data, bins)
        chi2 = chi_square_test(observed, expected)

        print("\n--- Resultados ---")
        print("Frecuencias observadas:", observed)
        print("Frecuencias esperadas:", expected)
        print("Valor Chi-Cuadrado:", chi2)
        print("Grados de libertad:", v)

        valor_critico = float(input(f"Ingrese el valor crítico de Chi-Cuadrado (α={alpha}, gl={v}): "))
        if chi2 <= valor_critico:
            print("✅ No se puede rechazar H₀: los datos siguen la distribución esperada.")
        else:
            print("❌ Se rechaza H₀: los datos NO siguen la distribución esperada.")

if __name__ == "__main__":
    main()
