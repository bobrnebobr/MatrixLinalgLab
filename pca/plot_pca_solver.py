from matplotlib import pyplot as plt

from matrix import Matrix
from matplotlib.figure import Figure


def plot_pca_projection(X_proj:'Matrix') -> Figure:
    """
    Вход: проекция данных X_proj (n×2)
    Выход: объект Figure из Matplotlib
    """
    x = [X_proj[i, 1] for i in range(1, X_proj.shape[0] + 1)]
    y = [X_proj[i, 2] for i in range(1, X_proj.shape[0] + 1)]

    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)
    ax.scatter(x, y)

    return figure