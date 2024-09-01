import pandas as pd
import numpy as np
from sklearn.linear_model import Perceptron
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
pla = Perceptron(alpha=0.00001,eta0=0.1,max_iter=50,penalty='elasticnet',tol=0.01,random_state=42)
pla.fit(X_train, y_train)

# Dự đoán kết quả trên tập kiểm tra
y_predict = pla.predict(X_test)
accuracy_Perceptron=metrics.accuracy_score(y_test, y_predict)
Precision_Perceptron=precision_score(y_test, y_predict, average='micro')
Recall_Perceptron=recall_score(y_test, y_predict, average='micro')
F1_Perceptron=f1_score(y_test, y_predict, average='micro')
# Đánh giá độ chính xác
print('\nThông số Perceptron:')
print('Accuracy Score:', metrics.accuracy_score(y_test, y_predict))
print('Độ chính xác Precision:', precision_score(y_test, y_predict, average='micro'))
print('Độ chính xác Recall:', recall_score(y_test, y_predict, average='micro'))
print('Độ chính xác F1:', f1_score(y_test, y_predict, average='micro'))

import matplotlib.pyplot as plt
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy_Perceptron, Precision_Perceptron,
                  Recall_Perceptron, F1_Perceptron]

fig, ax = plt.subplots()
bars = ax.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
plt.title('Perceptron')
plt.xlabel('Các độ đo')
plt.ylabel('Tỷ lệ')

# Display numerical values on top of each bar
for bar, value in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.01, f'{value:.3f}', fontsize=9)

plt.show()
