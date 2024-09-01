import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score, silhouette_score, make_scorer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv('penguins.csv')

# Select features
X = df[['culmen_length_mm','culmen_depth_mm','flipper_length_mm',
        'body_mass_g','sex']]


# Encode categorical features
label_encoder = LabelEncoder()
X = X.apply(label_encoder.fit_transform)

# Split the data into training and testing sets
X_train, X_test = train_test_split(X, test_size=0.1, shuffle=True, random_state=42)

# Define the parameter grid for GridSearchCV
param_grid = {
    'n_clusters': [2, 3, 4, 5],  # You can adjust the range of clusters as needed
    'n_init': [5, 10, 15],
    'max_iter': [100, 200, 300],
    'tol': [1e-4, 1e-3, 1e-2]
}

# Create KMeans instance
kmeans = KMeans(random_state=42)
##Best Parameters: {'max_iter': 100, 'n_clusters': 2, 'n_init': 5, 'tol': 0.0001}
##Davies-Bouldin Score: 0.8581537100580884
##Silhouette Score: 0.42072955471645357
##hàm tinh trung binh de do do toi uu 
def combined_score(y_true, y_pred):
    db = davies_bouldin_score(y_true, y_pred)
    silhouette = silhouette_score(y_true, y_pred)
    return np.mean([db, silhouette])

combined_scorer = make_scorer(combined_score)

# Tạo đối tượng GridSearchCV
grid_search = GridSearchCV(kmeans, param_grid, scoring=combined_scorer, cv=5)


# Fit the model to the training data
grid_search.fit(X_train)

# Mo hinh voi thamso tot nhat
best_params = grid_search.best_params_
print("Best Parameters:", best_params)

# lay mo hinh tot nhat
best_kmeans = grid_search.best_estimator_

# Du doan nhan
labels = best_kmeans.predict(X_test)

# Evaluate the model
db_score = davies_bouldin_score(X_test, labels)
print(f'Davies-Bouldin Score: {db_score}')
silhouette_avg = silhouette_score(X_test, labels)
print(f'Silhouette Score: {silhouette_avg}')
