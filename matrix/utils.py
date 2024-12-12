from .matrix import Matrix


def input_matrix(type: type = float) -> Matrix:
    """
    Функция для ввода матрицы
    :param type: один ищ Numeric типов
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
