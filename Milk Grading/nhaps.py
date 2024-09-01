from tkinter import *
from tkinter import messagebox
from tkinter import ttk


#Tạo form
form = Tk()
##đầu đề form
form.title("Dự đoán chất lượng sữa")
form.geometry("1700x600")

lable_ten = Label(form, text = "Nhập thông tin cho sữa:", font=("Arial Bold", 15), fg="blue")
lable_ten.grid(row = 1, column = 3, padx = 40, pady = 10)
##độ ph
lable_pH= Label(form, text = "pH(3->9,5):", font=("Arial Bold", 15))
lable_pH.grid(row = 2, column = 1,padx = 40, pady = 10)
textbox_pH = Entry(form, font=("Arial Bold", 15))
textbox_pH.grid(row = 2, column = 2,padx = 40, pady = 10)
##Nhiệt độ
lable_Temprature = Label(form, text = "Temprature(C):", font=("Arial Bold", 15))
lable_Temprature.grid(row = 2, column = 3,padx = 40, pady = 10)
textbox_Temprature = Entry(form, font=("Arial Bold", 15))
textbox_Temprature.grid(row = 2, column = 4,padx = 40, pady = 10)

##Hương vị
lable_Taste = Label(form, text = "Taste(Bad:0/Good:1):", font=("Arial Bold", 15))
lable_Taste.grid(row = 3, column = 1,padx = 40, pady = 10)
textbox_Taste = Entry(form, font=("Arial Bold", 15))
textbox_Taste.grid(row = 3, column = 2,padx = 40, pady = 10)


##Mùi
lable_Odor = Label(form, text = "Odor(Bad:0/Good:1):", font=("Arial Bold", 15))
lable_Odor.grid(row = 3, column = 3,padx = 40, pady = 10)
textbox_Odor = Entry(form, font=("Arial Bold", 15))
textbox_Odor.grid(row = 3, column = 4,padx = 40, pady = 10)
##Chất béo
lable_Fat = Label(form, text = "Fat(Low:0/High:1):", font=("Arial Bold", 15))
lable_Fat.grid(row = 4, column = 1 ,padx = 40, pady = 10)
textbox_Fat = Entry(form, font=("Arial Bold", 15))
textbox_Fat.grid(row = 4, column = 2,padx = 40, pady = 10)
##Độ đục
lable_Turbidity = Label(form, text = "Turbidity(Low:0/High:1):", font=("Arial Bold", 15))
lable_Turbidity.grid(row = 4, column = 3 ,padx = 40, pady = 10)
textbox_Turbidity = Entry(form, font=("Arial Bold", 15))
textbox_Turbidity.grid(row = 4, column = 4,padx = 40, pady = 10)
##Màu (dùng mã màu)
lable_Colour = Label(form, text = "Colour(240->255):", font=("Arial Bold", 15))
lable_Colour.grid(row = 5, column = 1 ,padx = 40, pady = 10)
textbox_Colour = Entry(form, font=("Arial Bold", 15))
textbox_Colour.grid(row = 5, column = 2,padx = 40, pady = 10)



##label in ra các độ đo
from sklearn.ensemble import StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import Perceptron,LogisticRegression
df = pd.read_csv('milknew.csv')
X = df[['pH','Temprature','Taste','Odor','Fat ','Turbidity','Colour']]
y = df['Grade']
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True,random_state=42)
decision_tree = DecisionTreeClassifier(criterion='gini',max_depth = 10,min_samples_split = 2,min_samples_leaf=1 ,random_state=42)
decision_tree.fit(X_train, y_train)
neural_network_model= MLPClassifier(max_iter=300,hidden_layer_sizes=(100,100),alpha=0.0001,learning_rate='constant',solver='adam',activation='relu',random_state=42)
neural_network_model.fit(X_train, y_train)
perceptron_model=Perceptron(alpha=0.00001,eta0=0.1,max_iter=50,penalty='elasticnet',tol=0.01,random_state=42)
perceptron_model.fit(X_train, y_train)

# Tạo các mô hình cơ bản
base_classifiers = [
    ('decision_tree', DecisionTreeClassifier(criterion='gini',max_depth = 10,min_samples_split = 2,min_samples_leaf=1 ,random_state=42)),
    ('mlp', MLPClassifier(max_iter=500,hidden_layer_sizes=(100,100),alpha=0.0001,learning_rate='constant',solver='adam',activation='relu',random_state=42)),
    ('perceptron', Perceptron(alpha=0.00001,eta0=0.1,max_iter=50,penalty='elasticnet',tol=0.01,random_state=42))
]

# Mô hình cuối cùng (meta-classifier)
meta = LogisticRegression(random_state=42,C=1,penalty='l2',solver='lbfgs',max_iter=400,class_weight=None)

