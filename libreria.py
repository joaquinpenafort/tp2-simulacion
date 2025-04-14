import random
import math

# ------------------------------------------------------
# Distribución Uniforme
# ------------------------------------------------------
# Genera n valores aleatorios con distribución uniforme continua en el intervalo [a, b].
# Fórmula: X = a + (b - a) * U, donde U ~ U(0,1)
# Esto se basa en la transformación directa de un número uniforme en el rango deseado.
def generate_uniform(a, b, n):
    return [a + (b - a) * random.random() for _ in range(n)]

# ------------------------------------------------------
# Distribución Exponencial
# ------------------------------------------------------
# Genera n valores aleatorios usando el método de la transformada inversa.
# La función de distribución acumulada (CDF) de la exponencial es:
#     F(x) = 1 - e^(-λx)   para x >= 0
# Su inversa es:
#     F⁻¹(u) = -ln(1 - u) / λ
# Donde u ~ U(0,1). Esta fórmula se aplica directamente aquí.
def generate_exponential(lambd, n):
    return [-(1 / lambd) * math.log(1 - random.random()) for _ in range(n)]

# ------------------------------------------------------
# Distribución de Poisson
# ------------------------------------------------------
# Genera n valores usando el algoritmo de Knuth (no es transformada inversa).
# Este método simula el número de eventos que ocurren en un intervalo dado
# usando una cadena de multiplicaciones de valores uniformes hasta alcanzar
# una cota basada en e^(-λ). Es eficiente para valores pequeños o moderados de λ.
def generate_poisson(lambd, n):
    values = []
    for _ in range(n):
        L = math.exp(-lambd)
        k = 0
        p = 1
        while p > L:
            k += 1
            p *= random.random()
        values.append(k - 1)
    return values

# ------------------------------------------------------
# Distribución Normal (Gaussiana)
# ------------------------------------------------------
# Genera n valores usando el método Box-Muller.
# Este método transforma dos variables U1, U2 ~ U(0,1) en dos variables normales estándar:
#     Z1 = sqrt(-2 ln U1) * cos(2π U2)
#     Z2 = sqrt(-2 ln U1) * sin(2π U2)
# Luego se ajustan con media y desvío estándar deseados:
#     X = μ + σZ
# Este método es eficiente y no requiere la inversa de la CDF normal (que no tiene forma cerrada).
def generate_normal(mu, sigma, n):
    values = []
    for _ in range(n // 2):  # genera dos valores por iteración
        u1 = random.random()
        u2 = random.random()
        z1 = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        z2 = math.sqrt(-2 * math.log(u1)) * math.sin(2 * math.pi * u2)
        values.extend([mu + sigma * z1, mu + sigma * z2])
    if n % 2:
        u1 = random.random()
        u2 = random.random()
        z = math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)
        values.append(mu + sigma * z)
    return values

# ------------------------------------------------------
# Prueba de Bondad de Ajuste: Ji-Cuadrado (Chi-Square)
# ------------------------------------------------------
# Esta función compara la distribución de frecuencias observadas con las esperadas para
# determinar si los datos generados siguen la distribución esperada.
# Se usa principalmente para variables discretas o para histogramas de variables continuas.
def chi_square_test(observed, expected):
    chi2 = 0
    for o, e in zip(observed, expected):
        if e > 0:
            chi2 += ((o - e) ** 2) / e
    return chi2

# ------------------------------------------------------
# Construir Histograma
# ------------------------------------------------------
# Divide los datos en una cantidad dada de intervalos y devuelve las frecuencias por intervalo.
def build_histogram(data, bins, min_val=None, max_val=None):
    if min_val is None:
        min_val = min(data)
    if max_val is None:
        max_val = max(data)
    width = (max_val - min_val) / bins
    frequencies = [0] * bins
    for value in data:
        index = int((value - min_val) / width)
        if index == bins:  # para valores en el borde superior
            index -= 1
        frequencies[index] += 1
    return frequencies, min_val, width




