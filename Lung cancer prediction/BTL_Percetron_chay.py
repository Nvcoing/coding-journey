import pandas as pd
import numpy as np
from PercepTron import Perceptron
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

# Define the parameter grid for SVC


# Create a Perceptron object
perceptron_model = Perceptron()

# Fit the Perceptron model
perceptron_model.fit(X_train_scaled, Y_train.ravel())

# Make predictions on the test set
Y_pre = perceptron_model.predict(X_test_scaled)


# Print evaluation metrics
print('Accuracy Score:', metrics.accuracy_score(Y_test, Y_pre))
print('Precision Score:', precision_score(Y_test, Y_pre, average='weighted', zero_division=1.0))
print('Recall Score:', recall_score(Y_test, Y_pre, average='weighted', zero_division=1.0))
print('F1 Score:', f1_score(Y_test, Y_pre, average='weighted', zero_division=1.0))
