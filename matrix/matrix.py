import typing as tp
from copy import copy

from .common import numeric


class Matrix:
    """Класс матрицы"""

    def __init__(self, n: int, m: int):
        """
        Инициализация класса
        :param n: количество строк
        :param m: количество столбцов
        """
        self.shape = (n, m)
        self.values = []
        self.row_indices = []
        self.col_indices = []

    def __getitem__(self, key: tp.Tuple[int, int]) -> numeric:
        """
        Получение строки матрицы
        :param row_key: индекс строки матрицы
        :param col_key: индекс столбца матрицы
        :return: строка матрицы по ключу
        """
        row_key, col_key = key

        if row_key <= 0 or col_key <= 0 or row_key > self.shape[0] or col_key > self.shape[1]:
            raise KeyError("Index out of range")

        possible_cols = {}
        for i, row_indice in enumerate(self.row_indices):
            if row_indice == row_key:
                possible_cols[self.col_indices[i]] = i

        if col_key not in possible_cols:
            return 0
        return self.values[possible_cols[col_key]]

    def sparse_index(self, row_key, col_key) -> int:
        if row_key <= 0 or col_key <= 0 or row_key > self.shape[0] or col_key > self.shape[1]:
            raise KeyError("Index out of range")

        possible_cols = {}
        for i, row_indice in enumerate(self.row_indices):
            if row_indice == row_key:
                possible_cols[self.col_indices[i]] = i

        if col_key not in possible_cols:
            return -1
        return possible_cols[col_key]

    def __setitem__(self, key: tp.Tuple[int, int], value: numeric) -> None:
        """
        Задать строку матрицы явно
        :param key:
        :param value:
        :return:
        """
        row_key, col_key = key

        if row_key <= 0 or col_key <= 0 or row_key > self.shape[0] or col_key > self.shape[1]:
            raise KeyError("Index out of range")

        index = self.sparse_index(row_key, col_key)

        if index == -1:
            if value == 0:
                return

            self.row_indices.append(row_key)
            self.col_indices.append(col_key)
            self.values.append(value)
        else:
            if value == 0:
                self.row_indices.pop(index)
                self.col_indices.pop(index)
                self.values.pop(index)
                return

            self.values[index] = value

    def __str__(self) -> str:
        """
        Строковое представление матрицы для вывода в консоль
        """
        result = []
        for i in range(1, self.shape[0] + 1):
            result.append([])
            for j in range(1, self.shape[1] + 1):
                result[-1].append(str(self[i, j]))

        return "\n".join(["\t".join(row) for row in result])

    def __add__(self, other: 'Matrix') -> 'Matrix':
        """
        Сложение матриц
        :param other: Матрица той же размерности, иначе будет вызвана ошибка
        :return: матрица суммы
        """
        if self.shape[0] != other.shape[0] or self.shape[1] != other.shape[1]:
            raise Exception("Матрицы должны быть одного размера")

        matrix_sum = Matrix(self.shape[0], self.shape[1])

        for i in range(1, other.shape[0] + 1):
            for j in range(1, other.shape[1] + 1):
                matrix_sum[i, j] = self[i, j] + other[i, j]

        return matrix_sum

    def __neg__(self) -> 'Matrix':
        """
        :return: Матрица, элементы которой противоположны
        """
        new_matrix = Matrix(self.shape[0], self.shape[1])

        for i in range(len(self.values)):
            new_matrix[self.row_indices[i], self.col_indices[i]] = -self.values[i]

        return new_matrix

    def __sub__(self, other: 'Matrix') -> 'Matrix':
        """
        Вычитание матриц
        :param other: матрица той же размерности, иначе ошибка
        :return: матрица, полученная вычитанием из первой матрицы второй
        """
        return self + (-other)

    def __multiply_by_number(self, number: numeric):
        """
        Метод для умножения матрицы на скаляр
        :param number: скаляр
        :return: матрица, умноженная на скаляр
        """
        matrix_copy = Matrix(self.shape[0], self.shape[1])

        for i in range(1, self.shape[0] + 1):
            for j in range(1, self.shape[1] + 1):
                matrix_copy[i, j] = self[i, j] * number

        return matrix_copy

    def __multiply_two_matrices(self, other: 'Matrix'):
        """
        Метод для умножения матриц между собой
        :param other: матрица, количество строк которой равно количеству столбцов левой матрицы
        :return: произведение матриц
        """
        if self.shape[1] != other.shape[0]:
            raise Exception("Количество столбцов первой матрицы должно совпадать с количеством строк второй")

        multiplied_matrix = Matrix(self.shape[0], self.shape[1])

        for row_index_first_matrix in range(1, self.shape[0] + 1):
            for col_index_second_matrix in range(1, other.shape[1] + 1):
                for multiply_index in range(1, self.shape[1] + 1):
                    multiplied_matrix[row_index_first_matrix, col_index_second_matrix] += (
                            self[row_index_first_matrix, multiply_index] * other[multiply_index,
                    col_index_second_matrix])

        return multiplied_matrix

    def __mul__(self, other) -> 'Matrix':
        """
        Умножение матриц либо на число, либо на матрицу
        :param other: или скаляр, или матрица, удовл. условиям произведения матриц
        :return: матрица
        """
        if isinstance(other, Matrix):
            return self.__multiply_two_matrices(other)
        if isinstance(other, int) or isinstance(other, float) or isinstance(other, complex):
            return self.__multiply_by_number(other)

        raise Exception("Умножение на данный объект некорректно (тип)")

    def __rmul__(self, other) -> 'Matrix':
        return self * other

    def trace(self):
        """
        След матрицы
        :return: след матрицы
        """
        if self.shape[1] != self.shape[0]:
            raise Exception("След существует только у квадратной матрицы")

        trace = 0

        for i in range(1, self.shape[0] + 1):
            trace += self[i, i]

        return trace

    def pop(self, row_key: int, col_key: int) -> 'Matrix':
        if self.shape[0] == 0 or self.shape[1] == 0:
            raise Exception("Нечего удалять буквально")

        new_shape = [self.shape[0] - 1, self.shape[1] - 1]
        new_matrix = Matrix(new_shape[0], new_shape[1])

        for i in range(1, self.shape[0] + 1):
            for j in range(1, self.shape[1] + 1):
                if i != row_key and j != col_key:
                    if i < row_key and j < col_key:
                        new_matrix[i, j] = self[i, j]
                    elif i > row_key and j < col_key:
                        new_matrix[i - 1, j] = self[i, j]
                    elif i < row_key and j > col_key:
                        new_matrix[i, j - 1] = self[i, j]
                    else:
                        new_matrix[i - 1, j - 1] = self[i, j]

        return new_matrix
