import unittest
from inspect import trace

from matrix import Matrix


class TestMatrix(unittest.TestCase):

    def equals(self, data, matrix): #функция проверки совпадения матрицы и массива
        for i in range(1, len(data) + 1):
            for j in range(1, len(data[0]) + 1):
                self.assertEqual(data[i-1][j-1], matrix[i, j])

    def test_init(self): #Тест инициализации матрицы
        n, m = 3, 3
        matrix = Matrix(3, 3)
        data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        self.equals(data, matrix)

    def test_getitem_out_of(self): #Тест, если индекс за пределами матрицы
        n, m = 3, 3
        matrix = Matrix(3, 3)
        data = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        try:
            print(matrix[4, 4])
        except KeyError as e:
            print("\nТест 3:", e)


    def test_add(self): #Тест сложения
        n, m = 2, 2
        matrix1 = Matrix(2, 2)
        matrix2 = Matrix(2, 2)

        data1 = [[30, 39], [14, 24]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix1[i, j] = float(data1[i - 1][j - 1])

        data2 = [[20, 11], [36, 26]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix2[i, j] = float(data2[i - 1][j - 1])

        matrix_sum = matrix1 + matrix2

        data_sum = [[50, 50], [50, 50]]

        self.equals(data_sum, matrix_sum)

    def test_subtract(self): #Тест вычитания
        n, m = 2, 2
        matrix1 = Matrix(2, 2)
        matrix2 = Matrix(2, 2)

        data1 = [[50, 50], [50, 50]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix1[i, j] = float(data1[i - 1][j - 1])

        data2 = [[20, 11], [36, 26]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix2[i, j] = float(data2[i - 1][j - 1])

        matrix_sub = matrix1 - matrix2

        data_sub = [[30, 39], [14, 24]]

        self.equals(data_sub, matrix_sub)

    def test_multiply_by_number(self): #Тест умножения на число
        n, m = 3, 3
        matrix = Matrix(n, m)
        data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])
        matrix_multiply = matrix * 2
        data_multiply = [[2, 4, 6], [8, 10, 12], [14, 16, 18]]

        self.equals(data_multiply, matrix_multiply)

    def multiply_two_matrices(self): #Тест умножения матриц
        n, m = 2, 2
        matrix1 = Matrix(2, 2)
        matrix2 = Matrix(2, 2)

        data1 = [[1, 0], [0, 1]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix1[i, j] = float(data1[i - 1][j - 1])

        data2 = [[3, 3], [6, 6]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix2[i, j] = float(data2[i - 1][j - 1])

        matrix_mult = matrix1 * matrix2

        data_mult = [[3, 3], [6, 6]]

        self.equals(data_mult, matrix_mult)

        matrix3 = Matrix(2, 2)
        matrix4 = Matrix(2, 2)

        data3 = [[2, 4], [8, 16]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix3[i, j] = float(data3[i - 1][j - 1])

        data4 = [[3, 3], [6, 6]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix4[i, j] = float(data4[i - 1][j - 1])

        matrix_mult2 = matrix3 * matrix4

        data_mult2 = [[30, 30], [120, 120]]

        self.equals(data_mult2, matrix_mult2)

    def test_trace(self): #тест получения следа
        n, m = 3, 3
        matrix = Matrix(n, m)
        data = [[5, -1, 0], [0, -1, 1], [15, -1, 4]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])
        self.assertEqual(matrix.trace(), 8)

    def test_negative(self): #Тест отрицательная матрица
        n, m = 3, 3
        matrix = Matrix(n, m)
        data = [[5, -1, 2], [-9, -1, 1], [15, -1, 4]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])
        data_neg =  [[-5, 1, -2], [9, 1, -1], [-15, 1, -4]]

        self.equals(data_neg, -matrix)

    def test_pop(self): #Тест удаления строки и столбца
        n, m = 3, 3
        matrix = Matrix(n, m)

        data = [[5, -1, 2], [-9, -1, 1], [15, -1, 4]]
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                matrix[i, j] = float(data[i - 1][j - 1])

        data_pop = [[5, 2], [-9, 1]]
        matrix_pop = matrix.pop(3, 2)

        self.equals(data_pop, matrix_pop)
