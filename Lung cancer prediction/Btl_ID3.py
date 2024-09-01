import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
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
X_train, X_test, Y_train, Y_test = train_test_split(X_data_encoded, y_data, test_size=0.2, shuffle=True, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the parameter grid for DecisionTreeClassifier
param_grid = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [None, 10, 20, 30, 40, 50],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'max_features': [None, 'sqrt', 'log2']
}

scoring_methods = ['accuracy', 'precision', 'recall', 'f1']

# Create a GridSearchCV object for DecisionTreeClassifier
grid_search = GridSearchCV(DecisionTreeClassifier(random_state=42), param_grid, scoring=scoring_methods, refit='f1', cv=5)
grid_search.fit(X_train_scaled, Y_train.ravel())

# Get the best DecisionTreeClassifier model
dt_classifier = grid_search.best_estimator_

# Make predictions on the test set
Y_pre = dt_classifier.predict(X_test_scaled)

# Print evaluation metrics
print('Accuracy Score:', metrics.accuracy_score(Y_test, Y_pre))
print('Precision Score:', precision_score(Y_test, Y_pre, average='weighted'))
print('Recall Score:', recall_score(Y_test, Y_pre, average='weighted'))
print('F1 Score:', f1_score(Y_test, Y_pre, average='weighted'))
print('Best Model:', dt_classifier)
