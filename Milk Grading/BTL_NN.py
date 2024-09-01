import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder,LabelBinarizer
from sklearn import metrics
from sklearn.metrics import recall_score, precision_score, f1_score


df = pd.read_csv('milknew.csv')
X = df[['pH','Temprature','Taste','Odor','Fat ','Turbidity','Colour']]
y = df['Grade']


label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)


# Phân chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True,random_state=42)
s = StandardScaler()
X_train = s.fit_transform(X_train)
X_test = s.fit_transform(X_test)


# Tạo và huấn luyện mô hình Perceptron
pla = MLPClassifier(max_iter=300,hidden_layer_sizes=(100,100),alpha=0.0001,learning_rate='constant',solver='adam',activation='relu',random_state=42)
pla.fit(X_train, y_train)

# Dự đoán kết quả trên tập kiểm tra
y_predict = pla.predict(X_test)
accuracy_NN=metrics.accuracy_score(y_test, y_predict)
Precision_NN=precision_score(y_test, y_predict, average='micro')
Recall_NN=recall_score(y_test, y_predict, average='micro')
F1_NN=f1_score(y_test, y_predict, average='micro')
# Đánh giá độ chính xác
print('\nThông số neural_network:')
print('Accuracy Score:', metrics.accuracy_score(y_test, y_predict))
print('Độ chính xác Precision:', precision_score(y_test, y_predict, average='micro'))
print('Độ chính xác Recall:', recall_score(y_test, y_predict, average='micro'))
print('Độ chính xác F1:', f1_score(y_test, y_predict, average='micro'))


import matplotlib.pyplot as plt
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy_NN, Precision_NN,
                  Recall_NN, F1_NN]

fig, ax = plt.subplots()
bars = ax.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
plt.title('Neural Network')
plt.xlabel('Các độ đo')
plt.ylabel('Tỷ lệ')

# Display numerical values on top of each bar
for bar, value in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.01, f'{value:.3f}', fontsize=9)

plt.show()
