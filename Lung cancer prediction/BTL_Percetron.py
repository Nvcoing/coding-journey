import pandas as pd
import numpy as np
from sklearn.linear_model import Perceptron
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn import metrics
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.model_selection import GridSearchCV

# Load the dataset
df = pd.read_csv('survey lung cancer.csv')

# Extract features (X_data) and target variable (y_data)
X_data = df[['GENDER', 'AGE', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'PEER_PRESSURE', 'CHRONIC DISEASE',
             'FATIGUE ', 'ALLERGY ', 'WHEEZING', 'ALCOHOL CONSUMING', 'COUGHING', 'SHORTNESS OF BREATH',
             'SWALLOWING DIFFICULTY', 'CHEST PAIN']]
y_data = df['LUNG_CANCER']

# Encode the categorical target variable using LabelBinarizer for binary classification
label_binarizer = LabelBinarizer()
y_data = label_binarizer.fit_transform(y_data)

# One-hot encode categorical variables
X_data_encoded = pd.get_dummies(X_data, columns=['GENDER'])

# Split the data into training and testing sets with a random state for reproducibility
X_train, X_test, Y_train, Y_test = train_test_split(X_data_encoded, y_data, test_size=0.3, shuffle=True)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the parameter grid for Perceptron
param_grid = {
    'penalty': [None, 'l1', 'l2', 'elasticnet'],
    'alpha': [0.0001, 0.001, 0.01, 0.1, 1, 10],
    'max_iter': [100, 500, 1000, 5000],
    'eta0': [0.1, 0.01, 0.001]
}

scoring_methods = {
    'accuracy': 'accuracy',
    'precision': 'precision_micro',
    'recall': 'recall_micro',
    'f1': 'f1_micro',
}


# Create a GridSearchCV object for Perceptron
grid_search = GridSearchCV(Perceptron(random_state=42), param_grid, scoring=scoring_methods, refit='f1', cv=5,error_score='raise',  # This will raise an error for invalid parameter combinations
    return_train_score=False,
    verbose=2,
    n_jobs=-1,)
grid_search.fit(X_train_scaled, Y_train.ravel())

# Get the best Perceptron model
perceptron_model = grid_search.best_estimator_

# Make predictions on the test set
Y_pre = perceptron_model.predict(X_test_scaled)

# Print evaluation metrics
print('Accuracy Score:', metrics.accuracy_score(Y_test, Y_pre))
print('Precision Score:', precision_score(Y_test, Y_pre, average='micro'))
print('Recall Score:', recall_score(Y_test, Y_pre, average='micro'))
print('F1 Score:', f1_score(Y_test, Y_pre, average='micro'))
print('Best Model:', perceptron_model)
