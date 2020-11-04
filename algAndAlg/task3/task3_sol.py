import numpy as np

n = int(input())

row = (2 ** (2 ** n))
col = 2 ** n

mat = np.zeros((row, col), dtype=int)
idx = []
# taken = set()
taken = {}
count = 2 * n


if n == 1:
    x1 = np.array([0, 1])
    mat[0] = x1
elif n == 2:
    x1 = np.array([0, 0, 1, 1])
    x2 = np.array([0, 1, 0, 1])
    mat[0] = x1
    mat[1] = x2
elif n == 3:
    x1 = np.array([0, 0, 0, 0, 1, 1, 1, 1])
    x2 = np.array([0, 0, 1, 1, 0, 0, 1, 1])
    x3 = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    mat[0] = x1
    mat[1] = x2
    mat[2] = x3
elif n == 4:
    x1 =  np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1])
    x2 =  np.array([0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1])
    x3 =  np.array([0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1])
    x4 =  np.array([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1])
    mat[0] = x1
    mat[1] = x2
    mat[2] = x3
    mat[3] = x4


idx.append((0, 2 * n))
for i in range(n):
    print(f"GATE {n+i} NOT {i}")
    mat[n + i] = ~mat[i] + 2
    # taken.add(tuple(mat[i]))
    taken[tuple(mat[i])] = tuple(mat[i])
    # taken.add(tuple(mat[n + i]))
    taken[tuple(mat[n + i])] = tuple(mat[n + i])

k = n
n -= 2

while (row > count):
    for i in range(1, (n//2) + 1):
        for j in range(idx[i - 2][0], idx[i - 2][1]):
            for z in range(idx[n - i - 1][0], idx[n - i - 1][1]):
                # Сверяем по &
                op = mat[j] & mat[z]
                # if tuple(op) not in taken:
                if not tuple(op) in taken:
                    print(f"GATE {count} AND {j} {z}")
                    mat[count] = op
                    # taken.add(tuple(op))
                    taken[tuple(op)] = tuple(op)
                    count += 1
                # Сверяем по |
                op = mat[j] | mat[z]
                # if tuple(op) not in taken:
                if not tuple(op) in taken:
                    print(f"GATE {count} OR {j} {z}")
                    mat[count] = op
                    # taken.add(tuple(op))
                    taken[tuple(op)] = tuple(op)
                    count += 1

    idx.append((idx[-1][0], count))
    n += 1

for i in range(row):
    print(f'OUTPUT {i} {i}')