# Tạo StackingClassifier
stacking = StackingClassifier(estimators=base_classifiers, final_estimator=meta, cv=5,stack_method='auto',n_jobs=None)

# Huấn luyện mô hình
stacking.fit(X_train, y_train)

def dudoanid3():
##    gán các biến = dữ liệu nhập vào
    pH = textbox_pH.get()
    Temprature = textbox_Temprature.get()
    Taste = textbox_Taste.get()
    Odor =textbox_Odor.get()
    Fat =textbox_Fat.get()
    Turbidity =textbox_Turbidity.get()
    Colour =textbox_Colour.get()
    
##để trống in ra thông báo
    if((pH == '') or (Temprature == '') or (Taste == '')
       or (Odor == '') or (Fat == '')or(Turbidity == '')or(Colour == '') ):
        messagebox.showinfo("Thông báo", "Bạn cần nhập đầy đủ thông tin!")
    else:
##chuẩn hóa dữ liệu nhập vào
       

        
         # Tạo một mẫu mới từ dữ liệu người dùng nhập
        new_data_point = np.array([[pH, Temprature,
                                    Taste, Odor, Fat,Turbidity,Colour]])

    # Dự đoán nhãn của mẫu mới
        predicted_label_id3 = decision_tree.predict(new_data_point)[0]
        if(predicted_label_id3==1):
            predicted_label_id3='low(bad)'
        elif(predicted_label_id3==0):
            predicted_label_id3='high(Good)'
        elif(predicted_label_id3==2):
            predicted_label_id3='medium(Moderate)'
            

    # Hiển thị kết quả
        lbl.configure(text=f"Dự đoán là: {predicted_label_id3}")


def dudoanNN():
    
    
##    gán các biến = dữ liệu nhập vào
    pH = textbox_pH.get()
    Temprature = textbox_Temprature.get()
    Taste = textbox_Taste.get()
    Odor =textbox_Odor.get()
    Fat =textbox_Fat.get()
    Turbidity =textbox_Turbidity.get()
    Colour =textbox_Colour.get()
    
##để trống in ra thông báo
    if((pH == '') or (Temprature == '') or (Taste == '')
    or (Odor == '') or (Fat == '')or(Turbidity == '')or(Colour == '') ):
        messagebox.showinfo("Thông báo", "Bạn cần nhập đầy đủ thông tin!")
    else:
##chuẩn hóa dữ liệu nhập vào
       

        pH = float(textbox_pH.get())
        Temprature = float(textbox_Temprature.get())
        Taste = float(textbox_Taste.get())
        Odor =float(textbox_Odor.get())
        Fat =float(textbox_Fat.get())
        Turbidity =float(textbox_Turbidity.get())
        Colour =float(textbox_Colour.get())
         # Tạo một mẫu mới từ dữ liệu người dùng nhập
        new_data_point = np.array([[pH, Temprature,
                                    Taste, Odor, Fat,Turbidity,Colour]])

    # Dự đoán nhãn của mẫu mới
        predicted_label_NN = neural_network_model.predict(new_data_point)[0]
        if(predicted_label_NN==1):
            predicted_label_NN='low(bad)'
        elif(predicted_label_NN==0):
            predicted_label_NN='high(Good)'
        elif(predicted_label_NN==2):
            predicted_label_NN='medium(Moderate)'
            

    # Hiển thị kết quả
        lbl_nn.configure(text=f"Dự đoán là: {predicted_label_NN}")



def dudoanPerceptron():
    
    
##    gán các biến = dữ liệu nhập vào
    pH = textbox_pH.get()
    Temprature = textbox_Temprature.get()
    Taste = textbox_Taste.get()
    Odor =textbox_Odor.get()
    Fat =textbox_Fat.get()
    Turbidity =textbox_Turbidity.get()
    Colour =textbox_Colour.get()
    
##để trống in ra thông báo
    if((pH == '') or (Temprature == '') or (Taste == '')
    or (Odor == '') or (Fat == '')or(Turbidity == '')or(Colour == '') ):
        messagebox.showinfo("Thông báo", "Bạn cần nhập đầy đủ thông tin!")
    else:
##chuẩn hóa dữ liệu nhập vào
        pH = float(textbox_pH.get())
        Temprature = float(textbox_Temprature.get())
        Taste = float(textbox_Taste.get())
        Odor =float(textbox_Odor.get())
        Fat =float(textbox_Fat.get())
        Turbidity =float(textbox_Turbidity.get())
        Colour =float(textbox_Colour.get())

        
         # Tạo một mẫu mới từ dữ liệu người dùng nhập
        new_data_point = np.array([[pH, Temprature,
                                    Taste, Odor, Fat,Turbidity,Colour]])

    # Dự đoán nhãn của mẫu mới
        predicted_label_perceptron_model = perceptron_model.predict(new_data_point)[0]
        if(predicted_label_perceptron_model==1):
            predicted_label_perceptron_model='low(bad)'
        elif(predicted_label_perceptron_model==0):
            predicted_label_perceptron_model='high(Good)'
        elif(predicted_label_perceptron_model==2):
            predicted_label_perceptron_model='medium(Moderate)'
            

    # Hiển thị kết quả
        lbl_perceptron_model.configure(text=f"Dự đoán là: {predicted_label_perceptron_model}")


