import cv2
from pyzbar.pyzbar import decode

# Load the image containing the 2D barcode
image = cv2.imread('img-01.png')

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Decode the barcode
barcodes = decode(gray_image)

# Loop through all the detected barcodes
for barcode in barcodes:
    barcode_data = barcode.data.decode('utf-8')
    print("Barcode data: ", barcode_data)

    # You can add more processing or actions based on the decoded data here

# Display the image with detected barcodes (optional)
cv2.imshow('Detected Barcode', image)
cv2.waitKey(0)
cv2.destroyAllWindows()