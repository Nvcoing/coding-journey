import numpy as np

class SimplePerceptron:
    def __init__(self, learning_rate=0.01, max_epochs=100, penalty=None, alpha=0.01, tol=0.001):
##tham số tốc độ học tập        
        self.learning_rate = learning_rate
## Số lần truyền tối đa trên dữ liệu huấn luyện
        self.max_epochs = max_epochs
##Hệ số chính quy  sử dụng để kiểm soát việc overfitting.        
        self.penalty = penalty
##Hằng số nhân số hạng chính quy nếu sử dụng chính quy.        
        self.alpha = alpha
##Tiêu chí dừng lại khi hôi tụ
        self.tol = tol
##w:trọng số
        self.weights = None
##b:độ lệch hay w0       
        self.bias = None

    def fit(self, X, y):
##lấy số lượng đặc trưng trong dữ liệu đầu vào X
        num_features = X.shape[1]
##Lấy w(trọng số) từ num_features và gán = 0        
        self.weights = np.zeros(num_features)
##b=0
        self.bias = 0
##Số lần lập lại
        for epoch in range(self.max_epochs):
##lặp qua mỗi hàng (mỗi mẫu) trong ma trận đầu vào X
            for i in range(X.shape[0]):
##giá trị kích hoạt=w*Xi+b
                activation = np.dot(self.weights, X[i]) + self.bias
##Dự đoán là 0 hay 1
                prediction = 1 if activation >= 0 else 0
##tốc độ học tập nhân Chênh lệch giữa giá trị thực tế và dự đoán
##VD nếu prediction=1 và yi=1 thì update = 0 =>mô hình dự đoán đúng và 0 update nữa
                update = self.learning_rate * (y[i] - prediction)
##w=w0+giá trị cập nhật*Xi
                self.weights += update * X[i]
##b=b0+giá trị cập nhật
                self.bias += update

#Kiểm tra xem có hôi tụ không
            if np.max(np.abs(update * X[i])) < self.tol:
                break

    def predict(self, X):
##1 if np.dot(self.weights, x) + self.bias >= 0 else 0:
##Nếu giá trị kích hoạt lớn hơn hoặc bằng 0, thì dự đoán là 1,
##ngược lại dự đoán là 0.
        predictions = [1 if np.dot(self.weights, x) + self.bias >= 0 else 0 for x in X]
        return np.array(predictions)
    


