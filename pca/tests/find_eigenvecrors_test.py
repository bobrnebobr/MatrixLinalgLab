import unittest
from matrix import Matrix
from pca.find_eigenvectors import find_eigenvectors

class TestFindEigenvectors(unittest.TestCase):
    def test_single_eigenvalue(self):
        """Тест для матрицы с одним собственным значением"""
        C = Matrix(1, 1)
        C[1, 1] = 5.0
        eigenvalues = [5.0]
        eigenvectors = [i[0] for i in find_eigenvectors(C, eigenvalues)]

        self.assertEqual(len(eigenvectors), 1)
        self.assertAlmostEqual(eigenvectors[0][1, 1], 1.0, delta=1e-6)

        # Проверка что это действительно собственный вектор
        Av = C * eigenvectors[0]
        lambda_v = eigenvectors[0] * 5.0
        self.assertAlmostEqual(Av[1, 1], lambda_v[1, 1], delta=1e-6)

    def test_zero_matrix(self):
        """Тест для нулевой матрицы (все собственные значения 0)"""
        C = Matrix(3, 3)  # Все элементы 0
        eigenvalues = [0.0, 0.0, 0.0]
        eigenvectors = [i[0] for i in find_eigenvectors(C, eigenvalues)]

        # Должен вернуть ровно один вектор (по спецификации)
        self.assertEqual(len(eigenvectors), 3)

        # Проверка что это собственный вектор
        Av = C * eigenvectors[0]
        lambda_v = eigenvectors[0] * 0.0
        for j in range(1, 4):
            self.assertAlmostEqual(Av[j, 1], lambda_v[j, 1], delta=1e-6)

    def test_orthogonal_vectors(self):
        """Тест для симметричной матрицы (векторы должны быть ортогональны)"""
        C = Matrix(2, 2)
        C[1, 1] = 1
        C[1, 2] = 2
        C[2, 1] = 2
        C[2, 2] = 1

        eigenvalues = [3.0, -1.0]
        eigenvectors = [i[0] for i in find_eigenvectors(C, eigenvalues)]

        self.assertEqual(len(eigenvectors), 2)

        # Проверка ортогональности
        dot_product = sum(eigenvectors[0][i, 1] * eigenvectors[1][i, 1] for i in range(1, 3))
        self.assertAlmostEqual(dot_product, 0.0, delta=1e-6)


if __name__ == '__main__':
    unittest.main()