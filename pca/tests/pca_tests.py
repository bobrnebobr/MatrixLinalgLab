from matrix import Matrix
from pca.pca import *
import unittest


class TestGaussSolver(unittest.TestCase):
    def test_simple_sample(self):
        A = Matrix(2, 2)
        A[1, 1] = 1
        A[1, 2] = 2
        A[2, 1] = 3
        A[2, 2] = 4

        results = pca(A, k=1)
        self.assertAlmostEqual(A[1, 1], reconstruct_X(results)[1, 1], delta=1e-6)
        self.assertAlmostEqual(A[1, 2], reconstruct_X(results)[1, 2], delta=1e-6)
        self.assertAlmostEqual(A[2, 1], reconstruct_X(results)[2, 1], delta=1e-6)
        self.assertAlmostEqual(A[2, 2], reconstruct_X(results)[2, 2], delta=1e-6)

        self.assertAlmostEqual(0.707106, results.eigenvectors_matrix[1, 1], delta=1e-5)
        self.assertAlmostEqual(0.707106, results.eigenvectors_matrix[2, 1], delta=1e-5)

    def test_another(self):
        A = Matrix(3, 3)
        A[1, 1] = 2
        A[1, 2] = 0
        A[1, 3] = 0
        A[2, 1] = 0
        A[2, 2] = 2
        A[2, 3] = 1
        A[3, 1] = 0
        A[3, 2] = 0
        A[3, 3] = 3

        results = pca(A, k=2)
        self.assertAlmostEqual(A[1, 1], reconstruct_X(results)[1, 1], delta=1e-6)
        self.assertAlmostEqual(A[1, 2], reconstruct_X(results)[1, 2], delta=1e-6)
        self.assertAlmostEqual(A[2, 1], reconstruct_X(results)[2, 1], delta=1e-6)
        self.assertAlmostEqual(A[2, 2], reconstruct_X(results)[2, 2], delta=1e-6)

        self.assertAlmostEqual(-0.581364, results.eigenvectors_matrix[1, 1], delta=1e-5)
        self.assertAlmostEqual(0.060668, results.eigenvectors_matrix[2, 1], delta=1e-5)