import numpy as np
##công thức tính Hàm sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
##công thức tính Đạo Hàm sigmoid
##sigmoid_derivative(x)=sigmoid(x)*(1−sigmoid(x))= x*(1−x)
def sigmoid_derivative(x):
    return x * (1 - x)

class NeuralNetwork:
    def __init__(self, input_size=7, hidden_size=(7,7), output_size=3, learning_rate=0.01, max_iter=300, random_state=42):
##số lượng đặc trưng hoặc biến đầu vào trong mỗi mẫu dữ liệu
        self.input_size = input_size
##  các lớp ẩn
        self.hidden_size = sum(hidden_size) if isinstance(hidden_size, tuple) else hidden_size
## số lượng neuron trong lớp đầu ra của mạng
        self.output_size = output_size
##tốc độ học tập
        self.learning_rate = learning_rate
##số lượng vòng lặp tối đa
        self.max_iter = max_iter
        self.random_state = random_state

        # Initialize weights and biases with small random values
        np.random.seed(self.random_state)
##Lấy w đầu vào
        self.weights_input_hidden = np.random.randn(self.input_size, self.hidden_size) * 0.01
##Lây b lớp ẩn
        self.bias_hidden = np.zeros((1, self.hidden_size))
        self.weights_hidden_output = np.random.randn(self.hidden_size, self.output_size) * 0.01
        self.bias_output = np.zeros((1, self.output_size))

#Hàm softmax để chuyển đổi đầu ra của lớp đầu ra thành một phân phối xác suất
    def softmax(self, x):
 # Tránh overflow bằng cách trừ giá trị lớn nhất từ mỗi phần tử
##keepdims:kích thước của trục có được giữ nguyên sau khi áp dụng hàm không
##axis=1:áp dụng hàm theo chiều ngang (theo hàng) của mảng, giảm kích thước của mảng theo chiều ngang.
        exp_x = np.exp(x - np.max(x, axis=1, keepdims=True))
# Chuẩn hóa để có xác suất tổng cộng bằng 1
        return exp_x / np.sum(exp_x, axis=1, keepdims=True)
##Hàm log_loss để đo lường hiệu suất của mô hình phân loại dựa trên xác suất dự đoán của mô hình và nhãn thực tế
    def log_loss(self, predicted_output, y):
        m = len(y)# Số lượng mẫu trong tập dữ liệu
# Tính log loss dựa trên xác suất dự đoán (predicted_output) và nhãn thực tế (y)
        log_loss = -np.sum(np.log(predicted_output[np.arange(m), y] + 1e-10)) / m
        return log_loss

    def fit(self, X, y):
        for epoch in range(self.max_iter):
          
            hidden_layer_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
            hidden_layer_output = sigmoid(hidden_layer_input)

            output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
            predicted_output = self.softmax(output_layer_input)

            # tính toán giá trị mất mát (loss) của mô hình 
            loss = self.log_loss(predicted_output, y)

            # tính toán sai số (error) của mô hình trong quá trình backward pass
            error = predicted_output
##Điều chỉnh giá trị của error bằng cách giảm 1 từ giá trị tương ứng với lớp thực tế của mỗi mẫu dữ liệu
            error[np.arange(len(y)), y] -= 1

            hidden_layer_error = error.dot(self.weights_hidden_output.T)
            hidden_layer_delta = hidden_layer_error * sigmoid_derivative(hidden_layer_output)

            # Update weights and biases
            self.weights_hidden_output -= hidden_layer_output.T.dot(error) * self.learning_rate
            self.bias_output -= np.sum(error, axis=0, keepdims=True) * self.learning_rate
            self.weights_input_hidden -= X.T.dot(hidden_layer_delta) * self.learning_rate
            self.bias_hidden -= np.sum(hidden_layer_delta, axis=0, keepdims=True) * self.learning_rate

    def predict(self, X):
        hidden_layer_input = np.dot(X, self.weights_input_hidden) + self.bias_hidden
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights_hidden_output) + self.bias_output
        predicted_output = self.softmax(output_layer_input)
        return np.argmax(predicted_output, axis=1)



