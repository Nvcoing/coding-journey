import numpy as np
class SVC:
    def __init__(self, learning_rate=0.001, num_epochs=1000, C=1.0):
##        self là tham số định nghĩa trong lớp.
        self.learning_rate = learning_rate
##        learning_rate: tốc độ học 
        self.num_epochs = num_epochs
##        num_epochs: số lần lặp lại quá trình huấn luyện trên toàn bộ dữ liệu.
        self.C = C
##        C: Tham số điều chỉnh độ chấp nhận của mô hình đối với sự vi phạm của dữ liệu.
        self.weights = None
##        weights: vector trọng số 
        self.bias = None
##        bias: hệ số chêch lệch

    def fit(self, X, y):
##  lấy kích thước của mảng X, gồm số mẫu và số đặc trưng.
        num_samples, num_features = X.shape
## num_samples là số hàng, num_features là số cột của mảng
        y = np.where(y <= 0, -1, 1)
##Hàm np.where sẽ trả về một mảng mới, trong đó các phần tử của y thỏa mãn điều kiện y <= 0 thay bằng -1, còn không thỏa mãn thay bằng 1
## gán cho weights một mảng NumPy chứa toàn bộ các phần tử có giá trị là 0, với kích thước (số lượng phần tử) là num_features.
        self.weights = np.zeros(num_features)
##Thêm hệ số b vào sẽ khiến cho mô hình linh hoạt hơn một chút bằng cách bỏ ràng
buộc đường thẳng quan hệ giữa đầu ra và đầu vào luôn đi qua gốc toạ độ
        self.bias = 0

        # Đào tạo mô hình SVM bàng cách sử dụng gradient descent
        for epoch in range(self.num_epochs):
            for i in range(num_samples):
##đảm bảo rằng mọi điểm dữ liệu đều nằm đúng phía của ranh giới quyết định và thoả mãn đến ranh giới quyết định.
                condition = y[i] * (np.dot(X[i], self.weights) - self.bias) >= 1
##phân loại đúng và nằm đúng phía của siêu phẳng
                if not condition:
##phân loại sai hoặc nằm giữa hai siêu phẳng và nằm trong vùng biên
                    self.weights -= self.learning_rate * (2 * self.C * self.weights - np.dot(X[i], y[i]))
##w=w0-n(2*c*w-xi*yi)
                    self.bias -= self.learning_rate * y[i]
##b=b0-n*y
##điều chỉnh w và b để cố gắng đạt được điều kiện
    def predict(self, X):
        return np.where(np.dot(X, self.weights) - self.bias >= 0, 1, -1)
##(X*w-b)>=0 =>1 
