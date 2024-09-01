import tkinter as tk
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

class ClusterPredictionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Cluster Prediction App")

        # Create input text boxes
        self.entry_labels = []
        self.input_data = []
        self.num_dimensions = 3  # Đặt số chiều của vector dữ liệu

        for i in range(self.num_dimensions):
            label = tk.Label(master, text=f"Dimension {i+1}:")
            entry = tk.Entry(master)
            label.grid(row=i, column=0, sticky=tk.E)
            entry.grid(row=i, column=1)
            self.entry_labels.append(label)
            self.input_data.append(entry)

        # Create predict button
        predict_button = tk.Button(master, text="Predict", command=self.predict_clusters)
        predict_button.grid(row=self.num_dimensions, column=0, columnspan=2)

        # Display predicted label
        self.label_result = tk.Label(master, text="")
        self.label_result.grid(row=self.num_dimensions + 1, column=0, columnspan=2)

        # Display evaluation metrics
        self.label_silhouette = tk.Label(master, text="")
        self.label_silhouette.grid(row=self.num_dimensions + 2, column=0, columnspan=2)

        self.label_davies_bouldin = tk.Label(master, text="")
        self.label_davies_bouldin.grid(row=self.num_dimensions + 3, column=0, columnspan=2)

    def predict_clusters(self):
        # Lấy dữ liệu từ text boxes
        input_values = [float(entry.get()) for entry in self.input_data]
        data_point = np.array(input_values).reshape(1, -1)

        # Mô hình phân cụm (ví dụ K-Means)
        kmeans = KMeans(n_clusters=3)  # Đặt số lượng cụm tùy ý
        # Thực hiện phân cụm
        kmeans.fit(data_point)
        predicted_label = kmeans.predict(data_point)[0]

        # Hiển thị kết quả
        self.label_result.config(text=f"Predicted Label: {predicted_label}")

        # Tính toán độ đo đánh giá chất lượng mô hình
        silhouette_score = metrics.silhouette_score(data_point, kmeans.labels_)
        davies_bouldin_score = metrics.davies_bouldin_score(data_point, kmeans.labels_)

        # Hiển thị độ đo đánh giá chất lượng mô hình
        self.label_silhouette.config(text=f"Silhouette Score: {silhouette_score}")
        self.label_davies_bouldin.config(text=f"Davies-Bouldin Score: {davies_bouldin_score}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClusterPredictionApp(root)
    root.mainloop()
