from matrix import Matrix, calculate_determinant
from typing import List
from pca.root_finder import *
import math

def find_eigenvalues(C: 'Matrix', tol: float = 1e-6)-> List[float]:
    """Вход:
    C: матрица ковариаций (m×m)
    tol: допустимая погрешность
    Выход: список вещественных собстpвенных значений
    """
    m = C.shape[0]

    min_val = float('inf')
    max_val = -float('inf')

    for i in range(1, m+1):
        r = sum(abs(C[i, j]) for j in range(1, m+1) if i != j)
        center = C[i, i]
        min_val = min(min_val, center - r)
        max_val = max(max_val, center + r)

    def charact_polynom(lambd):
        C_minus_lambd_E = Matrix(m, m)
        for i in range(1, m+1):
            for j in range(1, m+1):
                if i == j:
                    C_minus_lambd_E[i, j] = C[i, j] - lambd
                else:
                    C_minus_lambd_E[i, j] = C[i, j]
        det = calculate_determinant(C_minus_lambd_E)
        # print(C_minus_lambd_E)
        return det

    root_finder = RootFinder(charact_polynom)

    n_intervals = max(1000, 100*m) #количество интервалов для поиска
    step = (max_val - min_val) / n_intervals

    intervals = []
    #проверочка на границы
    x = min_val - step / 2
    x_next = x + step
    prev_val = charact_polynom(x)

    eigenvalues = []

    for _ in range(2 * n_intervals + 1):
        curr_val = charact_polynom(x_next)

        if prev_val*curr_val <= 0 or abs(prev_val) < tol:
            intervals.append((x, x_next))
        x = x + step / 2
        x_next = x_next + step / 2
        prev_val = curr_val

    for a, b in intervals:
        root, _ = root_finder.bisection(a, b, tol)
        if root is not None:
            if not any(abs(root - x) < tol for x in eigenvalues):
                eigenvalues.append(root)

    if len(eigenvalues) < m:
        for i in range(1, m + 1):
            diag_val = C[i, i]
            if not any(abs(diag_val - x) < tol for x in eigenvalues):
                eigenvalues.append(diag_val)
    eigenvalues.sort(reverse=True)

    return eigenvalues




