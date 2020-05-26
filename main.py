import csv
from math import log2
from itertools import combinations

def read(name):
    with open(name, newline="", encoding="utf-8-sig") as csvfile:
        csv_file = csv.reader(csvfile)
        return list(csv_file)


def h(p, q):
    if p == 0 and q == 0:
        return 0
    elif p == 0:
        return -q * log2(q)
    elif q == 0:
        return -p * log2(p)
    else:
        return -p * log2(p) - q * log2(q)


def freq(val, values):
    count = 0
    for ele in values:
        if val == ele:
            count += 1
    return count


def distancia_manhattan(v0, v1):
    d = 0
    for j, val in enumerate(v0):
        d += abs(int(val) - v1[j])
    return abs(d)


def distancia_euclidiana(v0, v1):
    d = 0
    for j, val in enumerate(v0):
        d += pow(int(val)-v1[j], 2)
    return abs(d)


def id3(name):
    data = read(name)

    # Create the value and freq lists
    values = []
    for _ in data[0]:
        values.append([])

    # Read and count data
    for row in data[1:]:
        for col, val in enumerate(row):
            if val in values[col]:
                i = values[col].index(val)
            else:
                values[col].append(val)

    posible_values = values[-1]

    # Read and count final results
    results = []

    # Insertamos una lista por cada columna
    for _ in values[:-1]:
        results.append([])

    # Insertamos una lista por cada valor distinto de la col
    for i in range(len(results)):
        for _ in range(len(values[i])):
            results[i].append([])

    # Insertamos una lista por cada resultado posible
    for i, col in enumerate(results):
        for j, pos in enumerate(col):
            for _ in range(len(posible_values)):
                results[i][j].append(0)

    # Contamos cuantas veces aparece cada resultado
    for i, row in enumerate(data[1:]):
        for j, col in enumerate(row[:-1]):
            val_i = values[j].index(col)
            res_i = values[-1].index(row[-1])

            results[j][val_i][res_i] += 1

    # Una lista por cada posible valor de id3
    id3 = []
    for _ in data[0]:
        id3.append([])

    # Creamos tabla de frecuencias
    freq = []
    for i in range(len(data[0])):
        freq.append([])
        for _ in range(len(values[i])):
            freq[i].append(0)

    # Calculamos las frecuencias
    for row in data[1:]:
        for i, col in enumerate(row):
            val_i = values[i].index(col)
            freq[i][val_i] += 1

    print()
    print("==========================================")
    print("Cuentas basicas ==========================")
    print("==========================================")
    print()

    # Print results in table
    for i, column in enumerate(results):
        print("{}".format(data[0][i]))
        for j, val in enumerate(values[i]):
            print("\tPara \"{}\", ".format(val), end=" ")
            for k, res in enumerate(posible_values):
                print("{} veces el \"{}\"".format(column[j][k], res), end="; ")
            print()

    print()
    print("==========================================")
    print("Calculo de la h ==========================")
    print("==========================================")
    print()

    hval = []
    for i, carac in enumerate(values[:-1]):
        print("H(X | {})".format(data[0][i]), end=" = ")
        res = 0
        for j, val in enumerate(carac):
            print("{}/{} * H({}/{}, {}/{})".format(
                freq[i][j],
                sum(freq[i]),
                results[i][j][0],
                sum(results[i][j]),
                results[i][j][1],
                sum(results[i][j])), end="")

            if j != len(carac) - 1:
                print(" + ", end="")

            res += freq[i][j] / sum(freq[i]) * h(results[i][j][0] / sum(results[i][j]),
                                                 results[i][j][1] / sum(results[i][j]))
        print(" = {:.4f} bits".format(res))


def c45(name, knn=None, userk=None):
    data = read(name)

    # Create the value and freq lists
    values = []
    for _ in data[0]:
        values.append([])

    # Read and count data
    for row in data[1:]:
        for col, val in enumerate(row):
            if val in values[col]:
                i = values[col].index(val)
            else:
                values[col].append(val)

    nu_values = []
    for i in range(len(values)):
        nu_values.append(sorted(values[i]))

    values = nu_values

    posible_values = values[-1]

    # Sacamos los limites
    limites = []
    for _ in range(len(data[0]) - 1):
        limites.append([])
    for i, carac in enumerate(values[:-1]):
        for value in carac[:-1]:
            limites[i].append(value)

    # Creamos la tabla de frecuencias
    freq = []
    for _ in range(len(data[0]) - 1):
        freq.append([])
    for i, part in enumerate(freq):
        for _ in range(len(limites[i]) * 2):
            freq[i].append([0, 0])

    # Calculamos los valores de las frecuencias
    for i, col in enumerate(data[1:]):
        for j, row in enumerate(col[:-1]):
            for k, lim in enumerate(limites[j]):
                res_i = posible_values.index(data[i + 1][-1])

                if row > lim:
                    freq[j][k * 2][res_i] += 1
                else:
                    freq[j][k * 2 + 1][res_i] += 1

    print()
    print("==========================================")
    print("Calculo de c4.5 ==========================")
    print("==========================================")
    print()

    # Imprimimos los datos
    for i, carac in enumerate(freq):
        for j, lim in enumerate(limites[i]):
            print("{}>{}:".format(data[0][i], lim))

            frecuencias = carac[j * 2:j * 2 + 2]

            print("\tRama verdadera: {} si; {} no".format(frecuencias[0][1], frecuencias[0][0]))
            print("\tRama falsa    : {} si; {} no".format(frecuencias[1][1], frecuencias[1][0]))

            total = len(data) - 1
            total_v = sum(carac[j * 2:j * 2 + 2][0])
            total_f = sum(carac[j * 2:j * 2 + 2][1])

            print("\tH(X | {}>{}) = {}/{} * H({}/{}, {}/{}) + {}/{} * H({}/{}, {}/{}) = ".format(
                data[0][i], lim,
                total_v, total,
                carac[j * 2:j * 2 + 2][0][1], total_v,
                carac[j * 2:j * 2 + 2][0][0], total_v,
                total_f, total,
                carac[j * 2:j * 2 + 2][1][1], total_f,
                carac[j * 2:j * 2 + 2][1][0], total_f,
            ), end="")

            res = total_v / total * h(carac[j * 2:j * 2 + 2][0][1]/total_v, carac[j * 2:j * 2 + 2][0][0]/total_v) \
                + total_f / total * h(carac[j * 2:j * 2 + 2][1][1]/total_f, carac[j * 2:j * 2 + 2][1][0]/total_f)

            print("{:.4f} bits".format(res))
            print("\tIG = 1 - {:.2f} = {:.2f}".format(res, 1 - res))

    if knn is not None and userk is not None:
        print()
        print("==========================================")
        print("Calculo de knn ===========================")
        print("==========================================")
        print()

        distances = []
        resultados = []
        min = None
        for i, row in enumerate(data[1:]):
            d = distancia_euclidiana(row[:-1], knn)
            distances.append(d)
            print(row, "| d^2 =", d)

if __name__ == "__main__":
    id3("examen2.csv")
    #c45("examen_last.csv", (1, -1), 3)
