import numpy as np


# finding the pivot
def find_pivot(matrix):
    # * getting the minimum of the z row
    z_min = np.min(matrix[-1][:-1])
    # * selecting the pivot column
    index_c = np.where(matrix[-1] == z_min)[0][0]
    pivot_c = matrix[:, index_c]
    # * selecting the pivot row
    div = np.zeros((len(matrix[:-1,0])))
    for i in range(len(pivot_c[:-1])):
        if pivot_c[i] == 0:
            div[i] = 1000
            continue
        div[i] = matrix[:-1, -1][i] / pivot_c[:-1][i]
    div_min = min(div)
    index_r = np.where(div == div_min)[0][0]
    # * returning the pivot coordinates
    return index_r, index_c


def pivoting(matrix, pivot):
    # * dividing the pivot row by the pivot element
    matrix[pivot[0]] /= matrix[pivot[0]][pivot[1]]
    # * pivoting circle
    for i in range(len(matrix)):
        if i == pivot[0]:
            continue
        matrix[i][:] -= matrix[i][pivot[1]] * matrix[pivot[0]]
    return matrix


# getting input
N_conditions = 2
N_variables = 2
# * restrictions
a = [3, 5]
b = [4, 1]
RHS = [78, 36]
# * objective function
Z = [5, 4]
# creating initial table
# * concatenating the restrictions
T = [a, b]
# * concatenating the restrictions and the basis
matrix = np.concatenate((T, np.identity(N_conditions)), axis=1)
# * adding the right hand side
matrix = np.column_stack((matrix, RHS))
# * adding the objective function
temp = np.append(np.negative(Z), np.zeros(N_conditions+1))
matrix = np.vstack((matrix, temp))
# * printing the initial table
print(matrix)

# running the algorithm
while np.any(matrix[-1] < 0):
    p = find_pivot(matrix)
    matrix = pivoting(matrix, p)
    print(np.round(matrix,1))








