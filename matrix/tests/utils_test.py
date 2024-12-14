import unittest
from inspect import trace

from matrix.utils import *


class TestUtils(unittest.TestCase):

    def test_determ1(self):
        n, m = 2, 2
        matrix = Matrix(n, m)
        data = [[1, 2], [3, 4]]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        self.assertEqual(calculate_determinant(matrix), -2.0)
        self.assertEqual(has_inverse(matrix), "Да, матрица имеет себе обратную")

    def test_determ2(self):
        n, m = 3, 3
        matrix = Matrix(n, m)
        data = [[1, 2, 3], [0, 1, 4], [5, 6, 0]]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        self.assertEqual(calculate_determinant(matrix), 1.0)
        self.assertEqual(has_inverse(matrix), "Да, матрица имеет себе обратную")

    def test_determ2(self):
        n, m = 4, 4
        matrix = Matrix(n, m)
        data = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        self.assertEqual(calculate_determinant(matrix), 0)
        self.assertEqual(has_inverse(matrix), "Нет, матрица не имеет себе обратную")

