import numpy as np

from ml.logisticregression import sigmoid


class NumberGuessingGameNN(object):
    def __init__(self):
        self.input_layer_size = 784
        self.hidden_layer_size = 25
        self.num_labels = 10
        self.alpha = 0.1
        self.lambdah = 2  # lambduh
        self.iterations = 200
        # load my own training set
        self.train_images_filepath = '../data/app/mnist/train-images'
        self.train_labels_filepath = '../data/app/mnist/train-labels'
        try:
            self.train_images = self.load(self.train_images_filepath)
            self.train_labels = self.load(self.train_labels_filepath)
        except FileNotFoundError:
            self.train_images = np.array([])
            self.train_labels = np.array([])
            self.save(self.train_images_filepath, self.train_images)
            self.save(self.train_labels_filepath, self.train_labels)
        # initialize weights and train
        self.theta_1, self.theta_2 = rand_initialize_weights(25, 785), rand_initialize_weights(10, 26)
        if len(self.train_images) > 0:
            for _ in range(self.iterations):
                self.theta_1, self.theta_2 = \
                    train([self.theta_1, self.theta_2], self.train_images, self.train_labels, self.lambdah, self.alpha)

    def guess_number(self, x_matrix):
        return predict([self.theta_1, self.theta_2], x_matrix)

    def train_with_new_data(self, x_matrix: np.ndarray, expected: np.ndarray):
        x_matrix = x_matrix.reshape((1, len(x_matrix)))
        if len(self.train_images) != 0:
            self.train_images = np.vstack((self.train_images, x_matrix))
            self.train_labels = np.hstack((self.train_labels, expected))
        else:
            self.train_images = x_matrix
            self.train_labels = expected
        self.save(self.train_images_filepath, self.train_images)
        self.save(self.train_labels_filepath, self.train_labels)
        self.theta_1, self.theta_2 = train([self.theta_1, self.theta_2], self.train_images, self.train_labels, self.lambdah, self.alpha)
        # for _ in range(iterations):
        #     self.theta_1, self.theta_2 = \
        #     train([self.theta_1, self.theta_2], train_images, train_labels, self.lambdah, self.alpha)

    def save(self, filename, variable):
        np.save(filename, variable, allow_pickle=False)

    def load(self, filename):
        return np.load(filename + '.npy', allow_pickle=False)


def cost_function(thetas, x_mat, y, num_labels, lambdah):
    theta_1 = thetas[0]
    theta_2 = thetas[1]
    m = len(y)
    cost = 0
    a_1 = np.hstack((np.ones((x_mat.shape[0], 1)), x_mat))
    z_2 = np.dot(a_1, theta_1.T)
    a_2 = np.hstack((np.ones((z_2.shape[0], 1)), sigmoid(z_2)))
    z_3 = np.dot(a_2, theta_2.T)
    a_3 = sigmoid(z_3)
    for k in range(num_labels):
        cost += (np.dot(np.log(a_3[:, k]).T, y == k)
                 + np.dot(np.log(1 - a_3[:, k]).T, 1 - (y == k)))
    cost *= -1/m
    cost += (lambdah / 2 / m) * np.sum(theta_2[:, 1:] ** 2)
    cost += (lambdah / 2 / m) * np.sum(theta_1[:, 1:] ** 2)
    return cost


def train(thetas, x_mat, y, lambdah, alpha):

    m = len(y)
    y = y.reshape((len(y), 1))

    theta_1 = thetas[0]
    theta_2 = thetas[1]

    # Backprop
    backprop_grad_1 = np.zeros(theta_1.shape)
    backprop_grad_2 = np.zeros(theta_2.shape)
    for i in range(m):
        # step 1
        a_1 = np.hstack((np.ones(1), x_mat[i, :]))
        z_2 = np.dot(a_1, theta_1.T)
        a_2 = np.hstack((np.ones(1), sigmoid(z_2)))
        z_3 = np.dot(a_2, theta_2.T)
        a_3 = sigmoid(z_3)
        # step 2
        my_y = np.zeros(a_3.shape)
        my_y[y[i]] = 1
        delta_3 = a_3 - my_y
        # other deltas
        delta_2 = np.dot(theta_2.T, delta_3) * a_2 * (1 - a_2)
        backprop_grad_2 += np.dot(np.reshape(delta_3, (len(delta_3), 1)), np.reshape(a_2, (1, len(a_2))))
        backprop_grad_1 += np.dot(np.reshape(delta_2[1:], (len(delta_2[1:]), 1)), np.reshape(a_1, (1, len(a_1))))
    backprop_grad_1 *= 1 / m
    backprop_grad_2 *= 1 / m
    backprop_grad_1 += (lambdah/m) * np.hstack((np.zeros((theta_1.shape[0], 1)), theta_1[:, 1:]))
    backprop_grad_2 += (lambdah/m) * np.hstack((np.zeros((theta_2.shape[0], 1)), theta_2[:, 1:]))

    theta_1 -= alpha*backprop_grad_1
    theta_2 -= alpha*backprop_grad_2

    return theta_1, theta_2


def predict(thetas, x_mat):
    x_mat = x_mat.reshape((1, len(x_mat)))
    theta_1 = thetas[0]
    theta_2 = thetas[1]
    h1 = sigmoid(np.dot(np.hstack((np.ones((x_mat.shape[0], 1)), x_mat)), theta_1.T))
    h2 = sigmoid(np.dot(np.hstack((np.ones((h1.shape[0], 1)), h1)), theta_2.T))
    return np.argmax(h2, axis=1)


def rand_initialize_weights(l_in, l_out):
    epsilon_init = np.sqrt(6) / np.sqrt(l_in + l_out)
    return np.random.random((l_in, l_out)) * 2 * epsilon_init - epsilon_init


def compute_numerical_gradient(thetas, x_mat, y, num_labels, lambdah):
    """
    This method is computationally extremely expensive
    """
    numgrad_1 = np.zeros(thetas[0].shape)
    numgrad_2 = np.zeros(thetas[1].shape)
    perturb_1 = np.zeros(thetas[0].shape)
    perturb_2 = np.zeros(thetas[1].shape)
    e = 0.0001
    for p in range(len(numgrad_1)):
        perturb_1[p] = e
        loss1 = cost_function([thetas[0] - perturb_1, thetas[1]], x_mat, y, num_labels, lambdah)
        loss2 = cost_function([thetas[0] + perturb_1, thetas[1]], x_mat, y, num_labels, lambdah)
        numgrad_1[p] = (loss2 - loss1) / (2*e)
        perturb_1[p] = 0
    for p in range(len(numgrad_2)):
        perturb_2[p] = e
        loss1 = cost_function([thetas[0], thetas[1] - perturb_2], x_mat, y, num_labels, lambdah)
        loss2 = cost_function([thetas[0], thetas[1] + perturb_2], x_mat, y, num_labels, lambdah)
        numgrad_2[p] = (loss2 - loss1) / (2*e)
        perturb_2[p] = 0
    return numgrad_1, numgrad_2
