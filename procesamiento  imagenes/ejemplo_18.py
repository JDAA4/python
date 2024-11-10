import numpy as np
def mae (y_true, y_pred):
    n = len(y_true)
    error = 0
    for i in range(n):
        error += abs(y_true[i] - y_pred[i])
    return error/n

def mse (y_true, y_pred):
    n = len(y_true)
    squared_error = 0
    for i in range(n):
        squared_error += (y_true[i] - y_pred[i])**2
    return squared_error/n

def rmse (y_true, y_pred):
    squared_error = mse(y_true, y_pred)
    return np.sqrt(squared_error)