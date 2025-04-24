from pca.pca import pca, reconstruct_X, reconstruction_error
from pca.plot_pca_solver import plot_pca_projection
from matrix import *

matrix = input_matrix()

results = pca(matrix, 1)
print(results.eigenvectors_matrix)
print("\n")
print(results.X_proj)
X_recon = reconstruct_X(results)
print(X_recon)
print(reconstruction_error(matrix, X_recon))