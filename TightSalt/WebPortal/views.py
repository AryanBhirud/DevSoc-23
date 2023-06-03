from django.shortcuts import render
from django.http import HttpResponse
from .models import student
import cv2
import numpy as np
import os
import face_recognition
from pyzbar import pyzbar
import qrcode
from PIL import Image



def home(request):
    context = {}
    return render(request, 'WebPortal/home.html', context)

def team(request):
    context = {}
    return render(request, 'WebPortal/team.html', context)

def result_view(request):
    context = {}
    return render(request, 'WebPortal/result.html', context)

def register(request):
    context = {}
    return render(request, 'WebPortal/register.html', context)

def qr_auth(request):
    qr_link = run_qr_scanner(request)
    context = {
        'barcode_data':f'the link of the user is {qr_link}'
    }
    return render(request, 'WebPortal/qr_auth.html', context)
# ---------------------------------------------------------------------------------------------------
def register_new_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        registration_number = request.POST.get('regNo')
        paswrd = request.POST.get('password')
        photo = request.FILES.get('save_img')
        
        user = student(fname=first_name, lname=last_name, email=email, mobile=mobile, regno=registration_number, password=paswrd, save_img=photo)
        user.save()
        
        qr_code = generate_qr_code(paswrd)
        qr_code.show()    
        return render(request, 'WebPortal/register_result.html', {'message': 'Student and face registered.'})
    return render(request, 'WebPortal/register_result.html', {'message': 'Student and face could not be registered.'})
       
# ---------------------------------------------------------------------------------------------------

# Load the existing database of faces
known_faces_dir = 'static\images\static\images'
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

def run_face_recog_page(request):
    if request.method == 'POST':
        price = request.POST.get('price')
    # Initialize the webcam
    video_capture = cv2.VideoCapture(0)

    attempt_count = 0  # Track the number of face recognition attempts

    while attempt_count < 2:  # Limit the number of attempts to 2
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
                # Release the webcam and close any open windows
                video_capture.release()
                cv2.destroyAllWindows()
                return render(request, 'WebPortal/result.html', {'message': 'Face recognized.'})

        # Increment the attempt count
        attempt_count += 1

    # If the face is not recognized within 2 attempts, return a message
    # Release the webcam and close any open windows
    video_capture.release()
    cv2.destroyAllWindows()
    return render(request, 'WebPortal/result.html', {'message': 'Face not recognized. Payment denied.'})


def run_qr_scanner(request):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        barcodes = pyzbar.decode(gray)
        
        if len(barcodes) > 0:
            for barcode in barcodes:
                (x, y, w, h) = barcode.rect
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                barcode_data = barcode.data.decode("utf-8")
                
                print("QR Code:", barcode_data)
                cap.release()
                cv2.destroyAllWindows()
                return barcode_data

            break
    
        cv2.imshow("QR Code Scanner", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    return img
