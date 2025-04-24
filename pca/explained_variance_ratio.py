from matrix import Matrix
from typing import List

def explained_variance_ratio(eigenvalues: List[float], k: int) -> float:
    """
    Вход:
    eigenvalues: список собственных значений
    k: число компонент
    Выход: доля объяснённой дисперсии
    """
    eigenvalues.sort(key=int, reverse=True)
    return sum(eigenvalues[:k]) / sum(eigenvalues)