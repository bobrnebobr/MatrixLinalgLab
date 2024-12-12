import typing as tp
from .common import numeric


class MatrixRow:
    """Отдельный класс для хранения строк матрицы и для удобства"""
    def __init__(self, values: tp.Dict[int, numeric], length: int) -> None:
        """
        Инициализация класса
        :param values: словарь вида индекс: значение для хранения строки в разреженном виде
        :param length: длина строки, количество столбцов матрицы
        """
        if len(values) > length:
            raise Exception("Значений в строке больше заданной ее длины")

        self.values = values
        self.length = length

    def __getitem__(self, key: int) -> numeric:
        """
        Метод для удобства получения элемента строки
        """
        if key > self.length or key <= 0:
            raise KeyError("Неправильный ключ")

        if key in self.values:
            return self.values[key]
        else:
            return 0

    def __setitem__(self, key: int, value: numeric) -> None:
        """Метод для того, чтобы задавать значения в строке по ключу"""
        if key > self.length or key <= 0:
            raise KeyError("Неправильный ключ")

        if value != 0:
            self.values[key] = value

    def __str__(self) -> str:
        """Вид строки для ее вывода"""
        items = []

        for i in range(1, self.length + 1):
            if i in self.values:
                items.append(self.values[i])
            else:
                items.append(0)

        return "\t".join(map(str, items))

    def __bool__(self) -> bool:
        return bool(self.values)
