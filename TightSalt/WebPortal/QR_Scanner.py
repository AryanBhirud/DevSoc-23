import cv2
from pyzbar import pyzbar

def scan_qr_code():
    # Open the default camera
    cap = cv2.VideoCapture(0)
    
    while True:
        # Read frames from the camera
        ret, frame = cap.read()
        
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Use the pyzbar library to scan for QR codes
        barcodes = pyzbar.decode(gray)
        
        # Check if any QR code is detected
        if len(barcodes) > 0:
            # Iterate over the detected barcodes
            for barcode in barcodes:
                # Extract the bounding box coordinates of the barcode
                (x, y, w, h) = barcode.rect
                
                # Draw a rectangle around the barcode
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Convert the barcode data to a string
                barcode_data = barcode.data.decode("utf-8")
                
                # Print the barcode data
                print("QR Code:", barcode_data)
                cap.release()
                cv2.destroyAllWindows()

            break
    
        # Display the frame without any detected QR codes
        cv2.imshow("QR Code Scanner", frame)
        
        # Check for the 'q' key to quit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

# Call the function to start scanning in real-time
scan_qr_code()
