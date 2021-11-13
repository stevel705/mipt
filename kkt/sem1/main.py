# Задача
# https://acm.timus.ru/problem.aspx?space=1&num=1041
# Алгоритм Грама-Шмидта
# https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81_%D0%93%D1%80%D0%B0%D0%BC%D0%B0_%E2%80%95_%D0%A8%D0%BC%D0%B8%D0%B4%D1%82%D0%B0

# INPUT 
# 5 3
# 1 0 0
# 0 1 0
# 0 0 1
# 0 0 2
# 0 0 3
# 10
# 20
# 30
# 10
# 10

# OUTPUT 
# 40
# 1
# 2
# 4

# Скалярное умножение векторов
def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

# Получение  
def gs_cofficient(v1, v2):
    if dot(v1, v1) == 0.0:
        return dot(v2, v1) / 0.00001
    else:
        return dot(v2, v1) / dot(v1, v1)

# Умножение вектора v1 на оператор проекции 
def multiply(cofficient, v):
    return map((lambda x : x * cofficient), v)

# Оператор проекции вектора a на вектор b 
def proj(v1, v2):
    return multiply(gs_cofficient(v1, v2) , v1)

# Алгоритм Процесс Грама ― Шмидта
def gs(X):
    Y = []
    for i in range(len(X)):
        temp_vec = X[i]
        for inY in Y:
            proj_vec = proj(inY, X[i])
            temp_vec = list(map(lambda x, y : x - y, temp_vec, proj_vec))
        Y.append(temp_vec)
    return Y

# Проверка на лин. зависимость
def check_linearly_dependent(liv, vec2):
    # Добавляем новый вектор в список
    liv.append(vec2)
    # Получение ортогональных векторов
    gs_mat = gs(liv)
    # Если последний добавленный вектор нулевой, то вектора лин. зависимы 
    if all(v == 0 for v in gs_mat[-1]):
        return True
    return False

# Считать M, N, вектора и цены
m, n = map(int, (input().split()))
vectors = [ list(map(int, (input().split()))) for _ in range(m) ]
prices = [ int(input()) for _ in range(m) ]

# ZIP векторов, стоимости и индексов векторов
zipped = zip(vectors, prices, range(1, len(vectors) + 1))

# Сортируем по весам в порядке возрастания
sort_zip = sorted(zipped, key=lambda x: x[1])

# Берем самый первый дешевый вектор, его вес и индекс
liv = [sort_zip[0][0]]
total_price = sort_zip[0][1]
indexes = [sort_zip[0][2]]

# проходим по всем отсортированным векторам
for i in range(1, len(sort_zip)):
    # Проверяем на лин. зависимость
    ch = check_linearly_dependent(liv, sort_zip[i][0])
    # Если лин. зависим, то удаляем из списка
    if ch:
        del liv[-1]
    # Иначе прибавляем в общую цену и записываем индекс вектора
    else:
        total_price += sort_zip[i][1]
        indexes.append(sort_zip[i][2])
    # Если количество векторов равно N, то прекращаем обход 
    if len(liv) == n:
        break

# Если количество равно N, то вывести мин. стоимость и отсортированные индексы векторов        
if len(liv) == n:
    print(total_price)
    print("\n".join(list(map(str, sorted(indexes)))))
# Иначе выводим 0
else:
    print(0)