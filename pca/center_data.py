from matrix import Matrix


def center_data(X: 'Matrix') -> 'Matrix':
    """
 Вход: матрица данных X (n×m)
 Выход: центрированная матрица X_centered (n×m)
 """
    n_rows, m_cols = X.shape
    colum_means = []

    for col in range(1, m_cols + 1):
        colum_sum = 0
        for row in range(1, n_rows + 1):
            colum_sum += X[row, col]

        mean_val = colum_sum / n_rows
        colum_means.append(mean_val)

    X_centered = Matrix(n_rows, m_cols)
    for row in range(1, n_rows+1):
        for col in range(1, m_cols+1):
            tek_val = X[row, col]
            mean_val_col = colum_means[col-1]
            X_centered[row, col] = tek_val - mean_val_col

    return X_centered
