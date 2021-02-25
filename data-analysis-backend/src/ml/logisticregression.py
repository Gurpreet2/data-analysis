import numpy as np
from scripts.load_mnist import read_images_labels
import logging

logging = logging.getLogger(__name__)

iterations = 50  # 1000
map_feature_degree = 6


class NumberGuessingGame(object):
    def __init__(self):
        train_images, train_labels = read_images_labels('../data/mnist/train-images-idx3-ubyte',
                                                        '../data/mnist/train-labels-idx1-ubyte', 5000)
        test_images, test_labels = read_images_labels('../data/mnist/t10k-images-idx3-ubyte',
                                                      '../data/mnist/t10k-labels-idx1-ubyte', 1000)
        self.trained_theta = train(train_images, train_labels, 10, 0.1)
        p = predict_one_vs_all(self.trained_theta, test_images)
        logging.info(f'Accuracy is {np.sum(p == test_labels)*100/len(test_images)}')

    def guess_number(self, x_matrix):
        return predict_one_vs_all(self.trained_theta, x_matrix)


def sigmoid(x):
    return 1/(1+np.power(np.e, -x))


def cost_function(theta, x_matrix, y, lambdah):
    """
    regularized logistic regression cost function
    Do not need to pass in l, only if calculating gradient
    """
    # J = (-1/m)*sum(i=1:m){y*log(h)+(1-y)log(1-h)} + (lambda/2m)*sum(j=1:n){theta.j^2}
    y = y.reshape((len(y), 1))
    # theta = theta.reshape((len(theta), 1))
    m = len(y)
    cost = (-1/m) * (np.dot(np.log(sigmoid(np.dot(x_matrix, theta))).T, y)
                     + np.dot(np.log(1-sigmoid(np.dot(x_matrix, theta))).T, 1-y)) + (lambdah/2/m)*np.sum(theta[1:]**2)
    # gradient = (1/m)*np.dot(x_matrix.T, sigmoid(np.dot(x_matrix, theta))-y) \
    #            + lambdah/m*(np.vstack((np.zeros(1), theta[1:]))**2)
    return cost


def get_gradient(theta, x_matrix, y, lambdah):
    y = y.reshape((len(y), 1))
    m = len(y)
    theta = theta.reshape((len(theta), 1))
    return (1 / m) * np.dot(x_matrix.T, sigmoid(np.dot(x_matrix, theta)) - y) \
        + lambdah / m * np.vstack((np.zeros(1), theta[1:]))


def gradient_descent(theta, x_matrix, y, lambdah, **kwargs):
    """
    gradient = (1/m)*sum(i=1:m){(h-y)*x.j} + lambda/m*theta, where theta[0] = 0
    """
    y = y.reshape((len(y), 1))
    m = len(y)
    theta = theta.reshape((len(theta), 1))
    local_iterations = kwargs['iterations'] if 'iterations' in kwargs else iterations
    for _ in range(local_iterations):
        gradient = (1 / m) * np.dot(x_matrix.T, sigmoid(np.dot(x_matrix, theta)) - y) \
                   + lambdah / m * np.vstack((np.zeros(1), theta[1:]))
        theta = theta - gradient
    return theta


def train(x_matrix, y, num_labels, lambdah):
    m = x_matrix.shape[0]
    n = x_matrix.shape[1]
    all_theta = np.zeros((num_labels, n+1))
    x_matrix = np.hstack((np.ones((m, 1)), x_matrix))
    for k in range(num_labels):
        initial_theta = np.zeros((n+1, 1))
        # this fmin doesn't work... couldn't get past like 34.86 percent...
        # theta = fmin(func=cost_function, args=(x_matrix, y == k, lambdah), x0=initial_theta,
        #              maxiter=50, full_output=False)
        theta = gradient_descent(initial_theta, x_matrix, y == k, lambdah).T
        all_theta[k] = theta  # .reshape((1, theta.shape[1]))
    return all_theta


def predict_one_vs_all(all_theta, x_matrix):
    if len(x_matrix.shape) == 1:
        x_matrix = x_matrix.reshape((1, len(x_matrix)))
    m = x_matrix.shape[0]
    # num_labels = all_theta.shape[0]
    # p = np.zeros((m, 1))
    x_matrix = np.hstack((np.ones((m, 1)), x_matrix))
    # [vals, p] = max(X*all_theta', [], 2);
    preds = sigmoid(np.dot(x_matrix, all_theta.T))
    # for i in range(len(preds)):
    #     p[i] = preds[i].index(max(preds[i]))
    p = np.argmax(preds, axis=1)
    return p


def predict(theta, x_matrix):
    return np.floor(sigmoid(np.dot(x_matrix, theta)) + 0.5)


def map_feature(x1, x2):
    out = np.ones((x1.shape[0], 1))
    for i in range(1, map_feature_degree+1):
        for j in range(0, i+1):
            out = np.hstack((out, ((x1**(i-j))*(x2**j)).reshape(len(out), 1)))
    return out
