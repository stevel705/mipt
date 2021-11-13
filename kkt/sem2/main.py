# Задача 
# https://acm.timus.ru/problem.aspx?space=1&num=1421

# INPUT 
# 4
# 267 157 188 259
# 193 320 346 12

# OUTPUT 
# YES
# 100 55 100 12
# 0 70 87 0
# 0 95 93 0
# 93 100 66 0


# Алгоритм Форда-Фалкерсона

def dfs(C, F, s, t):
    stack = set([s])
    paths = {s:[]}
    if s == t:
        return paths[s]
    while(stack):
        u = stack.pop()
        for v in range(len(C)):
            if(C[u][v] - F[u][v] > 0) and v not in paths:
                paths[v] = paths[u] + [(u, v)]
                if v == t:
                    return paths[v]
                stack.add(v)
    return None

def max_flow(C, s, t):
    n = len(C)
    # Обнуляем все потоки
    A = [[0] * n for _ in range(n)]
    # В остаточной сети находим любой путь из источника в сток. Если такого пути нет, останавливаемся.
    path = dfs(C, A, s, t)
    while path != None:
        # На найденном пути в остаточной сети ищем ребро с минимальной пропускной способностью
        flow_min = min(C[u][v] - A[u][v] for u, v in path)
        for u, v in path:
            A[u][v] += flow_min # Для каждого ребра на найденном пути увеличиваем поток на flow_min
            A[v][u] -= flow_min # А в противоположном ему — уменьшаем на flow_min
        # Повторяем
        path = dfs(C, A, s, t)
    return sum(A[s][i] for i in range(n)), A
    
# Test graphs
graph = [[ 0, 193, 320, 346, 12, 0, 0, 0, 0, 0 ],  # s
            [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
            [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ], 
            [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
            [ 0, 0, 0, 0, 0, 100, 100, 100, 100, 0 ],  
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 267 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 157 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 188 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 259 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ]] # t
source = 0
sink = 9
SR = [193, 320, 346, 12]
n = len(SR)

# graph = [[ 0, 201, 201, 0, 0, 0],  # s
#          [ 0, 0, 0, 100, 100, 0],  # o
#          [ 0, 0, 0, 100, 100, 0],  # p
#          [ 0, 0, 0, 0, 0, 201],
#          [ 0, 0, 0, 0, 0, 201], 
#          [ 0, 0, 0, 0, 0, 0]]

# source = 0
# sink = 5

# Large test for cProfile
# python -m cProfile -s time main.py
# N = 100
# SR = [10000 for _ in range(N)]
# SC = [10000 for _ in range(N)]

#######################################################
# Парсинг данных из консоли 

# N = int(input())
# SR = list(map(int, input().split()))
# SC = list(map(int, input().split()))

# shape_graph = (N*2)+2
# graph = [[0] * shape_graph for _ in range(shape_graph)]

# source = 0  
# sink = shape_graph-1
# n = len(SR)

# for i in range(n):
#     graph[source][i+1] = SC[i]

# for i in range(n, n*2):
#     idx =  i - n
#     graph[i+1][sink] = SR[idx]

# for i in range(1, n+1):
#     for j in range(n+1, (n*2)+1):
#         graph[i][j] = 100
#######################################################
# На вход подается тестовая сеть и номер вершины источника и стока 
max_flow_value, A = max_flow(graph, source, sink)

# Вывод
if max_flow_value == sum(SR):
    print("YES")
    for j in range(n+1, (n*2)+1):
        lis_ = []
        for i in range(1, n+1):
            lis_.append(A[i][j])
        print(*lis_)
else:
    print("NO")

