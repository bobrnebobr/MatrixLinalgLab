from matrix import Matrix

def covariance_matrix(X_centered: 'Matrix') -> 'Matrix':
    """
    Вход: центрированная матрица X_centered (n×m)
    Выход: матрица ковариаций C (m×m)
    """
    n_rows, m_cols = X_centered.shape

    if n_rows == 1:
        raise ValueError('n равно 1 (не можем избежать деления на ноль)')

    C = Matrix(m_cols, m_cols)

    scale = 1/(n_rows-1)

    for i in range(1, m_cols + 1):
        for j in range(1, m_cols + 1):
            res = 0
            for k in range(1, n_rows + 1):
                res += X_centered[k, i]*X_centered[k, j]
            C[i, j] = res*scale

    return C

# expected = Matrix(3, 2)
# expected[1, 1] = -2
# expected[1, 2] = -2
# expected[2, 1] = 0
# expected[2, 2] = 0
# expected[3, 1] = 2
# expected[3, 2] = 2
# print(covariance_matrix(expected))