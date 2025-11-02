#!/usr/bin/env python3
"""
Comprehensive MaxiCode Decoder
Tries multiple methods to decode MaxiCode barcodes
"""

import sys
import os
from pathlib import Path

# Method 1: Try with pyzbar
def decode_with_pyzbar_pil(image_path):
    """Decode using pyzbar with PIL"""
    try:
        from PIL import Image
        from pyzbar.pyzbar import decode
        
        img = Image.open(image_path)
        decoded_objects = decode(img)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"pyzbar+PIL error: {e}"

# Method 2: Try with pyzbar and OpenCV
def decode_with_pyzbar_opencv(image_path):
    """Decode using pyzbar with OpenCV"""
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        img = cv2.imread(image_path)
        if img is None:
            return None, "Could not load image"
        
        decoded_objects = decode(img)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"pyzbar+OpenCV error: {e}"

# Method 3: Try with grayscale conversion
def decode_with_grayscale(image_path):
    """Decode with grayscale preprocessing"""
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        img = cv2.imread(image_path)
        if img is None:
            return None, "Could not load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"grayscale error: {e}"

# Method 4: Try with binary threshold
def decode_with_binary(image_path):
    """Decode with binary threshold preprocessing"""
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, "Could not load image"
        
        _, binary = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        decoded_objects = decode(binary)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"binary threshold error: {e}"

# Method 5: Try with Otsu's thresholding
def decode_with_otsu(image_path):
    """Decode with Otsu's thresholding"""
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, "Could not load image"
        
        _, otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        decoded_objects = decode(otsu)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"Otsu threshold error: {e}"

# Method 6: Try with adaptive thresholding
def decode_with_adaptive(image_path):
    """Decode with adaptive thresholding"""
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            return None, "Could not load image"
        
        adaptive = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 2)
        decoded_objects = decode(adaptive)
        
        for obj in decoded_objects:
            if obj.type == 'MAXICODE':
                return obj.data.decode('utf-8', errors='replace'), obj
        return None, None
    except Exception as e:
        return None, f"adaptive threshold error: {e}"

# Method 7: Try with ZXing via Docker
def decode_with_zxing_docker(image_path):
    """Decode using ZXing in Docker"""
    try:
        import subprocess
        
        if not os.path.exists(image_path):
            return None, f"File not found: {image_path}"
        
        command = [
            "docker", "run", "--rm", "-v",
            f"{os.path.abspath(os.path.dirname(image_path))}:/data",
            "zxing-decoder", f"/data/{os.path.basename(image_path)}"
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip(), None
        return None, f"ZXing returned: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return None, "Docker command timed out"
    except FileNotFoundError:
        return None, "Docker not found"
    except Exception as e:
        return None, f"ZXing Docker error: {e}"

def decode_maxicode(image_path):
    """Try all methods to decode MaxiCode"""
    
    print("=" * 80)
    print("MAXICODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}\n")
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file not found: {image_path}")
        return False
    
    methods = [
        ("Method 1: Decoding with pyzbar + PIL...", decode_with_pyzbar_pil),
        ("Method 2: Decoding with pyzbar + OpenCV...", decode_with_pyzbar_opencv),
        ("Method 3: Decoding with grayscale conversion...", decode_with_grayscale),
        ("Method 4: Decoding with binary threshold...", decode_with_binary),
        ("Method 5: Decoding with Otsu's thresholding...", decode_with_otsu),
        ("Method 6: Decoding with adaptive thresholding...", decode_with_adaptive),
        ("Method 7: Decoding with ZXing (Docker)...", decode_with_zxing_docker),
    ]
    
    for description, method in methods:
        print(description)
        result, obj = method(image_path)
        
        if result:
            print(f"\n✅ SUCCESS! MaxiCode decoded with {description.split(':')[0]}")
            print("-" * 80)
            print("Decoded Data:")
            print(result)
            print("-" * 80)
            
            if obj and hasattr(obj, 'rect'):
                print(f"\nPosition: x={obj.rect.left} y={obj.rect.top}")
                print(f"Size: {obj.rect.width}x{obj.rect.height} pixels")
            
            # Save to file
            output_file = os.path.join(os.path.dirname(image_path), "decoded_maxicode.txt")
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"MaxiCode Decoding Result\n")
                    f.write(f"{'=' * 80}\n")
                    f.write(f"Image: {image_path}\n")
                    f.write(f"Method: {description}\n")
                    f.write(f"\nDecoded Data:\n")
                    f.write(result)
                    f.write("\n")
                    
                    if obj and hasattr(obj, 'rect'):
                        f.write(f"\nPosition: x={obj.rect.left} y={obj.rect.top}\n")
                        f.write(f"Size: {obj.rect.width}x{obj.rect.height} pixels\n")
                
                print(f"\n💾 Result saved to: {output_file}")
            except Exception as e:
                print(f"\n⚠️ Could not save to file: {e}")
            
            return True
    
    print("\n❌ No MaxiCode found with any method!")
    print("\nPossible reasons:")
    print("  - The image doesn't contain a MaxiCode")
    print("  - The MaxiCode is damaged or unclear")
    print("  - Image quality is too low")
    print("  - MaxiCode requires ZXing library (try with Docker)")
    print("\n❌ DECODING FAILED")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_maxicode.py <image_path>")
        print("\nExample:")
        print("  python decode_maxicode.py maxicode.png")
        print("  python decode_maxicode.py d:\\path\\to\\maxicode.jpg")
        sys.exit(1)
    
    image_path = sys.argv[1]
    success = decode_maxicode(image_path)
    sys.exit(0 if success else 1)
