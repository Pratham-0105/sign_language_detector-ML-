import os
import cv2
import sys
import platform
import time

DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


number_of_classes = 5 

dataset_size = 100


cap = None
system = platform.system()

if system == "Darwin": 
    backends = [cv2.CAP_AVFOUNDATION, cv2.CAP_ANY]
else:

    backends = [cv2.CAP_ANY, cv2.CAP_AVFOUNDATION, cv2.CAP_V4L2, cv2.CAP_GSTREAMER]

print(f"System detected: {system}")
print(f"Trying camera backends: {backends}")

for backend in backends:
    try:
        print(f"Attempting to open camera with backend: {backend}")
        cap = cv2.VideoCapture(0, backend)
        if cap.isOpened():
            print(f"Successfully opened camera with backend: {backend}")
            ret, frame = cap.read()
            if ret:
                print("Camera is functioning correctly")
                break
            else:
                print(f"Camera opened but failed to read frame with backend {backend}")
                cap.release()
                cap = None
    except Exception as e:
        print(f"Failed to open camera with backend {backend}: {e}")
        continue

if cap is None or not cap.isOpened():
    print("Error: Could not open camera. Please check camera permissions and connections.")
    print("Troubleshooting tips:")
    print("1. Make sure your webcam is connected and not in use by another application")
    print("2. On macOS, go to System Preferences > Security & Privacy > Privacy > Camera")
    print("3. On macOS Sonoma+, disable 'AirPlay Receiver' in System Settings > General")
    sys.exit(1)


cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  

for j in range(number_of_classes):
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))


    print("Press 'q' to start collecting images for this class, ESC to quit")
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break
            
        cv2.putText(frame, f'Class {j}: Press "Q" to start', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2,
                    cv2.LINE_AA)
        cv2.putText(frame, 'ESC to quit', (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2,
                    cv2.LINE_AA)
        cv2.imshow('frame', frame)
        
       
        if time.time() - start_time > 60:  
            print("Timeout waiting for user input, moving to next class")
            break
            
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            print(f"Starting collection for class {j}")
            break
        elif key == 27:  
            print("User cancelled the process")
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(0)

    
    counter = 0
    print(f"Collecting {dataset_size} images for class {j}")
    while counter < dataset_size:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            break
            
        cv2.imshow('frame', frame)
        key = cv2.waitKey(25) & 0xFF
        if key == ord('q'):
            print(f"User cancelled collection for class {j}")
            break
        elif key == 27:  
            print("User cancelled the process")
            cap.release()
            cv2.destroyAllWindows()
            sys.exit(0)
        elif key == ord('s'):
            print(f"Skipping class {j}")
            break
            
       
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)
        counter += 1
        print(f"Collected image {counter}/{dataset_size} for class {j}")
        
     
        time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
print("Image collection completed successfully!")