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
        self.data = []
        self.indices = []
        self.indptr = [0] * (self.shape[0] + 1)  # Начинаем с 0

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

        start = self.indptr[row_key - 1]
        end = self.indptr[row_key]

        left, right = start, end
        while left < right:
            mid = (left + right) // 2
            if self.indices[mid] == col_key:
                return self.data[mid]
            elif self.indices[mid] < col_key:
                left = mid + 1
            else:
                right = mid

        return 0

    def __setitem__(self, key: tp.Tuple[int, int], value: numeric):
        """
        Присваивание значений в матрице
        """
        row_key, col_key = key

        if row_key <= 0 or col_key <= 0 or row_key > self.shape[0] or col_key > self.shape[1]:
            raise KeyError("Index out of range")

        start = self.indptr[row_key - 1]
        end = self.indptr[row_key]

        left, right = start, end
        pos = start
        while left < right:
            mid = (left + right) // 2
            if self.indices[mid] == col_key:
                if value != 0:
                    #обнова текущего значения
                    self.data[mid] = value
                else:
                    #удаляем элемент
                    del self.data[mid]
                    del self.indices[mid]
                    for i in range(row_key, len(self.indptr)):
                        self.indptr[i] -= 1
                return
            elif self.indices[mid] < col_key:
                left = mid + 1
            else:
                right = mid
        pos = left

        if value != 0:
            #вставляем новый элемент
            self.data.insert(pos, value)
            self.indices.insert(pos, col_key)
            for i in range(row_key, len(self.indptr)):
                self.indptr[i] += 1

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
        Сложение двух разреженных матриц в формате CSR.
        :param other: Матрица той же размерности.
        :return: Новая матрица, представляющая сумму self и other.
        """
        if self.shape != other.shape:
            raise ValueError("Матрицы должны быть одного размера")

        result = Matrix(self.shape[0], self.shape[1])
        result.indptr = [0]

        for row in range(self.shape[0]):
            row_data = {}
            # Обработка текущей строки из self
            for idx in range(self.indptr[row], self.indptr[row + 1]):
                col = self.indices[idx]
                val = self.data[idx]
                row_data[col] = val

            # Обработка текущей строки из other
            for idx in range(other.indptr[row], other.indptr[row + 1]):
                col = other.indices[idx]
                val = other.data[idx]
                if col in row_data:
                    row_data[col] += val
                else:
                    row_data[col] = val

            # Сортировка по столбцам для поддержания порядка
            sorted_cols = sorted(row_data.keys())
            for col in sorted_cols:
                val = row_data[col]
                if val != 0:
                    result.indices.append(col)
                    result.data.append(val)
            result.indptr.append(len(result.data))

        return result

    def __neg__(self) -> 'Matrix':
        """
        :return: Матрица, элементы которой противоположны
        """
        new_matrix = Matrix(self.shape[0], self.shape[1])

        for i in range(1, self.shape[0] + 1):
            for j in range(1, self.shape[1] + 1):
                new_matrix[i, j] = -self[i, j]

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

        multiplied_matrix = Matrix(self.shape[0], other.shape[1])

        m, k = self.shape
        _, n = other.shape

        for i in range(1, m + 1):
            start_a, end_a = self.indptr[i - 1], self.indptr[i]

            row_data = self.data[start_a:end_a]
            row_indices = self.indices[start_a:end_a]

            result_row = {}
            other_col_dict = other.build_column_dict()

            for j in other_col_dict:
                col_data, col_indices = other_col_dict[j]

                dot_product = 0
                a_idx, b_idx = 0, 0

                while a_idx < len(row_data) and b_idx < len(col_data):
                    if row_indices[a_idx] == col_indices[b_idx]:
                        dot_product += row_data[a_idx] * col_data[b_idx]
                        a_idx += 1
                        b_idx += 1
                    elif row_indices[a_idx] < col_indices[b_idx]:
                        a_idx += 1
                    else:
                        b_idx += 1

                if dot_product != 0:
                    result_row[j] = dot_product

            multiplied_matrix.indices.extend([idx for idx in sorted(result_row)])
            multiplied_matrix.data.extend([result_row[idx] for idx in sorted(result_row)])
            for row_indptr in range(i, self.shape[0] + 1):
                multiplied_matrix.indptr[row_indptr] += len(result_row)

        return multiplied_matrix

    def build_column_dict(self):
        col_dict = {}
        for row in range(1, self.shape[0] + 1):
            start, end = self.indptr[row - 1], self.indptr[row]
            for idx, value in zip(self.indices[start: end], self.data[start: end]):
                if idx not in col_dict:
                    col_dict[idx] = ([], [])
                col_dict[idx][0].append(value)
                col_dict[idx][1].append(row)
        return col_dict

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

    def transpose(self):
        new_matrix = Matrix(self.shape[1], self.shape[0])
        for i in range(1, self.shape[0] + 1):
            for j in range(1, self.shape[1] + 1):
                new_matrix[j, i] = self[i, j]
        return new_matrix