from typing import Tuple
from matrix import Matrix
from .find_eigenvalues import find_eigenvalues
from .covariance_matrix import covariance_matrix
from .center_data import center_data


def pca(X: Matrix, k: int) -> Tuple[Matrix, float]:
    """
    Вход:
    X: матрица данных (n×m)
    k: число главных компонент
    Выход:
    X_proj: проекция данных (n×k)
    : доля объяснённой дисперсии
    """
    centered_data = center_data(X)
    cov_matrix = covariance_matrix(centered_data)


