from  typing import List

from matrix import Matrix


def gauss_solver(A: 'Matrix', b: 'Matrix')-> List['Matrix']:
    """
    Вход:
    A: матрица коэффициентов (n×n). Используется класс Matrix из предыдущей лабораторной работы
    b: вектор правых частей (n×1)
    Выход:
    list[Matrix]: список базисных векторов решения системы
    Raises:
    ValueError: если система несовместна
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError('Матрица не квадратная')
    if A.shape[0] != b.shape[0] or b.shape[1] != 1:
        raise ValueError('Матрица и вектор несовместимы')

    n = A.shape[0]

    #расширенная матрица [A|b]
    augmented = Matrix(n, n+1)
    for i in range(1, n+1):
        for j in range(1, n+1):
            #из A
            augmented[i, j] = A[i, j]
        #из b
        augmented[i, n+1] = b[i, 1]

    #приведение к ступенчатому виду
    cur_row = 1
    for col in range(1, n+1):
        #поиск ведущего элемента в столбце
        max_row = cur_row
        max_val = abs(augmented[max_row, col])

        for row in range(cur_row + 1, n + 1):
            if abs(augmented[row, col]) > max_val:
                max_val = abs(augmented[row, col])
                max_row = row

        #если столбец нулевой (чтобы учесть погрешность при вычислениях, возьму эпсилон = 1e-10)
        if max_val < 1e-10:
            continue

        #перестановка строк
        if max_row != cur_row:
            for j in range(col, n+2):
                temp = augmented[cur_row, j]
                augmented[cur_row, j] = augmented[max_row, j]
                augmented[max_row, j] = temp

        #нормирую строку (делю на ведущий элемент)
        pivot_el = augmented[cur_row, col]
        for j in range(col, n+2):
            augmented[cur_row, j] /= pivot_el

        #вычитаю строку из других
        for row in range(1, n + 1):
            if row != cur_row:
                multiplier = augmented[row, col]
                for j in range(col, n+2):
                    augmented[row, j] -= multiplier*augmented[cur_row, j]

        cur_row += 1

    #надо учесть случай, когда [0, ..., 0 | c], где c != 0
    for row in range(cur_row, n + 1):
        if abs(augmented[row, n + 1]) > 1e-10:
            raise ValueError('У системы нет решений')

    #Случаи

    #Единственное решение (rank = n)
    if cur_row - 1 == n:
        solution = Matrix(n, 1)
        for i in range(1, n+1):
            solution[i, 1] = augmented[i, n+1]
        return [solution]

    #Бесконечно много решений (rank < n)
    #Надо найти базисные и свободные переменные

    #базисные переменные
    basic_vars = []
    for row in range(1, cur_row):
        for col in range(1, n+1):
            if abs(augmented[row, col] - 1) < 1e-10: #должна быть единичка на диагонали
                basic_vars.append(col)
                break
    #оставшиеся - свободные
    free_vars = [col for col in range(1, n+1) if col not in basic_vars]

    #построение системы решений
    solutions = []

    #частное решение неоднородной системы
    particular_solution = Matrix(n, 1)
    for row, col in enumerate(basic_vars, 1):
        particular_solution[col, 1] = augmented[row, n+1]
    solutions.append(particular_solution)

    #базисные решения однородной системы
    for free_col in free_vars:
        solution_vector = Matrix(n, 1) #вектор решения
        solution_vector[free_col, 1] = 1 #для свободной переменной

        #значения для базисных переменных
        for row, basic_col in enumerate(basic_vars, 1):
            sum_terms = 0
            for col in range(basic_col + 1, n+1):
                sum_terms += augmented[row, col]*solution_vector[col, 1]
            solution_vector[basic_col, 1] = -sum_terms

        solutions.append(solution_vector)

    return solutions