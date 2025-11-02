import cv2
import sys
from pyzbar.pyzbar import decode
from PIL import Image
import numpy as np

if len(sys.argv) < 2:
    print("Usage: python decode_robust.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

def try_decode(img, method_name):
    """Try to decode an image and return results"""
    decoded_objects = decode(img)
    if decoded_objects:
        print(f"\n✓ SUCCESS with {method_name}!")
        for obj in decoded_objects:
            print(f"  Type: {obj.type}")
            print(f"  Data: {obj.data.decode('utf-8', errors='ignore')}")
            print(f"  Quality: {obj.quality}")
        return True
    return False

print("=" * 60)
print("PDF417 Robust Decoder")
print("=" * 60)

# Load image
img_cv = cv2.imread(image_path)
if img_cv is None:
    print(f"Error: Could not load image {image_path}")
    sys.exit(1)

print(f"Image size: {img_cv.shape}")

# Try different preprocessing methods
methods_tried = 0
success = False

# Method 1: Original image
print(f"\n[{methods_tried+1}] Trying original image...")
if try_decode(img_cv, "original image"):
    success = True
methods_tried += 1

# Method 2: Grayscale
if not success:
    print(f"\n[{methods_tried+1}] Trying grayscale...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    if try_decode(gray, "grayscale"):
        success = True
    methods_tried += 1

# Method 3: Binary threshold
if not success:
    print(f"\n[{methods_tried+1}] Trying binary threshold...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    if try_decode(binary, "binary threshold"):
        success = True
    methods_tried += 1

# Method 4: Otsu's threshold
if not success:
    print(f"\n[{methods_tried+1}] Trying Otsu's threshold...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if try_decode(otsu, "Otsu's threshold"):
        success = True
    methods_tried += 1

# Method 5: Adaptive threshold
if not success:
    print(f"\n[{methods_tried+1}] Trying adaptive threshold...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY, 11, 2)
    if try_decode(adaptive, "adaptive threshold"):
        success = True
    methods_tried += 1

# Method 6: Inverted binary
if not success:
    print(f"\n[{methods_tried+1}] Trying inverted binary...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    _, binary_inv = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    if try_decode(binary_inv, "inverted binary"):
        success = True
    methods_tried += 1

# Method 7: Enhanced contrast
if not success:
    print(f"\n[{methods_tried+1}] Trying enhanced contrast...")
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    enhanced = cv2.equalizeHist(gray)
    if try_decode(enhanced, "enhanced contrast"):
        success = True
    methods_tried += 1

# Method 8: Rotations (sometimes images are sideways)
if not success:
    for angle in [90, 180, 270]:
        print(f"\n[{methods_tried+1}] Trying rotation {angle}°...")
        rows, cols = img_cv.shape[:2]
        M = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        rotated = cv2.warpAffine(img_cv, M, (cols, rows))
        if try_decode(rotated, f"rotation {angle}°"):
            success = True
            break
        methods_tried += 1

# Method 9: Denoising
if not success:
    print(f"\n[{methods_tried+1}] Trying denoising...")
    denoised = cv2.fastNlMeansDenoisingColored(img_cv, None, 10, 10, 7, 21)
    if try_decode(denoised, "denoised"):
        success = True
    methods_tried += 1

# Method 10: Sharpen
if not success:
    print(f"\n[{methods_tried+1}] Trying sharpening...")
    kernel = np.array([[-1,-1,-1],
                       [-1, 9,-1],
                       [-1,-1,-1]])
    sharpened = cv2.filter2D(img_cv, -1, kernel)
    if try_decode(sharpened, "sharpened"):
        success = True
    methods_tried += 1

print("\n" + "=" * 60)
if success:
    print("✓ DECODING SUCCESSFUL!")
else:
    print(f"✗ Failed to decode after {methods_tried} attempts")
    print("\nPossible reasons:")
    print("  - Image quality too low")
    print("  - Barcode is damaged or incomplete")
    print("  - Wrong barcode type")
    print("  - Image resolution too low")
print("=" * 60)
