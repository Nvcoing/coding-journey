from sklearn.ensemble import BaggingClassifier
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load sample data (replace with your own data)
data = load_iris()
X, y = data.data, data.target

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define three base models: Perceptron, ID3, Neural Network
perceptron_model = Perceptron()
id3_model = DecisionTreeClassifier()
neural_network_model = MLPClassifier()

# Define the BaggingClassifier with a single base estimator
base_estimator = DecisionTreeClassifier()  # You can choose the base estimator here
bagging_classifier = BaggingClassifier(base_estimator=base_estimator, n_estimators=10, random_state=42)

# Train the model
bagging_classifier.fit(X_train, y_train)

# Predict on the test set
y_pred = bagging_classifier.predict(X_test)

# Evaluate the performance
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')
