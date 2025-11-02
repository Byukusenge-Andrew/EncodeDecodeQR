import cv2
import sys
from pyzbar.pyzbar import decode
from PIL import Image

if len(sys.argv) < 2:
    print("Usage: python decode_multi.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# Method 1: Using pyzbar with PIL
print("=" * 50)
print("Method 1: Using pyzbar with PIL")
print("=" * 50)
try:
    img_pil = Image.open(image_path)
    decoded_objects = decode(img_pil)
    
    if decoded_objects:
        for obj in decoded_objects:
            print(f"Type: {obj.type}")
            print(f"Data: {obj.data.decode('utf-8')}")
            print(f"Quality: {obj.quality}")
            print(f"Rect: {obj.rect}")
    else:
        print("No barcode found with pyzbar")
except Exception as e:
    print(f"Error with pyzbar: {e}")

# Method 2: Using OpenCV with pyzbar
print("\n" + "=" * 50)
print("Method 2: Using OpenCV with pyzbar")
print("=" * 50)
try:
    img_cv = cv2.imread(image_path)
    if img_cv is not None:
        # Try with grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        
        if decoded_objects:
            for obj in decoded_objects:
                print(f"Type: {obj.type}")
                print(f"Data: {obj.data.decode('utf-8')}")
        else:
            print("No barcode found in grayscale")
            
            # Try with original image
            decoded_objects = decode(img_cv)
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"Type: {obj.type}")
                    print(f"Data: {obj.data.decode('utf-8')}")
            else:
                print("No barcode found in color image")
    else:
        print("Could not load image with OpenCV")
except Exception as e:
    print(f"Error with OpenCV: {e}")

# Method 3: Try with enhanced image
print("\n" + "=" * 50)
print("Method 3: Using enhanced image preprocessing")
print("=" * 50)
try:
    img_cv = cv2.imread(image_path)
    if img_cv is not None:
        # Convert to grayscale
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        decoded_objects = decode(thresh)
        if decoded_objects:
            for obj in decoded_objects:
                print(f"Type: {obj.type}")
                print(f"Data: {obj.data.decode('utf-8')}")
        else:
            print("No barcode found with thresholding")
            
            # Try with adaptive thresholding
            adaptive_thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            decoded_objects = decode(adaptive_thresh)
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"Type: {obj.type}")
                    print(f"Data: {obj.data.decode('utf-8')}")
            else:
                print("No barcode found with adaptive thresholding")
except Exception as e:
    print(f"Error with preprocessing: {e}")

print("\n" + "=" * 50)
print("Decoding attempts completed")
print("=" * 50)
