import typing as tp
from copy import copy

from .common import numeric
from .matrix_row import MatrixRow


class Matrix:
    def __init__(self, n: int, m: int):
        self.shape = (n, m)
        self.matrix: tp.Dict[int, MatrixRow] = {i: MatrixRow({}, length=m) for i in range(1, n + 1)}

    def __getitem__(self, key: int) -> tp.Optional:
        if key > self.shape[0] or key <= 0:
            raise KeyError("Неправильный ключ")

        if key in self.matrix:
            return self.matrix[key]
        else:
            return MatrixRow({}, self.shape[1])

    def __setitem__(self, key: int, value: MatrixRow):
        if key > self.shape[0] or key <= 0:
            raise KeyError("Неправильный ключ")

        self.matrix[key] = value

    def __str__(self) -> str:
        return "\n".join([str(self.matrix[row]) for row in self.matrix])

    def __add__(self, other: 'Matrix') -> 'Matrix':
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            raise Exception("Матрицы должны быть одного размера")

        matrix_sum = Matrix(self.shape[0], self.shape[1])

        for i in range(1, other.shape[0] + 1):
            for j in range(1, other.shape[1] + 1):
                matrix_sum[i][j] = self[i][j] + other[i][j]

        return matrix_sum

    def __neg__(self) -> 'Matrix':
        new_matrix = Matrix(self.shape[0], self.shape[1])

        for i in self.matrix:
            if not self.matrix[i]:
                continue

            for j in self.matrix[i].values:
                new_matrix[i][j] = -self.matrix[i][j]

        return new_matrix

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        return self + (-other)

    def __multiply_by_number(self, number: numeric):
        matrix_copy = Matrix(self.shape[0], self.shape[1])

        for i in range(1, self.shape[0] + 1):
            for j in range(1, self.shape[1] + 1):
                matrix_copy[i][j] = self[i][j] * number

        return matrix_copy

    def __multiply_two_matrices(self, other: 'Matrix'):
        if self.shape[1] != other.shape[0]:
            raise Exception("Количество столбцов первой матрицы должно совпадать с количеством строк второй")

        multiplied_matrix = Matrix(self.shape[0], self.shape[1])

        for row_index_first_matrix in range(1, self.shape[0] + 1):
            for col_index_second_matrix in range(1, other.shape[1] + 1):
                for multiply_index in range(1, self.shape[1] + 1):
                    multiplied_matrix[row_index_first_matrix][col_index_second_matrix] += (
                            self[row_index_first_matrix][multiply_index] * other[multiply_index][col_index_second_matrix])

        return multiplied_matrix

    def __mul__(self, other) -> 'Matrix':
        if isinstance(other, Matrix):
            return self.__multiply_two_matrices(other)
        if isinstance(other, numeric):
            return self.__multiply_by_number(other)

        raise Exception("Умножение на данный объект некорректно (тип)")

    def trace(self):
        if self.shape[1] != self.shape[0]:
            raise Exception("След существует только у квадратной матрицы")

        trace = 0

        for i in range(1, self.shape[0] + 1):
            trace += self[i][i]

        return trace

    def determinant(self):
        pass
