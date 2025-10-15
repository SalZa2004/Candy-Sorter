import serial
import time
import cv2
import numpy as np
from tensorflow.keras.models import load_model

# === Setup Serial Connection ===
arduino = serial.Serial('COM5', 9600)  # Change COM3 to your Arduino port
time.sleep(2)
print("Connected to Arduino.")


model = load_model('keras_model.h5') # Change path! 
labels = open('labels.txt', 'r').readlines()
# === Start Webcam ===
cap = cv2.VideoCapture(0)
print("Starting camera... Press 'q' to quit.")


last_sent_time = 0
send_interval = 1  # seconds

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Preprocess
    img = cv2.resize(frame, (224, 224))
    img = np.expand_dims(img / 255.0, axis=0).astype(np.float32)

    # Make prediction 
    prediction = model.predict(img) 
    index = np.argmax(prediction) 
    label = labels[index].strip() 
    confidence = prediction[0][index]



    # Display
    cv2.putText(frame, f"{label} ({confidence*100:.1f}%)", (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.imshow("Skittle Detector", frame)

    # Send to Arduino only if confidence > 90% and enough time has passed
    current_time = time.time()
    if confidence > 0.9 and (current_time - last_sent_time) > send_interval:
        if label == "0 Green":
            arduino.write(b"1")
        elif label == "1 Purple":
            arduino.write(b"3")
        elif label == "2 Salvina and Nadia":
            arduino.write(b"2")

        print(f"Detected {label} → Sent signal to Arduino")
        last_sent_time = current_time  # update last send time

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
arduino.close()
print("Program ended.")
