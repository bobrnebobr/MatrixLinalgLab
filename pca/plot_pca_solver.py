import pandas as pd
from matplotlib import pyplot as plt
import pandas as pd

from matrix import Matrix
from matplotlib.figure import Figure


def plot_pca_projection(X_proj:pd.DataFrame) -> Figure:
    """
    Вход: проекция данных X_proj (n×2)
    Выход: объект Figure из Matplotlib
    """
    x = X_proj.iloc[:, 0]  # первая компонента
    y = X_proj.iloc[:, 1]

    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)
    ax.scatter(x, y, c=X_proj["target"])

    return figure