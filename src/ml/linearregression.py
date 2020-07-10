from functools import reduce
import numpy as np

iterations = 1500
alpha = 0.0000001


def run_lin_reg(theta: np.ndarray, x_matrix: np.ndarray, y: np.ndarray) -> np.ndarray:
    x_matrix = x_matrix.copy()
    theta = theta.copy()
    y = y.copy()
    if reduce(lambda a, b: a * b, x_matrix.shape) < 100:
        x_matrix = np.concatenate((np.ones((len(y), 1)), x_matrix), axis=1)
        return brute_force_lin_reg(x_matrix, y)
    if len(x_matrix[0]) >= 2:  # is this the best way to tell if some features need to be normalized?
        x_matrix = feature_normalize(x_matrix)
    x_matrix = np.concatenate((np.ones((len(y), 1)), x_matrix), axis=1)
    return gradient_descent(theta, x_matrix, y)


def brute_force_lin_reg(x_matrix, y):
    """
    Ax=b -> x = (A^T * A)^-1 * A^T * b
    """
    return np.dot(np.dot(np.linalg.pinv(np.dot(x_matrix.T, x_matrix)), x_matrix.T), y)


def gradient_descent(theta, x_matrix, y):
    m = len(y)
    for _ in range(iterations):
        theta = theta - (alpha/m)*(np.dot(x_matrix.T, np.dot(x_matrix, theta)-y))
    return theta


def compute_cost(x_matrix, y, theta):
    # J = (1/2m)*sum(1:m){(h(x)-y)^2}
    return 1 / (2 * len(y)) * np.sum(np.square(np.dot(x_matrix, theta)-y))


def feature_normalize(x_matrix):
    for i in range(x_matrix.shape[1]):
        values = x_matrix[:, i]
        mean = np.mean(values)
        std = np.std(values)
        x_matrix[:, i] = (values - mean) / std
    return x_matrix
