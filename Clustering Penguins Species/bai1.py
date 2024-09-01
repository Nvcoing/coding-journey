from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score,silhouette_score
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn import metrics
from sklearn import preprocessing
df = pd.read_csv('penguins.csv')
X = df[['culmen_length_mm','culmen_depth_mm','flipper_length_mm','body_mass_g','sex']]


label_encoder = preprocessing.LabelEncoder()
X = X.apply(label_encoder.fit_transform)
X_train, X_test= train_test_split(X, test_size=0.1, shuffle=True)




# Train the Perceptron model
kmeans = KMeans(max_iter = 100, n_clusters = 2, n_init = 5, tol=0.0001,random_state=42)
kmeans.fit(X_train)

# Make predictions on the test set
labels = kmeans.predict(X_test)
db_score = davies_bouldin_score(X_test, labels)
print(f'Davies-Bouldin Score: {db_score}')
silhouette_avg = silhouette_score(X_test, labels)
print(f'Silhouette Score: {silhouette_avg}')

#form
form = Tk()
form.title("Phân Loại khách hàng:")
form.geometry("1000x500")

lable_ten = Label(form, text = "Nhập thông tin cho khách hàng:", font=("Arial Bold", 10), fg="blue")
lable_ten.grid(row = 1, column = 1, padx = 40, pady = 10)

lable_ID = Label(form, text = "ID́:")
lable_ID.grid(row = 2, column = 1, padx = 40, pady = 10)
textbox_ID = Entry(form)
textbox_ID.grid(row = 2, column = 2)
