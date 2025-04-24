import unittest
from matrix import Matrix
from pca.gauss_solver import gauss_solver

class TestGaussSolver(unittest.TestCase):
    def test_unique_solution_simple(self):
        """Простая система 2x2 с единственным решением"""
        A = Matrix(2, 2)
        A[1, 1] = 1
        A[1, 2] = 2
        A[2, 1] = 3
        A[2, 2] = 4

        b = Matrix(2, 1)
        b[1, 1] = 5
        b[2, 1] = 11

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0][1, 1], 1.0)
        self.assertAlmostEqual(solutions[0][2, 1], 2.0)

    def test_unique_solution_complex(self):
        """Система 3x3 с единственным решением"""
        A = Matrix(3, 3)
        A[1, 1] = 2
        A[1, 2] = 1
        A[1, 3] = -1
        A[2, 1] = -3
        A[2, 2] = -1
        A[2, 3] = 2
        A[3, 1] = -2
        A[3, 2] = 1
        A[3, 3] = 2

        b = Matrix(3, 1)
        b[1, 1] = 8
        b[2, 1] = -11
        b[3, 1] = -3

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0][1, 1], 2.0)
        self.assertAlmostEqual(solutions[0][2, 1], 3.0)
        self.assertAlmostEqual(solutions[0][3, 1], -1.0)

    def test_infinite_solutions_rank_2(self):
        """Система 3x3 с рангом 2 (бесконечно много решений)"""
        A = Matrix(3, 3)
        A[1, 1] = 1
        A[1, 2] = 2
        A[1, 3] = 3
        A[2, 1] = 4
        A[2, 2] = 5
        A[2, 3] = 6
        A[3, 1] = 7
        A[3, 2] = 8
        A[3, 3] = 9

        b = Matrix(3, 1)
        b[1, 1] = 6
        b[2, 1] = 15
        b[3, 1] = 24

        solutions = gauss_solver(A, b)
        self.assertGreater(len(solutions), 1)  # Частное решение + базисные (больше 1-го)

        # Проверяем, что частное решение удовлетворяет системе
        particular = solutions[0]
        for i in range(1, 4):
            left = sum(A[i, j] * particular[j, 1] for j in range(1, 4))
            self.assertAlmostEqual(left, b[i, 1])

        # Проверяем, что базисные решения удовлетворяют однородной системе
        for basis in solutions[1:]:
            for i in range(1, 4):
                left = sum(A[i, j] * basis[j, 1] for j in range(1, 4))
                self.assertAlmostEqual(left, 0)

    def test_infinite_solutions_rank_1(self):
        """Система 3x3 с рангом 1"""
        A = Matrix(3, 3)
        A[1, 1] = 1
        A[1, 2] = 2
        A[1, 3] = 3
        A[2, 1] = 2
        A[2, 2] = 4
        A[2, 3] = 6
        A[3, 1] = 3
        A[3, 2] = 6
        A[3, 3] = 9

        b = Matrix(3, 1)
        b[1, 1] = 6
        b[2, 1] = 12
        b[3, 1] = 18

        solutions = gauss_solver(A, b)
        #print(*solutions)
        self.assertEqual(len(solutions), 3)  # Частное + 2 базисных

    def test_no_solution_contradiction(self):
        """Несовместная система (противоречивые уравнения)"""
        A = Matrix(2, 2)
        A[1, 1] = 1
        A[1, 2] = 1
        A[2, 1] = 1
        A[2, 2] = 1

        b = Matrix(2, 1)
        b[1, 1] = 1
        b[2, 1] = 2

        with self.assertRaises(ValueError):
            gauss_solver(A, b)

    def test_no_solution_zero_row(self):
        """Несовместная система (нулевая строка с ненулевой правой частью)"""
        A = Matrix(3, 3)
        A[1, 1] = 1
        A[1, 2] = 0
        A[1, 3] = 0
        A[2, 1] = 0
        A[2, 2] = 1
        A[2, 3] = 0
        A[3, 1] = 0
        A[3, 2] = 0
        A[3, 3] = 0

        b = Matrix(3, 1)
        b[1, 1] = 1
        b[2, 1] = 1
        b[3, 1] = 1

        with self.assertRaises(ValueError):
            gauss_solver(A, b)

    def test_diagonal_matrix(self):
        """Диагональная матрица"""
        A = Matrix(3, 3)
        A[1, 1] = 2
        A[2, 2] = 3
        A[3, 3] = 4

        b = Matrix(3, 1)
        b[1, 1] = 4
        b[2, 1] = 9
        b[3, 1] = 16

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0][1, 1], 2.0)
        self.assertAlmostEqual(solutions[0][2, 1], 3.0)
        self.assertAlmostEqual(solutions[0][3, 1], 4.0)

    def test_triangular_matrix(self):
        """Треугольная матрица"""
        A = Matrix(3, 3)
        A[1, 1] = 1
        A[1, 2] = 2
        A[1, 3] = 3
        A[2, 1] = 0
        A[2, 2] = 1
        A[2, 3] = 2
        A[3, 1] = 0
        A[3, 2] = 0
        A[3, 3] = 1

        b = Matrix(3, 1)
        b[1, 1] = 6
        b[2, 1] = 3
        b[3, 1] = 1

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0][1, 1], 1.0)
        self.assertAlmostEqual(solutions[0][2, 1], 1.0)
        self.assertAlmostEqual(solutions[0][3, 1], 1.0)

    def test_zero_matrix_zero_vector(self):
        """Нулевая матрица с нулевым вектором (бесконечно много решений)"""
        A = Matrix(2, 2)
        b = Matrix(2, 1)

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 2)  #2 базисных

    def test_complex_numbers(self):
        """Система с комплексными числами"""
        A = Matrix(2, 2)
        A[1, 1] = 1
        A[1, 2] = -1
        A[2, 1] = 1
        A[2, 2] = 1

        b = Matrix(2, 1)
        b[1, 1] = 1j
        b[2, 1] = 1

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(0.5, solutions[0][1, 1].real)
        self.assertAlmostEqual(0.5, solutions[0][1, 1].imag)
        self.assertAlmostEqual(0.5, solutions[0][2, 1].real)
        self.assertAlmostEqual(-0.5, solutions[0][2, 1].imag)

    def test_ill_conditioned_matrix(self):
        """Плохо обусловленная матрица (проверка устойчивости)"""
        A = Matrix(2, 2)
        A[1, 1] = 1
        A[1, 2] = 1
        A[2, 1] = 1
        A[2, 2] = 1.0001

        b = Matrix(2, 1)
        b[1, 1] = 2
        b[2, 1] = 2.0001

        solutions = gauss_solver(A, b)
        self.assertEqual(len(solutions), 1)
        self.assertAlmostEqual(solutions[0][1, 1], 1.0, places=4)
        self.assertAlmostEqual(solutions[0][2, 1], 1.0, places=4)


if __name__ == '__main__':
    unittest.main()