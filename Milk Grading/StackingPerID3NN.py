import numpy as np


class MyLogisticRegression:
    def __init__(self, learning_rate=0.01, num_iterations=100, regularization_strength=1):
        self.learning_rate = learning_rate
        self.num_iterations = num_iterations
        self.regularization_strength = regularization_strength
        self.theta = None
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def fit(self, X, y):
        # Add a column of ones for the bias term
        X = np.insert(X, 0, 1, axis=1)
        
        # Initialize weights
        num_samples, num_features = X.shape
        self.theta = np.zeros(num_features)
        
        for _ in range(self.num_iterations):
            # Calculate the predicted probabilities
            y_pred = self.sigmoid(np.dot(X, self.theta))
            
            # Calculate the gradient with regularization
            gradient = (np.dot(X.T, (y_pred - y)) + self.regularization_strength * np.concatenate(([0], self.theta[1:]))) / num_samples
            
            # Update weights using gradient descent
            self.theta -= self.learning_rate * gradient
    
    def predict(self, X):
        # Add a column of ones for the bias term
        X = np.insert(X, 0, 1, axis=1)
        
        # Predict probabilities
        y_pred_proba = self.sigmoid(np.dot(X, self.theta))
        
        # Convert probabilities to binary predictions (0 or 1)
        y_pred = np.round(y_pred_proba)
        
        return y_pred


    
import numpy as np

class StackingClassifier:
    def __init__(self, base_classifiers, meta_classifier, cv=5):
        self.base_classifiers = base_classifiers
        self.meta_classifier = meta_classifier
        self.cv = cv
        self.stack_models = []

    def fit(self, X, y):
        num_samples = X.shape[0]
        fold_size = num_samples // self.cv

        for i in range(self.cv):
            # Split the data into train and validation sets
            start_idx = i * fold_size
            end_idx = (i + 1) * fold_size
            validation_X = X[start_idx:end_idx]
            validation_y = y[start_idx:end_idx]

            train_X = np.concatenate([X[:start_idx], X[end_idx:]])
            train_y = np.concatenate([y[:start_idx], y[end_idx:]])

            # Train the base classifiers on the training set
            for name, clf in self.base_classifiers:
                clf_instance = clf.__class__()
                clf_instance.fit(train_X, train_y)
                self.stack_models.append((name, clf_instance))

            # Create features for the meta-classifier using the validation set
            stack_features = np.column_stack([clf.predict(validation_X) for _, clf in self.stack_models])

            # Fit the meta-classifier using the validation set predictions from base classifiers
            self.meta_classifier.fit(stack_features, validation_y)

        return self

    def predict(self, X):
        stack_features = np.column_stack([clf.predict(X) for _, clf in self.stack_models])
        return self.meta_classifier.predict(stack_features)





