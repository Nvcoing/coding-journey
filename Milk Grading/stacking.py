import pandas as pd
import numpy as np
from sklearn.linear_model import Perceptron,LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.ensemble import StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier


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
    ('decision_tree', DecisionTreeClassifier(criterion='gini',max_depth = 10,min_samples_split = 2,min_samples_leaf=1 ,random_state=42)),
    ('mlp', MLPClassifier(max_iter=500,hidden_layer_sizes=(100,100),alpha=0.0001,learning_rate='constant',solver='adam',activation='relu',random_state=42)),
    ('perceptron', Perceptron(alpha=0.00001,eta0=0.1,max_iter=50,penalty='elasticnet',tol=0.01,random_state=42))
]

# Mô hình cuối cùng (meta-classifier)
meta_classifier = LogisticRegression(random_state=42,C=1,penalty='l2',solver='lbfgs',max_iter=100,class_weight=None)

# Tạo StackingClassifier
##estimators:danh sách công cụ ước tính
##final_estimator:công cụ ước tính cuối(một model meta)
#stack_method:gọi cho mỗi công cụ ước tính cơ sở
#nếu 'auto', nó sẽ cố gắng gọi, cho mỗi công cụ ước tính, 'predict_proba'hoặc 'decision_function'theo 'predict'thứ tự đó.
##n_jobs:Số lượng công việc phải chạy song song tất cả estimators
stacking_classifier = StackingClassifier(estimators=base_classifiers, final_estimator=meta_classifier, cv=5,stack_method='auto',n_jobs=None)

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

    