def dudoanStacking():
    
    
##    gán các biến = dữ liệu nhập vào
    pH = textbox_pH.get()
    Temprature = textbox_Temprature.get()
    Taste = textbox_Taste.get()
    Odor =textbox_Odor.get()
    Fat =textbox_Fat.get()
    Turbidity =textbox_Turbidity.get()
    Colour =textbox_Colour.get()
    
##để trống in ra thông báo
    if((pH == '') or (Temprature == '') or (Taste == '')
    or (Odor == '') or (Fat == '')or(Turbidity == '')or(Colour == '') ):
        messagebox.showinfo("Thông báo", "Bạn cần nhập đầy đủ thông tin!")
    else:
##chuẩn hóa dữ liệu nhập vào
        pH = float(textbox_pH.get())
        Temprature = float(textbox_Temprature.get())
        Taste = float(textbox_Taste.get())
        Odor =float(textbox_Odor.get())
        Fat =float(textbox_Fat.get())
        Turbidity =float(textbox_Turbidity.get())
        Colour =float(textbox_Colour.get())

        
         # Tạo một mẫu mới từ dữ liệu người dùng nhập
        new_data_point = np.array([[pH, Temprature,
                                    Taste, Odor, Fat,Turbidity,Colour]])

    # Dự đoán nhãn của mẫu mới
        predicted_label_Stacking = stacking.predict(new_data_point)[0]
        if(predicted_label_Stacking==1):
            predicted_label_Stacking='low(bad)'
        elif(predicted_label_Stacking==0):
            predicted_label_Stacking='high(Good)'
        elif(predicted_label_Stacking==2):
            predicted_label_Stacking='medium(Moderate)'
            

    # Hiển thị kết quả
        lbl_Stacking.configure(text=f"Dự đoán là: {predicted_label_Stacking}")
##tạo nút dự đoán nhãn
button_Stacking = Button(form, text = 'Kết quả dự đoán Sữa của Stacking', command = dudoanStacking, font=("Arial Bold", 15))
## đặt và hiển thị một nút trong giao diện
button_Stacking.grid(row = 7, column = 4, pady = 20)
lbl_Stacking = Label(form, text="...", font=("Arial Bold", 15))
lbl_Stacking.grid(column=4, row=8)


def Clear():
    textbox_pH.delete(0, END)
    textbox_Temprature.delete(0, END)
    textbox_Taste.delete(0, END)
    textbox_Odor.delete(0, END)
    textbox_Fat.delete(0, END)
    textbox_Turbidity.delete(0, END)
    textbox_Colour.delete(0, END)
 
    lbl.configure(text="...")
reset_button = Button(form, text='Xóa hết', command=Clear, font=("Arial Bold", 15))
reset_button.grid(row=7, column=5, pady=10)
import matplotlib.pyplot as plt
from stacking import *

lbl4 = Label(form, font=("Arial Bold", 15))
lbl4.grid(column=4, row=6)

lbl4.configure(text="\tThông số Stacking: "+'\n'
                           +"\tAccuracy: "+str(accuracy_stacking)+'\n'
                           +"\tPrecision: "+str(Precision_stacking)+'\n'
                           +"\tRecall: "+str(recall_score_stacking)+'\n'
                           +"\tF1: "+str(f1_score_stacking))

from BTL_perceptron import *
from BTL_ID3 import *
from BTL_NN import *
lbl3 = Label(form, font=("Arial Bold", 15))
lbl3.grid(column=1, row=6)
max_number = max(accuracy_Perceptron, accuracy_id3, accuracy_NN)
if(max_number==accuracy_Perceptron):
    lbl3.configure(text="\tMô hình tốt nhất:Perceptron "+'\n'
                           +"\tAccuracy: "+str(accuracy_Perceptron)+'\n'
                           +"\tPrecision: "+str(Precision_Perceptron)+'\n'
                           +"\tRecall: "+str(Recall_Perceptron)+'\n'
                           +"\tF1: "+str(F1_Perceptron))
    lbl2 = Label(form, font=("Arial Bold", 15))
    lbl2.grid(column=2, row=6)
    lbl2.configure(text="\tThông số ID3: "+'\n'
                           +"\tAccuracy: "+str(accuracy_id3)+'\n'
                           +"\tPrecision: "+str(Precision_id3)+'\n'
                           +"\tRecall: "+str(Recall_id3)+'\n'
                           +"\tF1: "+str(F1_id3))
    lbl1 = Label(form, font=("Arial Bold", 15))
    lbl1.grid(column=3, row=6)
    lbl1.configure(text="\tThông số neural_network: "+'\n'
                           +"\tAccuracy: "+str(accuracy_NN)+'\n'
                           +"\tPrecision: "+str(Precision_NN)+'\n'
                           +"\tRecall: "+str(Recall_NN)+'\n'
                           +"\tF1: "+str(F1_NN))
    ##tạo nút dự đoán nhãn
    button_perceptron_model = Button(form, text = 'Kết quả dự đoán Sữa của Perceptron', command = dudoanPerceptron, font=("Arial Bold", 15))
