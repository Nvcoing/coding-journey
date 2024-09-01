import pandas as pd
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score, precision_score, f1_score

# Load the dataset
df = pd.read_csv('milknew.csv')

# Select features and target variable
X = df[['pH', 'Temprature', 'Taste', 'Odor', 'Fat ', 'Turbidity', 'Colour']]
y = df['Grade']

# Label Encoding for the target variable
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Train-test split and standardization
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Create a Perceptron model
perceptron = Perceptron(random_state=42)

# Define the hyperparameter grid to search
param_grid = {
    'penalty': [None, 'l1', 'l2', 'elasticnet'],
    'alpha': [0.0001, 0.001, 0.01, 0.1, 1],
    'max_iter': [50,100, 200, 300, 400, 500],
    'eta0': [1,0.1, 0.01, 0.001, 0.0001],
    'tol':[1e-3,0.01,0.001]
}
scoring_methods = {
    'accuracy': 'accuracy',
    'precision': 'precision_micro',
    'recall': 'recall_micro',
    'f1': 'f1_micro',
}

# Create a GridSearchCV object
grid_search = GridSearchCV(perceptron, param_grid, scoring=scoring_methods,refit='f1', cv=5)

# Fit the GridSearchCV object to the training data
grid_search.fit(X_train_scaled, y_train)

# Get the best parameters and best estimator
best_params = grid_search.best_params_
best_perceptron = grid_search.best_estimator_

# Make predictions on the test set using the best model
y_pred = best_perceptron.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Best Parameters: {best_params}')
print(f'Accuracy on Test Set: {accuracy}')
print('Precision Score:', precision_score(y_test, y_pred, average='micro'))
print('Recall Score:', recall_score(y_test, y_pred, average='micro'))
print('F1 Score:', f1_score(y_test, y_pred, average='micro'))
