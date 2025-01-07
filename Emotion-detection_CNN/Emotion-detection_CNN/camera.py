from keras.models import load_model
from time import sleep
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import os
from keras.models import load_model

# Đường dẫn đến thư mục chứa file `.py` hiện tại
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'model-CNN.keras')

# Cố gắng load model nếu file tồn tại
classifier = None
try:
    if os.path.exists(model_path):
        classifier = load_model(model_path) 
        print("Model loaded successfully!")
    else:
        print("Model file not found. Continuing without loading the model.")
except Exception as e:
    print(f"Error loading model: {e}. Continuing without the model.")

face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
classifier = load_model(model_path)


emotion_labels = ['Tuc Gian','Buon ban','Kinh tom','Vui ve', 'Binh Thuong', 'Buon ba', 'Bat ngo']

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray]) != 0:
            roi = roi_gray.astype('float') / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)

            prediction = classifier.predict(roi)[0]
            label_index = prediction.argmax()
            label = emotion_labels[label_index]
            confidence = prediction[label_index] * 100  # Độ chính xác (%)

            label_position = (x, y)
            cv2.putText(frame, f'{label} ({confidence:.2f}%)', label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Emotion Detector', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
