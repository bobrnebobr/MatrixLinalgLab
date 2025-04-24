from typing import Tuple, List
from matrix import Matrix
from .find_eigenvalues import find_eigenvalues
from .find_eigenvectors import find_eigenvectors
from .covariance_matrix import covariance_matrix
from .center_data import center_data
from .explained_variance_ratio import explained_variance_ratio
import random


class PCA_DATA:
    mean_columns = []
    centered_data = None
    covariance_matrix = None
    X_proj = None
    eigenvalues = []
    eigenvectors_matrix = None
    varience = 0

    def __init__(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)


def pca(X: Matrix, k: int) ->  PCA_DATA:
    """
    Вход:
    X: матрица данных (n×m)
    k: число главных компонент
    Выход:
    X_proj: проекция данных (n×k)
    : доля объяснённой дисперсии
    """
    n, m = X.shape
    centered_data, mean_columns = center_data(X)
    cov_matrix = covariance_matrix(centered_data)

    eigenvalues = find_eigenvalues(cov_matrix)
    eigenvectors = find_eigenvectors(cov_matrix, eigenvalues)

    eigenvectors = list(sorted(eigenvectors, key=lambda x: x[1], reverse=True))

    eigenvalues = [round(i[1], 6) for i in eigenvectors]
    eigenvectors = [i[0] for i in eigenvectors]

    eigenvectors_matrix = Matrix(m, k)
    for i in range(k):
        for j in range(eigenvectors[i].shape[0]):
            eigenvectors_matrix[j + 1, i + 1] = eigenvectors[i][j + 1, 1]

    X_proj = centered_data * eigenvectors_matrix
    variance = explained_variance_ratio(eigenvalues, k)

    pca_data = PCA_DATA(
        mean_columns=mean_columns,
        eigenvalues=eigenvalues,
        eigenvectors_matrix=eigenvectors_matrix,
        covariance_matrix=cov_matrix,
        variance=variance,
        X_proj=X_proj,
        centered_data=centered_data,
    )

    return pca_data

def reconstruct_X(pca_data: PCA_DATA) -> Matrix:
    scaled_data = pca_data.X_proj * pca_data.eigenvectors_matrix.transpose()
    for row in range(1, scaled_data.shape[0] + 1):
        for col in range(1, scaled_data.shape[1] + 1):
            scaled_data[row, col] += pca_data.mean_columns[col - 1]
    return scaled_data

def reconstruction_error(X_orig: Matrix, X_recon: Matrix) -> float:
    """
    Возвращает среднеквадратическую ошибку восстановления
    """
    MSE = 1 / (X_orig.shape[0] * X_orig.shape[1])
    sum_error = 0
    for row in range(1, X_orig.shape[0] + 1):
        for col in range(1, X_orig.shape[1] + 1):
            sum_error += (X_orig[row, col] - X_recon[row, col]) ** 2
    MSE *= sum_error
    return MSE

def auto_select_k(eigenvalues: List[float], threshold: float = 0.95) -> int:
    """
    Вход:
    eigenvalues: список собственных значений
    threshold: порог объяснённой дисперсии
    Выход: оптимальное число главных компонент k
    """
    for i in range(1, len(eigenvalues) + 1):
        if explained_variance_ratio(eigenvalues, i) >= threshold:
            return i
    return -1

def add_noise_and_compare(X:'Matrix', noise_level: float = 0.1):
    """
    Вход:
    X: матрица данных (n×m)
    noise_level: уровень шума (доля от стандартного отклонения)
    Выход: результаты PCA до и после добавления шума.
    В этом задании можете проявить творческие способности, поэтому выходные данные не
    →
    типизированы.
    """
    for row in range(1, X.shape[0] + 1):
        for col in range(1, X.shape[1] + 1):
            X[row, col] += random.gauss(0, noise_level)
    return X
