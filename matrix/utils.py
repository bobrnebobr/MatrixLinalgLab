from .matrix import Matrix


def input_matrix(type: type = float) -> Matrix:
    """
    Функция для ввода матрицы
    :param type: один из Numeric типов
    :return:
    """
    if type != float and type != int and type != complex:
        raise TypeError("тип должен быть одним из float,  int, complex")

    n, m = map(int, input().split())
    matrix = Matrix(n, m)
    data = [list(input().split()) for _ in range(n)]

    if any(len(values) != m for values in data):
        raise Exception("Матрица должна быть строго размерности n x m")

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            matrix[i][j] = type(data[i - 1][j - 1])

    return matrix

def calculate_determinant(matrix: Matrix):
    if matrix.shape[0] == matrix.shape[1]:
        if matrix.shape[0] == 1:
            return matrix[1][1]
        else:
            det = 0
            for i in range(1, matrix.shape[1]+1):
                det += ((-1) ** (i+1)) * matrix[1][i] * calculate_determinant(matrix.pop(1, i))
            return det


def determinant() -> None:
    matrix = input_matrix()
    if matrix.shape[0] == matrix.shape[1]:
        return calculate_determinant(matrix)

    # количество строк matrix.shape[0]
    # количество столбцов matrix.shape[1]