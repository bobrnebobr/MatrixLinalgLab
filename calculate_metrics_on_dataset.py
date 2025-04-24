import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from matrix import Matrix
from sklearn.metrics import accuracy_score
from pca.pca import *
from pca.plot_pca_solver import plot_pca_projection

def pandas_to_matrix(df: pd.DataFrame) -> Matrix:
    matrix = Matrix(df.shape[0], df.shape[1])
    for i in range(1, matrix.shape[0] + 1):
        for j in range(1, matrix.shape[1] + 1):
            matrix[i, j] = float(df.values[i - 1, j - 1])

    return matrix

def matrix_to_pandas(matrix: 'Matrix') -> pd.DataFrame:
    n, m = matrix.shape
    data = []

    for i in range(1, n + 1):
        row = []
        for j in range(1, m + 1):
            row.append(matrix[i, j])
        data.append(row)

    return pd.DataFrame(data)


df = pd.read_csv("data/Seed_Data.csv")
target = df["target"]
df = df.drop("target", axis=1)
scaler = StandardScaler()
df = pd.DataFrame(scaler.fit_transform(df))
matrix = pandas_to_matrix(df)
pca_data = pca(matrix, 3)
error = reconstruction_error(matrix, reconstruct_X(pca_data))
print("------------- Подсчет метрик --------------")
raw_regression = LogisticRegression()
raw_regression.fit(df, target)
custom_pca_regression = LogisticRegression()
custom_pca_regression.fit(matrix_to_pandas(pca_data.X_proj), target)
sklearn_pca_regression = LogisticRegression()
sklearn_pca_regression.fit(PCA(n_components=3).fit_transform(df), target)

print(f"Accuracy scores:\nБез PCA: {accuracy_score(target, raw_regression.predict(df))}")
print(f"Мой PCA: {accuracy_score(target, custom_pca_regression.predict(matrix_to_pandas(pca_data.X_proj)))}")
print(f"Sklearn PCA: {accuracy_score(target, sklearn_pca_regression.predict(PCA(n_components=3).fit_transform(df)))}")
print("-------Про шум-----------")
noised_X = add_noise_and_compare(matrix)
noise_pca_data = pca(noised_X, 3)
print(f"Ошибка без шума: {error}\nОшибка с шумом: {reconstruction_error(noised_X, reconstruct_X(noise_pca_data))}")
print("----------Графики--------------")
fig = plot_pca_projection(pca_data.X_proj)
fig.show()
