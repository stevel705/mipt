import numpy as np

n = int(input())
outputs = n
table = np.zeros((2 ** (2 ** n), 2 ** n), dtype=np.int32)
output = ''
index = []
received = set()
if n == 1:
    x1 = [0, 1]
    table[0] = x1
elif n == 2:
    x1 = [0, 0, 1, 1]
    x2 = [0, 1, 0, 1]
    table[0] = x1
    table[1] = x2
elif n == 3:
    x1 = [0, 0, 0, 0, 1, 1, 1, 1]
    x2 = [0, 0, 1, 1, 0, 0, 1, 1]
    x3 = [0, 1, 0, 1, 0, 1, 0, 1]
    table[0] = x1
    table[1] = x2
    table[2] = x3
index.append((0, 2 * n))
for i in range(n):
    table[n + i] = ~table[i] + 2
    output += "GATE " + str(n + i) + ' NOT ' + str(i) + '\n'
    received.add(tuple(table[i]))
    received.add(tuple(table[n + i]))
size = 2 * n
k = n
n -= 1
while (size < 2 ** (2 ** k)):
    for t in range(1, (n // 2) + 1):
        for i in range(index[t - 1][0], index[t - 1][1]):
            for j in range(index[n - t - 1][0], index[n - t - 1][1]):
                formula = table[i] & table[j]
                if tuple(formula) not in received:
                    output += "GATE " + str(size) + ' AND ' + str(i) + ' ' + str(j) + '\n'
                    table[size] = formula
                    received.add(tuple(formula))
                    size += 1
                    formula = table[i] & table[j]
                formula = table[i] | table[j]
                if tuple(formula) not in received:
                    output += "GATE " + str(size) + ' OR ' + str(i) + ' ' + str(j) + '\n'
                    table[size] = formula
                    received.add(tuple(formula))
                    size += 1
    index.append((index[-1][1], size))
    n += 1
print(output[:-1])
for i in range(2 ** (2 ** outputs)):
    print('OUTPUT', i, i)

