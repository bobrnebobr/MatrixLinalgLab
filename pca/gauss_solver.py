from  typing import List

from matrix import Matrix


def gauss_solver(A: 'Matrix', b: 'Matrix') -> List['Matrix']:
    if A.shape[0] != A.shape[1]:
        raise ValueError('Матрица не квадратная')
    if A.shape[0] != b.shape[0] or b.shape[1] != 1:
        raise ValueError('Матрица и вектор несовместимы')

    n = A.shape[0]
    #расширенная матрица [A|b]
    augmented = Matrix(n, n + 1)
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            augmented[i, j] = A[i, j]
        augmented[i, n + 1] = b[i, 1]

    #прямой ход метода Гаусса
    rank = 0
    for col in range(1, n + 1):
        #ищем ненулевого элемента в текущем столбце
        pivot_row = None
        for row in range(rank + 1, n + 1):
            if abs(augmented[row, col]) > 1e-5:
                pivot_row = row
                break

        if pivot_row is None:
            continue  #пропускаем нулевой столбец

        #перестановка строк
        rank += 1
        if pivot_row != rank:
            for j in range(col, n + 2):
                augmented[rank, j], augmented[pivot_row, j] = augmented[pivot_row, j], augmented[rank, j]

        #нормировка текущей строки
        norm_val = augmented[rank, col]
        for j in range(col, n + 2):
            augmented[rank, j] /= norm_val

        #обнуление оставшихся элементов
        for row in range(1, n + 1):
            if row != rank and abs(augmented[row, col]) > 1e-10:
                factor = augmented[row, col]
                for j in range(col, n + 2):
                    augmented[row, j] -= factor * augmented[rank, j]

    for row in range(rank + 1, n + 1):
        if abs(augmented[row, n + 1]) > 1e-10:
            raise ValueError('У системы нет решений')

    #единственное решение
    if rank == n:
        solution = Matrix(n, 1)
        for i in range(1, n + 1):
            solution[i, 1] = augmented[i, n + 1]
        return [solution]

    #бесконечное множество решений
    #тогда определяю базисные и свободные переменные
    basic_vars = []
    for row in range(1, rank + 1):
        for col in range(1, n + 1):
            if abs(augmented[row, col] - 1) < 1e-10:
                basic_vars.append(col)
                break

    free_vars = [col for col in range(1, n + 1) if col not in basic_vars]
    solutions = []

    #частное решение
    particular = Matrix(n, 1)
    for row, col in enumerate(basic_vars, 1):
        particular[col, 1] = augmented[row, n + 1]
    if any(abs(particular[i, 1]) > 1e-10 for i in range(1, n + 1)):
        solutions.append(particular)

    #базисные решения
    for free_col in free_vars:
        vec = Matrix(n, 1)
        vec[free_col, 1] = 1
        for row, basic_col in enumerate(basic_vars, 1):
            sum_ = 0
            for j in range(basic_col + 1, n + 1):
                sum_ += augmented[row, j] * vec[j, 1]
            vec[basic_col, 1] = -sum_

        if any(abs(vec[i, 1]) > 1e-10 for i in range(1, n + 1)):
            solutions.append(vec)

    return solutions