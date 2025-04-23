import unittest
from matrix import Matrix
from pca.handle_missing_values import handle_missing_values


class HandleMissingValuesTest(unittest.TestCase):
    def test_basic_column_mean(self):
        C = Matrix(3, 3)
        C[1, 1] = 1
        C[1, 2] = 2
        C[1, 3] = 3
        C[2, 1] = 4
        C[2, 2] = None
        C[2, 3] = 6
        C[3, 1] = None
        C[3, 2] = 8
        C[3, 3] = None

        filled = handle_missing_values(C)

        self.assertEqual(filled[1, 1], 1)
        self.assertEqual(filled[1, 2], 2)
        self.assertEqual(filled[1, 3], 3)
        self.assertEqual(filled[2, 1], 4)
        self.assertAlmostEqual(filled[2, 2], 5.0)
        self.assertEqual(filled[2, 3], 6)
        self.assertAlmostEqual(filled[3, 1], 2.5)
        self.assertEqual(filled[3, 2], 8)
        self.assertAlmostEqual(filled[3, 3], 4.5)

    def test_all_none_in_column(self):
        C = Matrix(2, 3)
        C[1, 1] = None
        C[1, 2] = 5
        C[1, 3] = 7
        C[2, 1] = None
        C[2, 2] = 3
        C[2, 3] = None

        filled = handle_missing_values(C)

        self.assertEqual(filled[1, 1], 0)
        self.assertEqual(filled[1, 2], 5)
        self.assertEqual(filled[1, 3], 7)
        self.assertEqual(filled[2, 1], 0)
        self.assertEqual(filled[2, 2], 3)
        self.assertEqual(filled[2, 3], 7.0)

    def test_single_column_matrix(self):
        C = Matrix(4, 1)
        C[1, 1] = 5
        C[2, 1] = None
        C[3, 1] = 15
        C[4, 1] = None

        filled = handle_missing_values(C)

        self.assertEqual(filled[1, 1], 5)
        self.assertAlmostEqual(filled[2, 1], 10.0)
        self.assertEqual(filled[3, 1], 15)
        self.assertAlmostEqual(filled[4, 1], 10.0)

    def test_zeros_handling(self):
        C = Matrix(2, 2)
        C[1, 1] = 0
        C[1, 2] = None
        C[2, 1] = None
        C[2, 2] = 0

        filled = handle_missing_values(C)

        self.assertEqual(filled[1, 1], 0)
        self.assertEqual(filled[1, 2], 0.0)
        self.assertEqual(filled[2, 1], 0.0)
        self.assertEqual(filled[2, 2], 0)
