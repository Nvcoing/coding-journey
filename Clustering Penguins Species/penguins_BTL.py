from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import davies_bouldin_score,silhouette_score
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn import metrics
from sklearn import preprocessing
df = pd.read_csv('penguins.csv')
X = df[['culmen_length_mm','culmen_depth_mm','flipper_length_mm','body_mass_g','sex']]

##Chuẩn hóa dữ liệu bằng label_encoder
label_encoder = preprocessing.LabelEncoder()
X = X.apply(label_encoder.fit_transform)
##Chia dữ liệu thành tập train(0.9) và test(0.1)
X_train, X_test= train_test_split(X, test_size=0.1, shuffle=True)




##Mô hình đào tạo Kmean
##max_iter:số lần lập lại,n_clusters:số lượng cụm,
##n_init:xác định số lần chạy thuật toán với các trung tâm khởi tạo khác nhau
##đặc tả giới hạn tuyến tính về sự thay đổi trong hàm mục tiêu để coi mô hình đã hội tụ and stop
kmeans = KMeans(max_iter = 100, n_clusters = 2, n_init = 5, tol=0.0001,random_state=42)
##Đào tạo mô hình
kmeans.fit(X_train)

#Dự đoán
labels = kmeans.predict(X_test)
##Các độ đo
db_score = davies_bouldin_score(X_test, labels)

silhouette_avg = silhouette_score(X_test, labels)


#Tạo form
form = Tk()
##đầu đề form
form.title("Phân Cụm chim cánh cụt")
form.geometry("1000x500")

lable_ten = Label(form, text = "Nhập thông tin cho chim cánh cụt:", font=("Arial Bold", 10), fg="blue")
lable_ten.grid(row = 1, column = 1, padx = 40, pady = 10)

lable_culmen_length_mm= Label(form, text = "chiều dài mỏ chim(mm):")
lable_culmen_length_mm.grid(row = 2, column = 1, padx = 40, pady = 10)
textbox_culmen_length_mm = Entry(form)
textbox_culmen_length_mm.grid(row = 2, column = 2)

lable_culmen_depth_mm = Label(form, text = "chiều sâu mỏ chim(mm):")
lable_culmen_depth_mm.grid(row = 3, column = 1, padx = 40, pady = 10)
textbox_culmen_depth_mm = Entry(form)
textbox_culmen_depth_mm.grid(row = 3, column = 2)


lable_flipper_length_mm = Label(form, text = "chiều dài cánh chim(mm):")
lable_flipper_length_mm.grid(row = 4, column = 1,pady = 10)
textbox_flipper_length_mm = Entry(form)
textbox_flipper_length_mm.grid(row = 4, column = 2)



lable_body_mass_g = Label(form, text = "Khối lượng cơ thể(g):")
lable_body_mass_g.grid(row = 5, column = 1, pady = 10 )
textbox_body_mass_g = Entry(form)
textbox_body_mass_g.grid(row = 5, column = 2)

lable_sex = Label(form, text = "giới tính(MALE/FEMALE):")
lable_sex.grid(row = 6, column = 1, pady = 10 )
textbox_sex = Entry(form)
textbox_sex.grid(row = 6, column = 2)

lbl1 = Label(form)
lbl1.grid(column=3, row=3)
##label in ra các độ đo
lbl1.configure(text="\tSố liệu phân cụm: "+'\n'
                           +"\tDavies-Bouldin Score: "+str(db_score)+'\n'
                           +"\tSilhouette Score: "+str(silhouette_avg))

##hàm dự đoán nhãn
def dudoan():
##    gán các biến = dữ liệu nhập vào
    culmen_length = textbox_culmen_length_mm.get()
    culmen_depth = textbox_culmen_depth_mm.get()
    flipper_length = textbox_flipper_length_mm.get()
    body_mass =textbox_body_mass_g.get()
    sex =textbox_sex.get()
##để trống in ra thông báo
    if((culmen_length == '') or (culmen_depth == '') or (flipper_length == '')
       or (body_mass == '') or (sex == '')):
        messagebox.showinfo("Thông báo", "Bạn cần nhập đầy đủ thông tin!")
    else:
##chuẩn hóa dữ liệu nhập vào
        sex = label_encoder.transform([textbox_sex.get().strip()])[0]

        
         # Tạo một mẫu mới từ dữ liệu người dùng nhập
        new_data_point = np.array([[culmen_length, culmen_depth,
                                    flipper_length, body_mass, sex]])

    # Dự đoán nhãn của mẫu mới
        predicted_label = kmeans.predict(new_data_point)[0]

    # Hiển thị kết quả
        lbl.configure(text=f"Nhãn của dữ liệu là: {predicted_label}")
##tạo nút dự đoán nhãn
button_nhan = Button(form, text = 'Kết quả dự đoán nhãn chim cánh cụt', command = dudoan)
## đặt và hiển thị một nút trong giao diện
button_nhan.grid(row = 7, column = 1, pady = 20)
lbl = Label(form, text="...")
lbl.grid(column=2, row=7)

def Clear():
    textbox_culmen_length_mm.delete(0, END)
    textbox_culmen_depth_mm.delete(0, END)
    textbox_flipper_length_mm.delete(0, END)
    textbox_body_mass_g.delete(0, END)
    textbox_sex.delete(0, END)
    lbl.configure(text="...")
reset_button = Button(form, text='Xóa hết', command=Clear)
reset_button.grid(row=8, column=1, pady=10)

form.mainloop()                           

##form.mainloop() là một phương thức trong thư viện tkinter của Python,
##và nó có tác dụng chạy vòng lặp chính của giao diện đồ họa (GUI).
##Phương thức này được sử dụng để hiển thị cửa sổ
##và duy trì chương trình chính chờ đợi sự tương tác từ người dùng.
