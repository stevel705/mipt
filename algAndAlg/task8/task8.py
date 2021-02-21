# Задание 8: Разрез минимальной плотности
from collections import defaultdict
import numpy as np
from numpy import linalg


def valency(adj_matrix):
    n = adj_matrix.shape[0]   
    valency = np.zeros((n, n))   
    for i in range(n):
        for j in range(n):
            if adj_matrix[i][j] == 1:
                valency[i][i] += 1
            else:
                continue    
    return valency

def laplacian(adj_matrix):
    return valency(adj_matrix) - adj_matrix

def slice_score(graph, v1, v2):
    cut_size = sum(sum(1 for x in graph[i] if x in v2) for i in v1)
    density = cut_size / (len(v1) * len(major))
    return density

def density(v1, v2, adjacency_matrix):
    connections = 0
    for x in v1:
        for y in v2:
            connections += adjacency_matrix[x, y]
    return connections / (len(v1) * len(v2))

def main():
    n = int(input())
    vert_ = {}
    # Получаем матрицу Лапласа
    vertexs = defaultdict(list)
    count = 0
    for i in range(n):
        v1, v2 = [int(i) for i in input().split(' ')]
        vertexs[v1].append(v2)

        if v1 not in vert_:
            vert_[v1] = count
            count += 1
        if v2 not in vert_:
            vert_[v2] = count
            count += 1

    length = len(vert_)
    matrix = np.zeros((length, length))
    for i in vertexs.keys():
        for j in vertexs[i]:
                matrix[i, j] = 1
                matrix[j, i] = 1
    
    laplacian_matrix = laplacian(matrix)
    # Ищем собственный вектор соответствующий lambda_2
    w, v = linalg.eigh(laplacian_matrix)
    vector_2 = v[:, 1]
    
    # Ищем плотность
    vertex_indexes = np.arange(matrix.shape[0])
    vertex_indexes = vertex_indexes[np.argsort(vector_2)]
    print(vertex_indexes)

    output = []
    for k in range(1, len(vertex_indexes)):
        v1, v2 = vertex_indexes[:k], vertex_indexes[k:]
        dens = density(v1, v2, matrix)
        output.append([dens, [v1, v2]])
    
    output = [[k[0], list(sorted(k[1], key=lambda x: len(x))[0])] for k in output]
    # сортируем по плотности и если плотность равна, тогда лексиграфически по массиву вершин
    output = sorted(output, key=lambda x: (x[0], x[1]))
    print(output[0][1][0])

    # print(output)
if __name__ == "__main__":
    main()