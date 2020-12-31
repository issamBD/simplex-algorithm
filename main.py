import numpy as np
import pandas as pd
import sys


# a function to create the display the updated table
def create_table():
    # creating lists for columns and rows indexes
    cl = []
    rl = []
    # adding the titles of the basis and basis and non basis variables to the indexes
    for i in range(numOfv):
        p = "x" + str(i + 1)
        cl.append(p)
    for i in range(numOfc):
        p = "s" + str(i + 1)
        cl.append(p)
        rl.append(p)
    # adding the right hand side to the index
    cl.append("RHS")
    # creating a pandas DataFrame with the generated matrix and indexes
    df = pd.DataFrame(conds, columns=cl, index=rl)
    # adding the objective function to the DataFrame
    df.loc["Z"] = z_row
    # adding the title of the objective function to the indexes
    rl.append("Z")
    # printing the DataFrame
    print(df)
    print("---------------------------------")
    # returning the indexes of columns and rows
    return df, cl, rl


# a function to get the restrictions functions from the user
def define(input):
    global counter
    # a boolean variable to determine if the elements of the restriction function should be reversed
    param = False
    # a temporary empty list to save the elements of the restriction function
    array = np.zeros([1, numOfv + numOfc + 1])[0]
    # splitting the input by the comparative
    if "<=" in input:
        input = input.split("<=")
    elif ">=" in input:
        input = input.split(">=")
        # setting the boolean variable to true to reverse the elements of the restriction function later
        param = True
    # adding a plus sign to an element if it's negative (important for splitting the string)
    if '-' in input[0]:
        input[0] = input[0].replace("-", "+-")
    # deleting the potentially added plus sign at the start of the function if existed
    if input[0][0] == '+':
        input[0] = input[0][1:]
    # splitting the string by the plus sign
    input[0] = input[0].split("+")
    # eliminating the x1, x2... signs and keeping the numeric elements only
    for i in range(len(input[0])):
        array[i] = input[0][i][:-2]
    # saving the value of the right hand side of the restriction
    array[-1] = input[-1]
    # reversing the elements of the restriction if param is set to True
    if param:
        array = [-i for i in array]
    # setting the basis variables
    array[numOfv + counter] = 1
    counter += 1
    # returning the matrix row of the restriction generated from the input
    return array


# a function to get the objective function from the user
def define_r(input):
    # a temporary empty list to save the elements of the objective function
    array = np.zeros([1, numOfv + numOfc + 1])[0]
    # adding a plus sign to an element if it's negative (important for splitting the string)
    if "-" in input:
        input = input.replace("-", "+-")
    # deleting the potentially added plus sign at the start of the function if existed
    if input[0] == '+':
        input = input[1:]
    # splitting the input by the plus sign
    input = input.split("+")
    # eliminating the x1, x2... signs and keeping the numeric elements only
    for i in range(len(input)):
        array[i] = input[i][:-2]
    # returning the matrix row of the objective function generated from the input
    return array

# a function to find the minimum value in the objective function and monitoring if a solution is reached
def z_min(negative):
    # checking if all elements of the objective function are positive (in this case an optimal solution is found)
    if (z_row >= 0).all():
        print("solution is optimal")
        sys.exit()
    else:
        if negative:
            return
        # returning the minimum value of the objective function elements if the primal simplex algorithm is used
        else:
            minimum = min(z_row)
            return minimum


# a function to calculate the pivot element in the dual simplex algorithm
def find_pivot_r():
    z_min(True)
    r = conds[:, -1]
    r_minimum = min(r)
    pivot[0] = list(r).index(r_minimum)
    pivot_row = conds[pivot[0]]
    temp_size = len(z_row)
    temp = np.zeros([1, temp_size])[0]
    for i in range(len(pivot_row)):
        if pivot_row[i] >= 0:
            temp[i] = -5555
        else:
            temp[i] = z_row[i] / pivot_row[i]
    maxi = max(temp)
    pivot[1] = list(temp).index(maxi)
    rows[pivot[0]] = columns[pivot[1]]


def find_pivot():

    z_minimum = z_min(False)
    pivot[1] = list(z_row).index(z_minimum)
    pivot_column = conds[:, pivot[1]]
    if (pivot_column < 0).all():
        print("no solution is possible")
        sys.exit()

    temp_size = len(RHS)
    temp = np.zeros([1, temp_size])[0]
    for i in range(len(pivot_column)):
        if pivot_column[i] <= 0:
            temp[i] = 1000
        else:
            temp[i] = RHS[i] / pivot_column[i]
    temp_min = min(temp)
    pivot_row = list(temp).index(temp_min)
    pivot[0] = pivot_row
    rows[pivot[0]] = columns[pivot[1]]


def pivoting():
    conds[pivot[0],:] = conds[pivot[0],:] / conds[pivot[0]][pivot[1]]
    for i in conds:
        compare = i == conds[pivot[0],:]
        if compare.all():
            continue
        else:
            i[:] += (-i[pivot[1]]*conds[pivot[0]])
    z_row[:] = z_row[:]  - z_row[pivot[1]] * conds[pivot[0]]


def table():
    t_conds = conds.copy()
    t_z = z_row.copy()
    for i in t_conds:
        i[:] = [round(b, 2) for b in i]
    t_z[:] = [round(b, 2) for b in z_row]
    matrix = pd.DataFrame(t_conds)
    matrix.loc["Z"] = t_z
    matrix.columns = columns
    matrix.index = rows
    print(matrix)
    print("---------------------------------")


# variables definition
pivot = [-1, 1]
counter = 0
rows = []
columns = []
# getting the number of variables and restrictions
numOfv = int(input("enter the number of variables : "))
numOfc = int(input("enter number of restrictions : "))
# creating an empty matrix according to the number of variables and restrictions
conds = np.zeros([numOfc,  numOfv+numOfc+1])
# getting the objective function as user input and eliminating the white spaces
obj = input("Enter the objective function : ").replace(" ", "")
# reversing the signs of the objective function's elements
z_row = - np.array(define_r(obj))
# getting the restrictions as user input and eliminating the white spaces
for i in range(len(conds)):
    con = input("Enter the " + str(i+1) + ". restriction : ").replace(" ", "")
    conds[i] = define(con)
# saving the restrictions in a numpy array
conds = np.array(conds)
# creating the table to display and saving it along the number of columns and rows
matrix, columns, rows = create_table()
# looping until a solution is reached or until it's determined that no solution is possible
while True:
    # saving the right hand side of the table
    RHS = conds[:, -1]
    # checking if the right hand side of the table contains negative values
    if not (RHS >= 0).all():
        # implementing the dual simplex algorithm to find the pivot
        find_pivot_r()
    else:
        # implementing the primal simplex algorithm to find the pivot
        find_pivot()
    # pivoting the table
    pivoting()
    # displaying the table
    table()





