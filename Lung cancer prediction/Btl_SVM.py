import pandas as pd
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelBinarizer
from sklearn import metrics
from sklearn.metrics import recall_score, precision_score, f1_score

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
X_train, X_test, Y_train, Y_test = train_test_split(X_data_encoded, y_data, test_size=0.3, shuffle=True, random_state=42)

# Standardize the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
##Các tham số thử vào SVM
###param_grid = {
##    'C': [0.1, 1, 10],
##    'kernel': ['linear', 'rbf', 'poly'],
##    'degree': [2, 3, 4],
##    'gamma': ['scale', 'auto'],
##    'random_state': [42]
##}
##scoring_methods lấy các độ đo tối ưu nhất
#scoring_methods = ['accuracy', 'precision', 'recall', 'f1']

# Tạo GridSearchCV cho thư viện sklearn để tìm ra tham số tối ưu nhất
#SVC(C=1, degree=2, kernel='linear', random_state=42)
grid_search = SVC(C=1, degree=2, kernel='linear', random_state=42)
grid_search.fit(X_train_scaled, Y_train.ravel())

# Get the best SVM model
#svm_classifier = grid_search.best_estimator_
svm_classifier = grid_search
# Make predictions on the test set
Y_pre = svm_classifier.predict(X_test_scaled)

# Print evaluation metrics
print('Accuracy Score:', metrics.accuracy_score(Y_test, Y_pre))
print('Precision Score:', precision_score(Y_test, Y_pre, average='weighted'))
print('Recall Score:', recall_score(Y_test, Y_pre, average='weighted'))
print('F1 Score:', f1_score(Y_test, Y_pre, average='weighted'))
#print('Best Model:', grid_search.best_estimator_)



import matplotlib.pyplot as plt
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [metrics.accuracy_score(Y_test, Y_pre), precision_score(Y_test, Y_pre, average='micro'),
                  recall_score(Y_test, Y_pre, average='micro'), f1_score(Y_test, Y_pre, average='micro')]

fig, ax = plt.subplots()
bars = ax.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
plt.title('Support vector machine')
plt.xlabel('Các độ đo')
plt.ylabel('Tỷ lệ')

# Display numerical values on top of each bar
for bar, value in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.01, f'{value:.2f}', fontsize=9)

plt.show()