## đặt và hiển thị một nút trong giao diện
    button_perceptron_model.grid(row = 7, column = 2, pady = 20)
    lbl_perceptron_model = Label(form, text="...", font=("Arial Bold", 15))
    lbl_perceptron_model.grid(column=2, row=8)
elif(max_number==accuracy_id3):
    lbl3.configure(text="\tMô hình tốt nhất:ID3 "+'\n'
                           +"\tAccuracy: "+str(accuracy_id3)+'\n'
                        +"\tPrecision: "+str(Precision_id3)+'\n'
                           +"\tRecall: "+str(Recall_id3)+'\n'
                           +"\tF1: "+str(F1_id3))
    
    lbl2 = Label(form, font=("Arial Bold", 15))
    lbl2.grid(column=2, row=6)
    lbl2.configure(text="\tThông số Perceptron: "+'\n'
                           +"\tAccuracy: "+str(accuracy_Perceptron)+'\n'
                           +"\tPrecision: "+str(Precision_Perceptron)+'\n'
                           +"\tRecall: "+str(Recall_Perceptron)+'\n'
                           +"\tF1: "+str(F1_Perceptron))
    lbl1 = Label(form, font=("Arial Bold", 15))
    lbl1.grid(column=3, row=6)
    lbl1.configure(text="\tThông số neural_network: "+'\n'
                           +"\tAccuracy: "+str(accuracy_NN)+'\n'
                           +"\tPrecision: "+str(Precision_NN)+'\n'
                           +"\tRecall: "+str(Recall_NN)+'\n'
                           +"\tF1: "+str(F1_NN))
    ##tạo nút dự đoán nhãn
    button_nhan = Button(form, text = 'Kết quả dự đoán Sữa của ID3', command = dudoanid3, font=("Arial Bold", 15))
## đặt và hiển thị một nút trong giao diện
    button_nhan.grid(row = 7, column = 3, pady = 20)
    lbl = Label(form, text="...", font=("Arial Bold", 15))
    lbl.grid(column=3, row=8)

elif(max_number==accuracy_NN):
    lbl3.configure(text="\tMô hình tốt nhất:neural_network "+'\n'
                           +"\tAccuracy: "+str(accuracy_NN)+'\n'
                           +"\tPrecision: "+str(Precision_NN)+'\n'
                           +"\tRecall: "+str(Recall_NN)+'\n'
                           +"\tF1: "+str(F1_NN))
    lbl2 = Label(form, font=("Arial Bold", 15))
    lbl2.grid(column=2, row=6)
    lbl2.configure(text="\tThông số Perceptron: "+'\n'
                           +"\tAccuracy: "+str(accuracy_Perceptron)+'\n'
                           +"\tPrecision: "+str(Precision_Perceptron)+'\n'
                           +"\tRecall: "+str(Recall_Perceptron)+'\n'
                           +"\tF1: "+str(F1_Perceptron))
    lbl1 = Label(form, font=("Arial Bold", 15))
    lbl1.grid(column=3, row=6)
    lbl1.configure(text="\tThông số ID3: "+'\n'
                           +"\tAccuracy: "+str(accuracy_id3)+'\n'
                           +"\tPrecision: "+str(Precision_id3)+'\n'
                           +"\tRecall: "+str(Recall_id3)+'\n'
                           +"\tF1: "+str(F1_id3))
    ##tạo nút dự đoán nhãn
    button_nn = Button(form, text = 'Kết quả dự đoán Sữa của neural network', command = dudoanNN, font=("Arial Bold", 15))
## đặt và hiển thị một nút trong giao diện
    button_nn.grid(row = 7, column = 1, pady = 20)
    lbl_nn = Label(form, text="...", font=("Arial Bold", 15))
    lbl_nn.grid(column=1, row=8)


form.mainloop()                           

##form.mainloop() là một phương thức trong thư viện tkinter của Python,
##và nó có tác dụng chạy vòng lặp chính của giao diện đồ họa (GUI).
##Phương thức này được sử dụng để hiển thị cửa sổ
##và duy trì chương trình chính chờ đợi sự tương tác từ người dùng.
