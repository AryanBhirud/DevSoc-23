import cv2
import numpy as np
import os
import face_recognition

# Load the existing database of faces
known_faces_dir = 'check photos'
known_faces = []
known_names = []
for file_name in os.listdir(known_faces_dir):
    image = cv2.imread(os.path.join(known_faces_dir, file_name))
    face_encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(face_encoding)
    known_names.append(os.path.splitext(file_name)[0])

# Function to check if a face matches any known face
def is_face_known(face_encoding):
    matches = face_recognition.compare_faces(known_faces, face_encoding)
    return any(matches)

# Initialize the webcam
video_capture = cv2.VideoCapture(0)

attempt_count = 0  # Track the number of face recognition attempts

while attempt_count < 10:  # Limit the number of attempts to 10
    # Capture frame-by-frame from the webcam
    ret, frame = video_capture.read()

    # Convert the image from BGR color (used by OpenCV) to RGB color
    rgb_frame = frame[:, :, ::-1]

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Iterate over each detected face
    for face_encoding in face_encodings:
        # Check if the face matches any known face
        if is_face_known(face_encoding):
            print("Face recognized. Payment allowed.")
            # Release the webcam and close any open windows
            video_capture.release()
            cv2.destroyAllWindows()
            exit()

    # Increment the attempt count
    attempt_count += 1

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# If the face is not recognized within 10 attempts, print a message and stop the program
print("Face not recognized. Payment denied.")

# Release the webcam and close any open windows
video_capture.release()
cv2.destroyAllWindows()
