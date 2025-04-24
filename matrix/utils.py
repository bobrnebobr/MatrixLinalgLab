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
            matrix[i, j] = type(data[i - 1][j - 1])

    return matrix


def calculate_determinant(matrix: Matrix) -> float:
    """
    Вычисление определителя матрицы методом разложения по первой строке
    :param matrix: квадратная матрица
    :return: значение определителя
    """
    n = matrix.shape[0]
    if n != matrix.shape[1]:
        raise ValueError("Матрица должна быть квадратной")

    # Базовые случаи
    if n == 1:
        return matrix[1, 1]
    if n == 2:
        return matrix[1, 1] * matrix[2, 2] - matrix[1, 2] * matrix[2, 1]

    det = 0.0
    for col in range(1, n + 1):
        # Пропускаем нулевые элементы для оптимизации
        if matrix[1, col] == 0:
            continue

        # Создаем минор вручную
        minor = Matrix(n - 1, n - 1)
        minor_row = 1

        for row in range(2, n + 1):  # Пропускаем первую строку
            minor_col = 1
            for j in range(1, n + 1):
                if j != col:  # Пропускаем текущий столбец
                    minor[minor_row, minor_col] = matrix[row, j]
                    minor_col += 1
            minor_row += 1

        # Рекурсивный вызов и суммирование
        sign = (-1) ** (1 + col)
        det += sign * matrix[1, col] * calculate_determinant(minor)

    return det


def determinant():
    matrix = input_matrix()
    if matrix.shape[0] == matrix.shape[1]:
        return calculate_determinant(matrix), has_inverse(matrix)


def has_inverse(matrix: Matrix) -> str:
    det = calculate_determinant(matrix)
    return "Да, матрица имеет себе обратную" if det != 0 else "Нет, матрица не имеет себе обратную"
