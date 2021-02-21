import numpy as np
import math
n, m = map(int, input().split())

mat = []

for _ in range(m):
    breaket = list(map(int, input().split()))
    mat.append(breaket)

t = 0
while n > 2**t:
    t += 1
t = 2 ** t

r = max(t - 2, 1) 

