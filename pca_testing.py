from pca.pca import pca
from pca.plot_pca_solver import plot_pca_projection
from matrix import *

matrix = input_matrix()

results = pca(matrix, 2)

print(results[0])
print("\n")
print(results[1])
print("\n")
print(results[2])
print("\n")
fig = plot_pca_projection(results[0])
fig.show()