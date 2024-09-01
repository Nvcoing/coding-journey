import numpy as np

class Perceptron:
    def __init__(self, learning_rate=0.01, n_iterations=1000):
        self.learning_rate = learning_rate
        self.n_iterations = n_iterations
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        # Initialize weights and bias
        self.weights = np.zeros(X.shape[1])
        self.bias = 0

        for _ in range(self.n_iterations):
            for xi, target in zip(X, y):
                # Update weights and bias
                update = self.learning_rate * (target - self.predict(xi))
                self.weights += update * xi
                self.bias += update

    def predict(self, X):
        # Compute the weighted sum and apply the step function
        return np.where(np.dot(X, self.weights) + self.bias > 0, 1, 0)


