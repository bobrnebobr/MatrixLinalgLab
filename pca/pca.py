from typing import Tuple, List
from matrix import Matrix
from .find_eigenvalues import find_eigenvalues
from .find_eigenvectors import find_eigenvectors
from .covariance_matrix import covariance_matrix
from .center_data import center_data
from .explained_variance_ratio import explained_variance_ratio


def pca(X: Matrix, k: int) -> Tuple[Matrix, Matrix, float]:
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
    print(eigenvalues)

    return X_proj, eigenvectors_matrix, variance
