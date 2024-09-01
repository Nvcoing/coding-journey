import pandas as pd
import numpy as np
from StackingPerID3NN import StackingClassifier,MyLogisticRegression
from ID3 import SimpleDecisionTree
from neural_network import NeuralNetwork
from Perceptron import SimplePerceptron
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
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

# Tạo các mô hình cơ bản
base_classifiers = [
    ('decision_tree', SimpleDecisionTree()),
    ('mlp', NeuralNetwork()),
    ('perceptron', SimplePerceptron())
]

# Mô hình cuối cùng (meta-classifier)
meta_classifier = MyLogisticRegression()

# Tạo StackingClassifier
stacking_classifier = StackingClassifier(base_classifiers,meta_classifier)

# Huấn luyện mô hình
stacking_classifier.fit(X_train, y_train)

# Dự đoán trên tập kiểm tra
y_pred = stacking_classifier.predict(X_test)

# Đánh giá độ chính xác
accuracy_stacking = accuracy_score(y_test, y_pred)
Precision_stacking=precision_score(y_test, y_pred, average='micro')
recall_score_stacking=recall_score(y_test, y_pred, average='micro')
f1_score_stacking=f1_score(y_test, y_pred, average='micro')
print("Thông số Stacking:")
print(f"Accuracy: {accuracy_stacking}")
print('Precision:', Precision_stacking)
print('Recall:', recall_score_stacking)
print('F1:', f1_score_stacking)

   
import matplotlib.pyplot as plt
metrics_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
metrics_values = [accuracy_stacking, Precision_stacking,
                  recall_score_stacking, f1_score_stacking]

fig, ax = plt.subplots()
bars = ax.bar(metrics_names, metrics_values, color=['blue', 'green', 'orange', 'red'])
plt.title('Mô hình kết hợp Stacking')
plt.xlabel('Các độ đo')
plt.ylabel('Tỷ lệ')

# Display numerical values on top of each bar
for bar, value in zip(bars, metrics_values):
    ax.text(bar.get_x() + bar.get_width() / 2 - 0.1, bar.get_height() + 0.01, f'{value:.3f}', fontsize=9)
plt.ion()
plt.show()   

    
