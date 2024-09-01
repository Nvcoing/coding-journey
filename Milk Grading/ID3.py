import numpy as np
##Đại diện cho một nút trong cây quyết định như internal,leaf node
class Node:
    def __init__(self, feature=None, threshold=None, value=None, left=None, right=None, result=None):
        self.feature = feature        # chỉ số của đặc trưng sẽ được sử dụng để phân chia dữ liệu tại nút hiện tại của cây quyết định.
        self.threshold = threshold    # ngưỡng giá trị cho việc phân chia dữ liệu tại nút hiện tại
        self.value = value            # nhãn lớp được gán cho nút lá
        self.left = left              # cây con bên trái của nút hiện tại
        self.right = right            # cây con bên phải của nút hiện tại
        self.result = result          # nhãn lớp được gán cho nút lá

class SimpleDecisionTree:
    def __init__(self, max_depth=None, min_samples_split=2, min_samples_leaf=1):
##Độ sâu tối đa của cây
        self.max_depth = max_depth
##Số lượng mẫu tối thiểu cần thiết để phân chia một nút nội bộ:
        self.min_samples_split = min_samples_split
##Số lượng mẫu tối thiểu cần có ở một nút lá        
        self.min_samples_leaf = min_samples_leaf
        self.tree = None

    def fit(self, X, y):
        self.tree = self._build_tree(X, y, depth=0)

    def predict(self, X):
        return np.array([self._predict_tree(x, self.tree) for x in X])
#Xây dụng cây quyết định
    def _build_tree(self, X, y, depth):
##trả về một danh sách chứa số lượng hàng và cột của ma trận
        num_samples, num_features = X.shape
##tạo một mảng chứa các giá trị duy nhất của mảng y
        unique_classes = np.unique(y)

#Điều kiện này kiểm tra xem có chỉ một lớp duy nhất trong tập dữ liệu và cây đã đạt đến độ sâu tối đa chưa
        if len(unique_classes) == 1 or (self.max_depth is not None and depth == self.max_depth):
            return Node(value=unique_classes[0], result=unique_classes[0])

# Nếu num_samples nhỏ hơn min_samples_split, nó sẽ trả về một nút lá 
        if num_samples < self.min_samples_split:
##np.bincount(y): Hàm này đếm số lần xuất hiện của mỗi giá trị trong mảng y.
            return Node(value=unique_classes[np.argmax(np.bincount(y))], result=unique_classes[np.argmax(np.bincount(y))])

        #  chọn điểm chia tốt nhất cho tập dữ liệu tại nút hiện tại
        best_feature, best_threshold = self._find_best_split(X, y)

        # nếu best_feature không tìm thấy điểm chia nào thì giữ nguyên value,result
        if best_feature is None:
            return Node(value=unique_classes[np.argmax(np.bincount(y))], result=unique_classes[np.argmax(np.bincount(y))])

        # Nếu left_indices thỏa mãn thì return true , và ngược lại 
        left_indices = X[:, best_feature] <= best_threshold
##lấy phủ định của left_indices
        right_indices = ~left_indices
##xây dựng tiếp cây con bên trái  với độ sâu + thêm 1
        left_subtree = self._build_tree(X[left_indices], y[left_indices], depth + 1)
##xây dựng tiếp cây con bên phải 
        right_subtree = self._build_tree(X[right_indices], y[right_indices], depth + 1)

        return Node(feature=best_feature, threshold=best_threshold, left=left_subtree, right=right_subtree)

    def _find_best_split(self, X, y):
##trả về một danh sách chứa số lượng hàng và cột của ma trận
        num_samples, num_features = X.shape
##nếu num_samples <  min_samples_split trả về none,none ngược lại thì thôi
        if num_samples < self.min_samples_split:
            return None, None
#mảng chứa các giá trị duy nhất của mảng y
        class_values = np.unique(y)
        best_gini = float('inf')
        best_feature, best_threshold = None, None

        for feature in range(num_features):
#Tạo một mảng chứa các giá trị duy nhất từ cột đặc trưng thứ feature trong ma trận X
            unique_values = np.unique(X[:, feature])
#(Vị trí cuối + Vị trí đầu)/2
            thresholds = (unique_values[:-1] + unique_values[1:]) / 2

            for threshold in thresholds:
#nhãn tương ứng với các mẫu thuộc tập dữ liệu của cây con bên trái 
                left_indices = X[:, feature] <= threshold
                right_indices = ~left_indices
##tính toán độ không thuần khiết Gini impurity
                gini = self._gini_impurity(y[left_indices], y[right_indices])

                if gini < best_gini:
                    best_gini = gini
                    best_feature = feature
                    best_threshold = threshold

        return best_feature, best_threshold

    def _gini_impurity(self, left_labels, right_labels):
##tính toán kích thước (số lượng mẫu) của cây con bên trái,phải
        left_size = len(left_labels)
        right_size = len(right_labels)
        total_size = left_size + right_size
#Nếu total_size = 0, điều này ngụ ý rằng nút hiện tại không có dữ liệu,
#không có mẫu nào thuộc vào nó sau khi phân chia.
        if total_size == 0:
            return 0
##tính toán tỷ lệ số lượng mẫu
        p_left = left_size / total_size
        p_right = right_size / total_size
##Dùng hàm Gini
        gini_left = 1.0 - sum((np.sum(left_labels == c) / left_size) ** 2 for c in np.unique(left_labels))
        gini_right = 1.0 - sum((np.sum(right_labels == c) / right_size) ** 2 for c in np.unique(right_labels))

        gini = p_left * gini_left + p_right * gini_right

        return gini
##hàm entropy(không lấy vì không tối ưu bàng gini)  
##        entropy_left = -sum((np.sum(left_labels == c) / left_size) * np.log2(np.sum(left_labels == c) / left_size) for c in np.unique(left_labels) if np.sum(left_labels == c) > 0)
##        entropy_right = -sum((np.sum(right_labels == c) / right_size) * np.log2(np.sum(right_labels == c) / right_size) for c in np.unique(right_labels) if np.sum(right_labels == c) > 0)
##
##        entropy = p_left * entropy_left + p_right * entropy_right
##  
##        return entropy

    def _predict_tree(self, x, node):
##Kiểm tra có nhãn không 
        if node.result is not None:
            return node.result
#Kiểm tra giá trị tại nhãn có <= ngưỡng giá trị không có thì trả bên trái và ngược lại
        if x[node.feature] <= node.threshold:
            return self._predict_tree(x, node.left)
        else:
            return self._predict_tree(x, node.right)

