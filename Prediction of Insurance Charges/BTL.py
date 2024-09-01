import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np
from sklearn.model_selection import KFold
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

# Chia tập dữ liệu thành 70% huấn luyện và 30% kiểm thử
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=False)

# Lưu dữ liệu sau khi mã hóa vào file
np.savetxt("BTL1.txt", X, fmt='%.2f', delimiter='|')

# Hồi quy tuyến tính
linear_reg = LinearRegression()
linear_reg.fit(X_train, y_train)
y_pred_linear = linear_reg.predict(X_test)
y_linear=np.array(y_test)
# LASSO
lasso_reg = Lasso()
lasso_reg.fit(X_train, y_train)
y_pred_lasso = lasso_reg.predict(X_test)
y_lasso=np.array(y_test)
# RIDGE
ridge_reg = Ridge()
ridge_reg.fit(X_train, y_train)
y_pred_ridge = ridge_reg.predict(X_test)
y_ridge=np.array(y_test)
# K-Fold Cross Validation
k = 5
kf = KFold(n_splits=k, random_state=None)

max_error = float('inf')
best_model = None
best_iteration = 0

def NSE(y_test, y_pred):
    return (1 - (np.sum(y_pred - y_test) ** 2) / np.sum((y_test - np.mean(y_test)) ** 2))

def error(y, y_pred):
    return np.mean(np.abs(y - y_pred))

for iteration, (train_index, test_index) in enumerate(kf.split(X_train)):
    X_train_kfold, X_test_kfold = X_train.iloc[train_index], X_train.iloc[test_index]
    y_train_kfold, y_test_kfold = y_train.iloc[train_index], y_train.iloc[test_index]

    lr = LinearRegression()
    lr.fit(X_train_kfold, y_train_kfold)
    Y_Pred_train = lr.predict(X_train_kfold)
    Y_Pred_test = lr.predict(X_test_kfold)
    error_sum = error(y_train_kfold, Y_Pred_train) + error(y_test_kfold, Y_Pred_test)

    if error_sum < max_error:
        max_error = error_sum
        best_iteration = iteration
        best_model = lr

# In kết quả cuối cùng
X_test_final = X_test
Y_Pred_test_final = best_model.predict(X_test_final)
Y_test_final = np.array(y_test)

# Đánh giá chất lượng mô hình
def evaluate_model(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    nse = NSE(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    rmse = mean_squared_error(y_true, y_pred)
    return r2, nse, mae, rmse

# Đánh giá mô hình Hồi quy tuyến tính
linear_eval = evaluate_model(y_test, y_pred_linear)
print("Linear Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*linear_eval))
print("Thuc te      Du Doan      Chech Lech")
for i in range(0,len(y_linear)):
    print("%.2f"%y_linear[i]," ",y_pred_linear[i]," ",abs(y_linear[i]-y_pred_linear[i]))
# Đánh giá mô hình LASSO
lasso_eval = evaluate_model(y_test, y_pred_lasso)
print("\nLASSO Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*lasso_eval))
print("Thuc te      Du Doan      Chech Lech")
for i in range(0,len(y_lasso)):
    print("%.2f"%y_lasso[i]," ",y_pred_lasso[i]," ",abs(y_lasso[i]-y_pred_lasso[i]))
# Đánh giá mô hình RIDGE
ridge_eval = evaluate_model(y_test, y_pred_ridge)
print("\nRIDGE Regression Evaluation:")
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*ridge_eval))
print("Thuc te      Du Doan      Chech Lech")
for i in range(0,len(y_ridge)):
    print("%.2f"%y_ridge[i]," ",y_pred_ridge[i]," ",abs(y_ridge[i]-y_pred_ridge[i]))

# Kết quả cuối cùng với mô hình tốt nhất từ K-Fold Cross Validation
print("\nFinal Evaluation with Best Model:")
final_eval = evaluate_model(Y_test_final, Y_Pred_test_final)
print("R2: {:.4f}, NSE: {:.4f}, MAE: {:.4f}, RMSE: {:.4f}".format(*final_eval))
print("Mô hình tốt nhất là lần chia thứ", best_iteration + 1)
print("Lỗi nhỏ nhất là", max_error)
print("Thuc te      Du Doan      Chech Lech")
for i in range(0,len(Y_test_final)):
    print("%.2f"%Y_test_final[i]," ",Y_Pred_test_final[i]," ",abs(Y_test_final[i]-Y_Pred_test_final[i]))

