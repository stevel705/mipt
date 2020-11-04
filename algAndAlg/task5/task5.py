# Задание 5: совершенное паросочетание
import numpy as np

def s_set():
    prime_list = []
    for num in range(2,500):
        prime = True
        for i in range(2,num):
            if (num%i==0):
                prime = False
        if prime:
            prime_list.append(num)
    return prime_list


def create_Edmonds_matrix(n, S):
    vertexs = []
    for i in range(n):
        v1, v2 = [int(i) for i in input().split(' ')]
        vertexs.append((v1, v2))

    size = max(vertexs[n - 1]) + 1
    A_mat = np.zeros((size, size))

    for v1, v2 in vertexs:
        A_mat[v1][v2] = np.random.choice(S, 1)
   
    return A_mat 


def check_matching(adj_matrix):
    """Checks if det = 0"""
    div = 727
    for cur_ind in range(len(adj_matrix)):
        col_ind = -1
        for j in range(len(adj_matrix)):
            if adj_matrix[cur_ind][j] != 0:
                col_ind = j
                break
        if col_ind == -1:
            return False
        for other_ind in range(len(adj_matrix)):
            if other_ind == cur_ind:
                continue
            if adj_matrix[other_ind][col_ind] != 0:
                adj_matrix[other_ind] = (adj_matrix[other_ind] * adj_matrix[cur_ind][col_ind] - adj_matrix[cur_ind] * adj_matrix[other_ind][col_ind]) % div
    return True


def check_det(matrix):
    prime = 727
    for i in range(matrix.shape[0]):
        col = -1
        for j in range(matrix.shape[0]):
            if matrix[i][j] != 0:
                col = j
                break
        if col == -1:
            return False
        for k in range(matrix.shape[0]):
            if k == i:
                continue
            if matrix[k][col] != 0:
                matrix[k] = (matrix[k] * matrix[i][col] - matrix[i] * matrix[k][col]) % prime
    return True

def main():
    n = int(input())
    S = s_set()
    m = create_Edmonds_matrix(n, S)
   
    check = check_det(m)
    if check:
        print("yes")
    else:
        print("no")
   
if __name__ == "__main__":
    main()