from matrix import *
from pca import *
from pca.find_eigenvalues import find_eigenvalues

matrix = input_matrix()
print(find_eigenvalues(matrix))
