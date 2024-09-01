import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split,KFold
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
from sklearn.linear_model import LinearRegression, Lasso, Ridge

# Đọc dữ liệu từ file CSV
data = pd.read_csv("insurance.csv")

# Chia thành features (X) và target variable (y)
X = data[['age', 'sex', 'bmi', 'children', 'smoker', 'region']]
y = data['charges']

# Sử dụng LabelEncoder cho các cột 'sex', 'smoker', 'region'
label_encoder = LabelEncoder()
for column in X.columns:
    if X[column].dtype == 'object':
        X.loc[:, column] = label_encoder.fit_transform(X[column])
# Lưu dữ liệu sau khi mã hóa vào file
np.savetxt("BTL1.txt", X, fmt='%.2f', delimiter='|')
# Chia tập dữ liệu thành 70% huấn luyện và 30% kiểm thử
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)
print("X_train\n",X_train)
print("Y_train\n",y_train)
print("X_test\n",X_test)
print("Y_test\n",y_test)


# Hồi quy tuyến tính
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
y_pred_linear = linear_reg.predict(X_test)

# LASSO
lasso_reg = Lasso(alpha=0.1)  # Điều chỉnh alpha tùy thuộc vào bài toán
lasso_reg.fit(X_train, y_train)
y_pred_lasso = lasso_reg.predict(X_test)

# RIDGE
ridge_reg = Ridge(alpha=0.1)  # Điều chỉnh alpha tùy thuộc vào bài toán
ridge_reg.fit(X_train, y_train)
y_pred_ridge = ridge_reg.predict(X_test)

# K-Fold Cross Validation
k = 5
kf = KFold(n_splits=k, random_state=None)

max_error = float('inf')

i = 1

def NSE(y_test, y_pred):
    return (1 - (np.sum(y_test - y_pred) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))

def error(y, y_pred):
    return np.mean(np.abs(y - y_pred))

for train_index, test_index in kf.split(X_train):
    X_train_kfold, X_test_kfold = X_train.iloc[train_index], X_train.iloc[test_index]
    y_train_kfold, y_test_kfold = y_train.iloc[train_index], y_train.iloc[test_index]

    lr = LinearRegression()
    lr.fit(X_train_kfold, y_train_kfold)
    Y_Pred_train = lr.predict(X_train_kfold)
    Y_Pred_test = lr.predict(X_test_kfold)
    error_sum = error(y_train_kfold, Y_Pred_train) + error(y_test_kfold, Y_Pred_test)

    if error_sum < max_error:
        max_error = error_sum
        best_iteration = i
        best_model = lr
    i = i + 1
# In kết quả cuối cùng

Y_Pred_test_final = best_model.predict(X_test)
Y_test_final = y_test

print("\nDùng k-fold:\n")
# Đánh giá  mô hình tốt nhất từ K-Fold Cross Validation
print("LinearRegression:")
print("\nNSE: ", NSE(Y_test_final, Y_Pred_test_final))
print('R2: %.2f' % r2_score(Y_test_final, Y_Pred_test_final))
print("MAE: ", mean_absolute_error(Y_test_final, Y_Pred_test_final))
print("RMSE: ", mean_squared_error(Y_test_final, Y_Pred_test_final))
print("Mô hình tốt nhất là lần chia thứ", best_iteration )
print("Lỗi nhỏ nhất là", max_error)


print("\nKhông dùng k-fold:\n")
# Đánh giá chất lượng mô hình
def evaluate_model(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    nse = NSE(y_true, y_pred)
    return r2, nse, mae, rmse

# Đánh giá mô hình Hồi quy tuyến tính
linear_eval = evaluate_model(y_test, y_pred_linear)
print("Linear Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*linear_eval))

# Đánh giá mô hình LASSO
lasso_eval = evaluate_model(y_test, y_pred_lasso)
print("\nLASSO Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*lasso_eval))

# Đánh giá mô hình RIDGE
ridge_eval = evaluate_model(y_test, y_pred_ridge)
print("\nRIDGE Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*ridge_eval))
