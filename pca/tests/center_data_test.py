import unittest
from matrix import Matrix
from pca.center_data import center_data

class TestCenterData(unittest.TestCase):
    def test_small_matrix(self):
        """Тестирование на маленькой матрице"""
        X = Matrix(3, 2)
        X[1, 1] = 1
        X[1, 2] = 2
        X[2, 1] = 3
        X[2, 2] = 4
        X[3, 1] = 5
        X[3, 2] = 6

        expected = Matrix(3, 2)
        expected[1, 1] = -2
        expected[1, 2] = -2
        expected[2, 1] = 0
        expected[2, 2] = 0
        expected[3, 1] = 2
        expected[3, 2] = 2

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(expected, result))

    def test_already_centered(self):
        """Тестирование на уже центрированных данных"""
        X = Matrix(2, 2)
        X[1, 1] = -1
        X[1, 2] = 1
        X[2, 1] = 1
        X[2, 2] = -1

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(X, result))

    def test_single_row(self):
        """Тестирование на матрице с одной строкой"""
        X = Matrix(1, 3)
        X[1, 1] = 10
        X[1, 2] = 20
        X[1, 3] = 30

        expected = Matrix(1, 3)
        expected[1, 1] = 0
        expected[1, 2] = 0
        expected[1, 3] = 0

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(expected, result))

    def test_zeros_matrix(self):
        """Тестирование на матрице из нулей"""
        X = Matrix(2, 2)
        X[1, 1] = 0
        X[1, 2] = 0
        X[2, 1] = 0
        X[2, 2] = 0

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(X, result))

    def test_negative_values(self):
        """Тестирование на матрице с отрицательными значениями"""
        X = Matrix(2, 2)
        X[1, 1] = -5
        X[1, 2] = -3
        X[2, 1] = -1
        X[2, 2] = 1

        expected = Matrix(2, 2)
        expected[1, 1] = -2
        expected[1, 2] = -2
        expected[2, 1] = 2
        expected[2, 2] = 2

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(expected, result))

    def test_non_integer_result(self):
        """Тестирование на матрице с нецелочисленным результатом"""
        X = Matrix(2, 1)
        X[1, 1] = 1
        X[2, 1] = 2

        expected = Matrix(2, 1)
        expected[1, 1] = -0.5
        expected[2, 1] = 0.5

        result = center_data(X)[0]
        self.assertTrue(self.compare_matrices(expected, result))

    def compare_matrices(self, m1: Matrix, m2: Matrix) -> bool:
        """Вспомогательная функция для сравнения матриц"""
        if m1.shape != m2.shape:
            return False

        for i in range(1, m1.shape[0] + 1):
            for j in range(1, m1.shape[1] + 1):
                if abs(m1[i, j] - m2[i, j]) > 1e-9:  # Учет ошибок округления
                    return False
        return True


if __name__ == '__main__':
    unittest.main()