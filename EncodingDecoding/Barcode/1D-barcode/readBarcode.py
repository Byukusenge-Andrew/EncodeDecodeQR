import cv2
import pytesseract
from pyzbar.pyzbar import decode

# Load the image
image = cv2.imread('bar.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Use ZBar to decode the barcode
decoded_objects = decode(gray)

for obj in decoded_objects:
    barcode_data = obj.data.decode("utf-8")
    print("Decoded Data:", barcode_data)

# Use Tesseract to extract text (optional)
text = pytesseract.image_to_string(image)
print("Extracted Text:", text)
