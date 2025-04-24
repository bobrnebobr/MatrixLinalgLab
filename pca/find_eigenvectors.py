from matrix import Matrix
from typing import List, Tuple
from pca.gauss_solver import gauss_solver
import math

def gram_schmidt(eigen_pairs: List[Tuple[Matrix, float]]) -> List[Tuple[Matrix, float]]:
    """
    Применяет процесс Грама-Шмидта к списку пар (вектор, собственное значение)
    Возвращает новый список ортогональных векторов с сохранением собственных значений
    """
    ortho_pairs = []

    for v, lambda_ in eigen_pairs:
        # Создаем копию вектора для ортогонализации
        w = Matrix(v.shape[0], 1)
        for i in range(1, v.shape[0] + 1):
            w[i, 1] = v[i, 1]

        # Вычитаем проекции на уже имеющиеся ортогональные векторы
        for u, _ in ortho_pairs:
            # Вычисляем скалярное произведение
            dot_product = sum(w[i, 1] * u[i, 1] for i in range(1, w.shape[0] + 1))
            # Вычитаем проекцию
            for i in range(1, w.shape[0] + 1):
                w[i, 1] -= dot_product * u[i, 1]

        # Нормализуем вектор
        norm = math.sqrt(sum(w[i, 1] ** 2 for i in range(1, w.shape[0] + 1)))
        if norm > 1e-10:
            for i in range(1, w.shape[0] + 1):
                w[i, 1] /= norm
            ortho_pairs.append((w, lambda_))

    return ortho_pairs

def find_eigenvectors(C: 'Matrix', eigenvalues: List[float]) -> List[Tuple[Matrix, float]]:
    """
    Находит собственные векторы матрицы C для заданных собственных значений.

    Вход:
    C: матрица ковариаций (m×m)
    eigenvalues: список собственных значений

    Выход: список собственных векторов (каждый вектор - объект Matrix размера m×1)
    """
    m = C.shape[0]
    eigen_pairs = []

    for lambda_ in eigenvalues:
        A = Matrix(m, m)
        b = Matrix(m, 1)

        for i in range(1, m + 1):
            for j in range(1, m + 1):
                if i == j:
                    A[i, j] = C[i, j] - lambda_
                else:
                    A[i, j] = C[i, j]

        solutions = gauss_solver(A, b)

        if solutions:
            for sol in solutions:
                eigen_pairs.append((sol, lambda_))

    ortho_pairs = gram_schmidt(eigen_pairs)
    return ortho_pairs

