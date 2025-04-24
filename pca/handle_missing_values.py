from matrix import Matrix


def handle_missing_values(X:'Matrix') ->'Matrix':
    """
    Вход: матрица данных X (n×m) с возможными NaN
    Выход: матрица данных X_filled (n×m) без NaN
    """
    mean_values = [0 for _ in range(X.shape[1])]

    for col in range(1, X.shape[1] + 1):
        colum_sum = 0
        colum_not_null_count = 0
        for row in range(1, X.shape[0] + 1):
            if X[row, col] is not None:
                colum_sum += X[row, col]
                colum_not_null_count += 1
        if colum_sum == 0:
            for row in range(1, X.shape[0] + 1):
                X[row, col] = 0
        else:
            for row in range(1, X.shape[0] + 1):
                if X[row, col] is not None:
                    continue
                X[row, col] = colum_sum / colum_not_null_count

    return X
