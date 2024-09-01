import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder
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

# Encode the categorical target variable
label_encoder = LabelEncoder()
y_data = label_encoder.fit_transform(y_data)

# One-hot encode categorical features
X_data = pd.get_dummies(X_data, columns=['GENDER', 'SMOKING', 'YELLOW_FINGERS', 'ANXIETY', 'CHRONIC DISEASE'])

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X_data, y_data, test_size=0.3, shuffle=True)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Reshape the target variables
Y_train = np.ravel(Y_train)
Y_test = np.ravel(Y_test)

param_grid = {
    'C': [0.001, 0.01, 0.1, 1, 10, 100],
    'solver': ['liblinear', 'newton-cg', 'lbfgs', 'sag', 'saga'],
    'max_iter': [100, 500, 1000],
    'penalty' : ['l1','l2'],
    'max_iter': [100],
    'class_weight':['balanced']
}
scoring_methods = ['accuracy', 'precision', 'recall', 'f1']

grid_search = GridSearchCV(LogisticRegression(random_state=42), param_grid,scoring = scoring_methods,refit='f1', cv=5)
grid_search.fit(X_train_scaled, Y_train.ravel())

log_reg = grid_search.best_estimator_

# Make predictions on the test set
Y_pred = log_reg.predict(X_test_scaled)

# Print evaluation metrics
print('Accuracy Score:', metrics.accuracy_score(Y_test, Y_pred))
print('Precision Score:', precision_score(Y_test, Y_pred, average='weighted', zero_division=1))
print('Recall Score:', recall_score(Y_test, Y_pred, average='weighted', zero_division=1))
print('F1 Score:', f1_score(Y_test, Y_pred, average='weighted', zero_division=1))
print('Mô hình tốt nhất: ',log_reg)
