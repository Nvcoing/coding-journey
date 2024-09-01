import numpy as np
import pandas as pd

class KMeans:
##Khởi tạo đối tượng
    def __init__(self, n_clusters=2, max_iters=100, tol=1e-4, n_init=10):
##    số cụm
        self.n_clusters = n_clusters
##    max_iter:số lần lập lại
        self.max_iters = max_iters
 ##đặc tả giới hạn tuyến tính về sự thay đổi trong hàm mục tiêu để coi mô hình đã hội tụ       
        self.tol = tol
##    xác định số lần chạy
        self.n_init = n_init

    def fit(self, X):
        
##        kiểm tra xem biến X có phải là một đối tượng của lớp pd.DataFrame trong thư viện không
        if isinstance(X, pd.DataFrame):
            X = X.values
##best_centroids: Lưu trữ centroid tốt nhất cho các cụm (clusters).
        best_centroids = None
##best_labels: Lưu trữ nhãn tốt nhất cho mỗi điểm dữ liệu (cluster mà điểm đó được gán vào).
        best_labels = None
##  best_inertia: Lưu trữ giá trị inertia tốt nhất và gán thành vô hạn
##  Inertia là tổng bình phương khoảng cách từ mỗi điểm dữ liệu đến centroid của cụm nó thuộc về.
##Giá trị inertia càng nhỏ, mô hình K-means càng tốt.
        best_inertia = np.inf
##for _ in range(self.n_init): được sử dụng để lặp qua các lần chạy của thuật toán K-means với các điểm khởi tạo ngẫu nhiên khác nhau.
##Biến _ không được sử dụng trong thân vòng lặp(thể hiện rằng bạn không quan tâm đến giá trị cụ thể của biến này)
        for _ in range(self.n_init):
##Tạo ra một mảng chứa self.n_clusters số nguyên ngẫu nhiên từ 0 đến len(X) - 1,
##mỗi số chỉ xuất hiện một lần (do replace=False) từ tập dữ liệu X
            centroids = X[np.random.choice(len(X), self.n_clusters, replace=False)]
##for _ in range(self.max_iters):: Dòng mã này tạo ra một vòng lặp chạy từ 0 đến self.max_iters - 1.
##Biến _ thường được sử dụng khi giá trị của biến không cần thiết và không được sử dụng bên trong vòng lặp.
            for _ in range(self.max_iters):
##Tính nhãn:
##X[:, np.newaxis]: Mở rộng chiều thứ hai của ma trận X
##np.linalg.norm(X[:, np.newaxis] - centroids, axis=2): Tính norm (khoảng cách Euclidean) giữa mỗi điểm dữ liệu và mỗi centroid.
##axis=2 làm cho nó tính norm theo chiều thứ ba, nghĩa là nó tính norm cho mỗi cặp điểm dữ liệu và centroid.
##np.argmin(..., axis=1): Chọn index của centroid có khoảng cách nhỏ nhất đối với mỗi điểm dữ liệu.
##axis=1 làm cho nó chọn index theo chiều thứ hai, nghĩa là chọn index của centroid.
                labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - centroids, axis=2), axis=1)

##Cập nhập tâm mới:
##mean(axis=0): Tính trung bình theo cột cho các điểm dữ liệu trong cụm i.
##Nếu axis=0, nó sẽ lấy trung bình theo chiều dọc (theo cột), cho ra một vectơ trung bình của tất cả các điểm dữ liệu trong cụm.                
                new_centroids = np.array([X[labels == i].mean(axis=0) for i in range(self.n_clusters)])

##Kiểm tra xem hội tụ chưa với độ chênh lệch nhỏ hơn hoặc bằng self.tol
##np.allclose kiểm tra xem tất cả các phần tử trong hai mảng centroids,new_centroids có "gần nhau" hay không.
                if np.allclose(centroids, new_centroids, rtol=self.tol):
                    break

                centroids = new_centroids

##tính toán giá trị inertia trong ngữ cảnh của thuật toán K-means
##Inertia là tổng bình phương khoảng cách từ mỗi điểm dữ liệu đến centroid của cụm nó thuộc về
            inertia = np.sum((X - centroids[labels]) ** 2)

##Kiểm tra xem giá trị inertia của lần chạy hiện tại có nhỏ hơn giá trị inertia tốt nhất đã ghi nhận trước đó hay không.
            if inertia < best_inertia:
                best_inertia = inertia
                best_centroids = centroids
                best_labels = labels

        self.centroids = best_centroids
        self.labels = best_labels

    def predict(self, X):
        # Convert DataFrame to NumPy array if X is a DataFrame
        if isinstance(X, pd.DataFrame):
            X = X.values

        # Assign each data point to the nearest centroid using pre-trained centroids
        return np.argmin(np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2), axis=1)
