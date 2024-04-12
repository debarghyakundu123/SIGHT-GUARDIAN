#full code for image , pdf , live cam detection model

import cv2
import pytesseract
import pyttsx3
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF

# Path to the Tesseract executable (change this if necessary)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Debarghya Kundu\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def image_to_text(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Perform thresholding to enhance text visibility
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Perform OCR on the preprocessed image
    text = pytesseract.image_to_string(thresh, lang='eng')  # Change 'eng' to the appropriate language code
    return text

def pdf_to_text(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

def speak_text(text):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()

    # Speak the text
    engine.say(text)
    engine.runAndWait()

def live_camera_text_detection():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Live Camera', frame)

        # Check for user input to capture image
        key = cv2.waitKey(1)
        if key == ord('c'):  # Press 'c' to capture image
            # Perform OCR on the captured image
            text = image_to_text(frame)

            # Print the extracted text
            print(text)

            # Speak out the extracted text
            speak_text(text)

        # Press 'q' to quit
        elif key == ord('q'):
            break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

def upload_and_read_image():
    # Open a file dialog to select image
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Read the image
    if file_path:
        image = cv2.imread(file_path)

        # Perform OCR on the image
        text = image_to_text(image)

        # Print the extracted text
        print(text)

        # Speak out the extracted text
        speak_text(text)

def upload_and_read_pdf():
    # Open a file dialog to select PDF
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()

    # Read the PDF
    if file_path:
        # Extract text from PDF
        text = pdf_to_text(file_path)

        # Print the extracted text
        print(text)

        # Speak out the extracted text
        speak_text(text)

def main():
    while True:
        print("Choose an option:")
        print("1. Live camera text detection")
        print("2. Upload and read image")
        print("3. Upload and read PDF")
        print("Enter 'q' to quit")

        option = input("Enter your choice: ")

        if option == '1':
            live_camera_text_detection()
        elif option == '2':
            upload_and_read_image()
        elif option == '3':
            upload_and_read_pdf()
        elif option == 'q':
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
