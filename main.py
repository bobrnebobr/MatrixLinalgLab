from matrix import *

if __name__ == '__main__':
    matrix1 = input_matrix()
    matrix2 = input_matrix()
    print(matrix1.build_column_dict())
    print(matrix1 * matrix2)
    print(matrix1 - matrix2)

    print(-matrix)
    print("-----------")
    print(matrix)
    print("-----------")
    # print(matrix[1, 2])
    # print("-----------")
    # print(matrix[3, 2])
    # print("-----------")
    # matrix[3, 3] = 7
    # matrix[3, 1] = 888
    # matrix[1, 1] = 4
    # print(matrix)

    matrix_2 = input_matrix()
    print("------------")
    print(matrix + matrix_2)
    print("-----------")
    # matrix_2[2, 2] += 5
    print(matrix_2)
    print("-----------")
    print(matrix * matrix_2)
    print("-------------")
    print(7 * matrix)
    print("-----------")
    print((matrix * matrix_2).trace())
    print("-------------")
    print(matrix.pop(3, 2))
    print("-------------")
    print(determinant())
