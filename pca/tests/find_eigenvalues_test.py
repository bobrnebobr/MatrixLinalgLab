import unittest
from matrix import Matrix
from pca.find_eigenvalues import find_eigenvalues  # Импортируем вашу функцию

class TestFindEigenvalues(unittest.TestCase):
    def test_2x2_matrix(self):
        """Тест для матрицы 2x2 с известными собственными значениями"""
        C = Matrix(2, 2)
        C[1, 1] = 4
        C[1, 2] = 1
        C[2, 1] = 1
        C[2, 2] = 3

        eigenvalues = find_eigenvalues(C)

        # Ожидаемые собственные значения: 4.618 и 2.382
        self.assertEqual(len(eigenvalues), 2)
        self.assertAlmostEqual(eigenvalues[0], 4.618, places=2)
        self.assertAlmostEqual(eigenvalues[1], 2.382, places=2)

    def test_diagonal_matrix(self):
        """Тест для диагональной матрицы (собственные значения = диагональным элементам)"""
        C = Matrix(3, 3)
        C[1, 1] = 5
        C[1, 2] = 0
        C[1, 3] = 0
        C[2, 1] = 0
        C[2, 2] = 3
        C[2, 3] = 0
        C[3, 1] = 0
        C[3, 2] = 0
        C[3, 3] = 1

        eigenvalues = find_eigenvalues(C)
        #print(eigenvalues)
        self.assertEqual(len(eigenvalues), 3)
        self.assertAlmostEqual(eigenvalues[0], 5.0, places=4)
        self.assertAlmostEqual(eigenvalues[1], 3.0, places=4)
        self.assertAlmostEqual(eigenvalues[2], 1.0, places=4)

    def test_symmetric_matrix(self):
        """Тест для симметричной матрицы"""
        C = Matrix(2, 2)
        C[1, 1] = 2
        C[1, 2] = 1
        C[2, 1] = 1
        C[2, 2] = 2

        eigenvalues = find_eigenvalues(C)

        # Ожидаемые собственные значения: 3 и 1
        print(eigenvalues)
        self.assertEqual(len(eigenvalues), 2)
        self.assertAlmostEqual(eigenvalues[0], 3.0, places=4)
        self.assertAlmostEqual(eigenvalues[1], 1.0, places=4)

    def test_single_value_matrix(self):
        """Тест для матрицы 1x1"""
        C = Matrix(1, 1)
        C[1, 1] = 5.5

        eigenvalues = find_eigenvalues(C)

        self.assertEqual(len(eigenvalues), 1)
        self.assertAlmostEqual(eigenvalues[0], 5.5, places=4)

    def test_multiple_roots(self):
        """Тест для матрицы с кратными собственными значениями"""
        C = Matrix(2, 2)
        C[1, 1] = 2
        C[1, 2] = 0
        C[2, 1] = 0
        C[2, 2] = 2

        eigenvalues = find_eigenvalues(C, tol=1e-8)

        # Оба собственных значения равны 2
        self.assertEqual(len(eigenvalues), 1)
        self.assertAlmostEqual(eigenvalues[0], 2.0, places=6)

    def test_zero_matrix(self):
        """Тест для нулевой матрицы"""
        C = Matrix(3, 3)
        # Все элементы по умолчанию 0

        eigenvalues = find_eigenvalues(C)

        # Все собственные значения должны быть 0
        self.assertEqual(len(eigenvalues), 1)
        for val in eigenvalues:
            self.assertAlmostEqual(val, 0.0, places=6)

    def test_high_tolerance(self):
        """Тест с разной точностью"""
        C = Matrix(2, 2)
        C[1, 1] = 4
        C[1, 2] = 1
        C[2, 1] = 1
        C[2, 2] = 3

        # Тест с низкой точностью
        eigenvalues_low = find_eigenvalues(C, tol=1e-2)
        # Тест с высокой точностью
        eigenvalues_high = find_eigenvalues(C, tol=1e-8)

        # Проверяем что результаты согласуются с ожидаемыми
        self.assertAlmostEqual(eigenvalues_low[0], 4.618, places=2)
        self.assertAlmostEqual(eigenvalues_low[1], 2.382, places=2)
        self.assertAlmostEqual(eigenvalues_high[0], 4.618, places=4)
        self.assertAlmostEqual(eigenvalues_high[1], 2.382, places=4)


if __name__ == '__main__':
    unittest.main()