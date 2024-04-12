import cv2
import numpy as np
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Function to speak the detected color
def speak_color(detected_color):
    engine.say(f"The detected color is {detected_color}")
    engine.runAndWait()

# Define lower and upper bounds for the colors you want to detect in HSV color space
color_ranges = {
    'blue':          ([100, 100, 100], [140, 255, 255]),
    'red':           ([0, 100, 100], [10, 255, 255]),
    'green':         ([40, 100, 100], [80, 255, 255]),
    'yellow':        ([20, 100, 100], [30, 255, 255]),
    'orange':        ([10, 100, 100], [20, 255, 255]),
    'purple':        ([140, 100, 100], [160, 255, 255]),
    'pink':          ([160, 100, 100], [180, 255, 255]),
    'brown':         ([0, 100, 100], [20, 255, 255]),
    'black':         ([0, 0, 0], [180, 255, 30]),
    'white':         ([0, 0, 200], [180, 40, 255]),
    'gray':          ([0, 0, 50], [180, 40, 200]),
    'beige':         ([20, 50, 100], [40, 150, 200]),
    'turquoise':     ([80, 100, 100], [100, 255, 255]),
    'maroon':        ([0, 100, 50], [10, 255, 200]),
    'navy':          ([100, 100, 50], [140, 255, 200]),
    'olive':         ([30, 100, 50], [40, 255, 200]),
    'teal':          ([80, 100, 50], [90, 255, 200]),
    'magenta':       ([140, 100, 50], [160, 255, 200]),
    'cyan':          ([80, 0, 0], [100, 255, 255]),
    'lavender':      ([120, 50, 100], [140, 200, 200]),
    'gold':          ([20, 100, 100], [30, 255, 255]),
    'silver':        ([0, 0, 150], [180, 30, 200]),
    'bronze':        ([10, 100, 50], [20, 255, 200]),
    'indigo':        ([100, 100, 50], [120, 255, 200]),
    'coral':         ([0, 100, 50], [10, 255, 200]),
    'peach':         ([0, 100, 100], [20, 255, 255]),
    'mint':          ([80, 50, 100], [100, 200, 200]),
    'charcoal':      ([0, 0, 0], [100, 100, 50]),
    'cream':         ([0, 0, 200], [40, 50, 255]),
    'sky blue':      ([80, 100, 100], [100, 255, 255]),
    'forest green':  ([40, 100, 50], [80, 255, 200]),
    'ruby':          ([140, 100, 50], [160, 255, 200]),
    'emerald':       ([80, 100, 50], [100, 255, 200]),
    'lemon':         ([20, 100, 100], [30, 255, 255]),
    'tan':           ([20, 100, 100], [30, 255, 255]),
    'mauve':         ([140, 50, 100], [160, 150, 200]),
    'slate':         ([0, 0, 80], [180, 40, 150]),
    'burgundy':      ([0, 100, 50], [10, 255, 200]),
    'ivory':         ([0, 0, 200], [40, 50, 255]),
    'mahogany':      ([0, 100, 50], [10, 255, 200]),
    'olive green':   ([30, 100, 50], [40, 255, 200]),
    'turquoise blue':([80, 100, 100], [100, 255, 255]),
    'plum':          ([140, 100, 50], [160, 255, 200]),
    'salmon':        ([0, 100, 50], [10, 255, 200]),
    'mustard':       ([20, 100, 100], [30, 255, 255]),
    'teal blue':     ([80, 100, 50], [90, 255, 200]),
    'brick red':     ([0, 100, 50], [10, 255, 200]),
    'steel gray':    ([0, 0, 80], [180, 30, 150]),
    'sand':          ([0, 100, 100], [20, 200, 255]),
    'eggplant':      ([140, 100, 50], [160, 255, 200])
}

# Initialize webcam
cap = cv2.VideoCapture(0)

# Define the region of interest (ROI) where the color will be detected
roi_x, roi_y, roi_width, roi_height = 100, 100, 200, 200

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Draw a square box around the ROI
    cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_width, roi_y + roi_height), (255, 0, 0), 2)

    # Get the region of interest (ROI)
    roi = hsv[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]

    # Initialize variables to store detected color and maximum area
    detected_color = "Unknown"
    max_area = 0

    # Detect each color
    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower)
        upper = np.array(upper)
        mask = cv2.inRange(roi, lower, upper)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Find the contour with the maximum area
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > max_area:
                max_area = area
                detected_color = color

    # Display the detected color
    cv2.putText(frame, f"Detected color: {detected_color}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Speak the detected color
    speak_color(detected_color)

    # Display the original frame
    cv2.imshow('Color Detection', frame)

    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
