from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import pyttsx3
import sounddevice as sd
import soundfile as sf

face_classifier = cv2.CascadeClassifier(r'C:\Users\Debarghya Kundu\Desktop\dream project\Emotion_Detection\haarcascade_frontalface_default.xml')
classifier = load_model(r'C:\Users\Debarghya Kundu\Desktop\dream project\Emotion_Detection\emotionmodel.h5')

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

# Initialize the text-to-speech engine
engine = pyttsx3.init()

cap = cv2.VideoCapture(0)

# Define a function to play spoken words
def play_sound(label):
    engine.say(label)
    engine.runAndWait()
# Callback function to play sound using sounddevice
def callback(outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = 0

# Start the sound stream
stream = sd.OutputStream(callback=callback)
stream.start()

# Flag to stop the loop
stop_flag = False

while not stop_flag:
    _, frame = cap.read()
    labels = []
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
            label = emotion_labels[prediction.argmax()]
            label_position = (x, y)
            cv2.putText(frame, label, label_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Play spoken words for the detected emotion
            play_sound(label)

        else:
            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('Emotion Detector', frame)
    
    # Wait for user input to stop or continue
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        stop_flag = True

# Stop the sound stream
stream.stop()
stream.close()

cap.release()
cv2.destroyAllWindows()
