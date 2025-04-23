import unittest
from matrix import Matrix
from pca.covariance_matrix import covariance_matrix

class TestCovarianceMatrix(unittest.TestCase):
    def test_simple_2x2_case(self):
        """Тест на простой матрице 3x2"""
        X_centered = Matrix(3, 2)
        X_centered[1, 1] = -2
        X_centered[1, 2] = -2
        X_centered[2, 1] = 0
        X_centered[2, 2] = 0
        X_centered[3, 1] = 2
        X_centered[3, 2] = 2

        expected = Matrix(2, 2)
        expected[1, 1] = 4
        expected[1, 2] = 4
        expected[2, 1] = 4
        expected[2, 2] = 4

        result = covariance_matrix(X_centered)
        self.assertTrue(self.compare_matrices(expected, result))

    def test_uncorrelated_features(self):
        """Тест с некоррелированными признаками"""
        X_centered = Matrix(4, 2)
        X_centered[1, 1] = 1;
        X_centered[1, 2] = 0
        X_centered[2, 1] = -1;
        X_centered[2, 2] = 1
        X_centered[3, 1] = 2;
        X_centered[3, 2] = -1
        X_centered[4, 1] = -2;
        X_centered[4, 2] = 0

        result = covariance_matrix(X_centered)

        # Проверяем диагональные элементы
        self.assertAlmostEqual(round(float(result[1, 1]), ndigits=3), 3.333, places=3)
        self.assertAlmostEqual(round(float(result[2, 2]), ndigits=3), 0.667, places=3)

        # Проверяем недиагональные элементы (ковариация должна быть маленькой)
        self.assertAlmostEqual(round(float(result[1, 2]), ndigits=3), -1.000, places=3)
        self.assertAlmostEqual(round(float(result[2, 1]), ndigits=3), -1.000, places=3)

    def test_single_feature(self):
        """Тест с одним признаком"""
        X_centered = Matrix(5, 1)
        X_centered[1, 1] = -2
        X_centered[2, 1] = -1
        X_centered[3, 1] = 0
        X_centered[4, 1] = 1
        X_centered[5, 1] = 2

        expected = Matrix(1, 1)
        expected[1, 1] = 2.5

        result = covariance_matrix(X_centered)
        self.assertAlmostEqual(result[1, 1], expected[1, 1])

    def test_symmetric_result(self):
        """Проверка что результат симметричен"""
        X_centered = Matrix(4, 3)
        for i in range(1, 5):
            for j in range(1, 4):
                X_centered[i, j] = (i + j) * 0.5 - 1

        result = covariance_matrix(X_centered)

        for i in range(1, 4):
            for j in range(1, 4):
                self.assertAlmostEqual(result[i, j], result[j, i])

    def test_error_on_single_row(self):
        """Проверка вызова ошибки при n=1"""
        X_centered = Matrix(1, 3)
        with self.assertRaises(ValueError):
            covariance_matrix(X_centered)

    def compare_matrices(self, m1: Matrix, m2: Matrix, places=7) -> bool:
        """Вспомогательная функция для сравнения матриц"""
        if m1.shape != m2.shape:
            return False

        for i in range(1, m1.shape[0] + 1):
            for j in range(1, m1.shape[1] + 1):
                try:
                    self.assertAlmostEqual(m1[i, j], m2[i, j], places=places)
                except AssertionError:
                    return False
        return True


if __name__ == '__main__':
    unittest.main()