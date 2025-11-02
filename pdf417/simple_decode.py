import cv2
from pyzbar.pyzbar import decode
from PIL import Image
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python simple_decode.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' not found!")
    sys.exit(1)

print("=" * 70)
print("PDF417 Barcode Decoder")
print("=" * 70)
print(f"Image: {image_path}\n")

success = False

# Method 1: Try with PIL
print("[1] Trying with PIL...")
try:
    img_pil = Image.open(image_path)
    decoded_objects = decode(img_pil)
    
    if decoded_objects:
        for obj in decoded_objects:
            print(f"\n✓ SUCCESS! Barcode decoded:")
            print(f"  Type: {obj.type}")
            print(f"  Data: {obj.data.decode('utf-8')}")
            
            # Save to file
            with open("decoded_result.txt", "w", encoding='utf-8') as f:
                f.write(obj.data.decode('utf-8'))
            print(f"\n✓ Text saved to 'decoded_result.txt'")
            success = True
            break
except Exception as e:
    print(f"  Error: {e}")

# Method 2: Try with OpenCV
if not success:
    print("\n[2] Trying with OpenCV...")
    try:
        img_cv = cv2.imread(image_path)
        if img_cv is not None:
            decoded_objects = decode(img_cv)
            
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"\n✓ SUCCESS! Barcode decoded:")
                    print(f"  Type: {obj.type}")
                    print(f"  Data: {obj.data.decode('utf-8')}")
                    
                    # Save to file
                    with open("decoded_result.txt", "w", encoding='utf-8') as f:
                        f.write(obj.data.decode('utf-8'))
                    print(f"\n✓ Text saved to 'decoded_result.txt'")
                    success = True
                    break
    except Exception as e:
        print(f"  Error: {e}")

# Method 3: Try with grayscale
if not success:
    print("\n[3] Trying with grayscale conversion...")
    try:
        img_cv = cv2.imread(image_path)
        if img_cv is not None:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            decoded_objects = decode(gray)
            
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"\n✓ SUCCESS! Barcode decoded:")
                    print(f"  Type: {obj.type}")
                    print(f"  Data: {obj.data.decode('utf-8')}")
                    
                    # Save to file
                    with open("decoded_result.txt", "w", encoding='utf-8') as f:
                        f.write(obj.data.decode('utf-8'))
                    print(f"\n✓ Text saved to 'decoded_result.txt'")
                    success = True
                    break
    except Exception as e:
        print(f"  Error: {e}")

#Method 4: Try with contrast enhancement
if not success:
    print("\n[4] Trying with contrast enhancement...")
    try:
        img_cv = cv2.imread(image_path)
        if img_cv is not None:
            gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            # Increase contrast
            enhanced = cv2.equalizeHist(gray)
            decoded_objects = decode(enhanced)
            
            if decoded_objects:
                for obj in decoded_objects:
                    print(f"\n✓ SUCCESS! Barcode decoded:")
                    print(f"  Type: {obj.type}")
                    print(f"  Data: {obj.data.decode('utf-8')}")
                    
                    # Save to file
                    with open("decoded_result.txt", "w", encoding='utf-8') as f:
                        f.write(obj.data.decode('utf-8'))
                    print(f"\n✓ Text saved to 'decoded_result.txt'")
                    success = True
                    break
    except Exception as e:
        print(f"  Error: {e}")

if not success:
    print("\n✗ FAILED: Could not decode the barcode")
    print("\nPossible reasons:")
    print("1. The image quality is too low")
    print("2. The PDF417 barcode is damaged or incomplete")
    print("3. The barcode might not be a valid PDF417 format")
    print("4. Try taking a clearer photo of the barcode")

print("\n" + "=" * 70)
