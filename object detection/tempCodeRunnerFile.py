from ultralytics import YOLO
import cv2
import pyttsx3
import threading
import queue
import time

# Load the YOLO model
model = YOLO("yolov8s.pt")

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Create a queue to communicate detected object names
object_queue = queue.Queue()

# Define the voice function to speak the names of detected objects
def voice():
    while True:
        # Get the list of object names from the queue
        object_names = object_queue.get()
        
        # Check if the sentinel value (None) was sent to stop the function
        if object_names is None:
            break
        
        # Convert the list of object names to a single string
        detected_objects_str = ", ".join(object_names)
        
        # Convert the object names to speech
        engine.say(f"Detected {detected_objects_str}")
        engine.runAndWait()

# Define the live camera detection function to perform object detection and send object names to the voice function
def live_camera_detection():
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        object_queue.put(None)  # Send sentinel value to stop voice function
        return

    # Process video frames in a loop
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame.")
            break
        
        # Perform object detection using the YOLO model
        results = model.predict(frame, conf=0.5)

        # Display the results on the frame
        annotated_frame = results[0].plot()
        
        # Create a set to store unique object names detected in the frame
        detected_objects = set()
        
        # Read out the names of detected objects
        for detection in results:
            # Iterate through each bounding box in the detection result
            for box in detection.boxes:
                # Access the class ID from the detection (box) object
                class_id = int(box.cls)
                
                # Use the class ID to get the object name from the model's names dictionary
                object_name = model.names[class_id]
                
                # Add the object name to the set of detected objects
                detected_objects.add(object_name)

        # Convert the set of detected objects to a list
        detected_objects_list = list(detected_objects)

        # Only put the detected objects in the queue if the queue is empty
        if object_queue.empty():
            object_queue.put(detected_objects_list)

        # Show the annotated frame
        cv2.imshow("Live Camera Detection", annotated_frame)

        # Add a sleep interval to control the detection rate and allow the voice function to catch up
        time.sleep(0.5)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
    
    # Send sentinel value to stop voice function
    object_queue.put(None)

# Run the live camera detection function and voice function concurrently
if __name__ == "__main__":
    # Create a thread for the voice function
    voice_thread = threading.Thread(target=voice)
    
    # Start the voice thread
    voice_thread.start()
    
    # Run the live camera detection function
    live_camera_detection()
    
    # Wait for the voice thread to finish
    voice_thread.join()
