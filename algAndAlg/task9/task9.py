# Задание 9: Вершинное покрытие графа

# Реализуйте приближённый алгоритм поиска минимального взвешенного вершинного покрытия графа 
# (ошибающийся по весу не более чем вдвое). Можно использовать как схему «решаем задачу ЛП и округляем»,
# так и алгоритм, не прибегающий явно к линейному программированию (хотя для обоснования качества решения, 
# получаемого этим алгоритмом, мы применяли теорему двойственности).

# На вход программы подаются веса вершин и рёбра в виде:

import random 

num_vertex = int(input())

weight_vertex = [int(input()) for _ in range(num_vertex)]

num_edges = int(input())

edges = [[int(i) for i in input().split(' ')] for _ in range(num_edges)]

for v1, v2 in edges[::-1]:
    # if weight_vertex[v1] * weight_vertex[v2] != 0:
        y_e = min(weight_vertex[v1], weight_vertex[v2])
        weight_vertex[v1] -= y_e
        weight_vertex[v2] -= y_e

output = [i for i, k in enumerate(weight_vertex) if k == 0]
print(*output)