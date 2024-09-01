import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
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
pla = DecisionTreeClassifier(criterion='gini',max_depth = 10,min_samples_split = 2,min_samples_leaf=1 ,random_state=42)
pla.fit(X_train, y_train)

# Dự đoán kết quả trên tập kiểm tra
y_predict = pla.predict(X_test)
accuracy_id3=metrics.accuracy_score(y_test, y_predict)
Precision_id3=precision_score(y_test, y_predict, average='micro')
Recall_id3=recall_score(y_test, y_predict, average='micro')
F1_id3=f1_score(y_test, y_predict, average='micro')
# Đánh giá độ chính xác
print('\nThông số cây ID3:')
print('Accuracy Score:', metrics.accuracy_score(y_test, y_predict))
print('Độ chính xác Precision:', precision_score(y_test, y_predict, average='micro'))
print('Độ chính xác Recall:', recall_score(y_test, y_predict, average='micro'))
print('Độ chính xác F1:', f1_score(y_test, y_predict, average='micro'))


import matplotlib.pyplot as plt
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy_id3, Precision_id3,
                  Recall_id3, F1_id3]

fig, ax = plt.subplots()
bars = ax.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
plt.title('ID3')
plt.xlabel('Các độ đo')
plt.ylabel('Tỷ lệ')

# Display numerical values on top of each bar
for bar, value in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.01, f'{value:.3f}', fontsize=9)

plt.show()
