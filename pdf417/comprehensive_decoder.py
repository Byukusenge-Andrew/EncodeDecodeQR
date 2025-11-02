"""
Comprehensive PDF417 Barcode Decoder
Uses multiple decoding libraries and preprocessing techniques
"""

import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
import sys
import os
import subprocess

def decode_with_pyzbar_pil(image_path):
    """Decode using pyzbar with PIL"""
    try:
        img = Image.open(image_path)
        decoded_objects = decode(img)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality,
                    'rect': obj.rect,
                    'polygon': obj.polygon
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_opencv_pyzbar(image_path):
    """Decode using OpenCV with pyzbar"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        decoded_objects = decode(img)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality,
                    'rect': obj.rect
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_grayscale(image_path):
    """Decode using grayscale conversion"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_binary_threshold(image_path):
    """Decode using binary thresholding"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        
        decoded_objects = decode(binary)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_otsu_threshold(image_path):
    """Decode using Otsu's thresholding"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        decoded_objects = decode(otsu)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_adaptive_threshold(image_path):
    """Decode using adaptive thresholding"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        adaptive = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, 11, 2
        )
        
        decoded_objects = decode(adaptive)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_contrast_enhancement(image_path):
    """Decode using histogram equalization"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        enhanced = cv2.equalizeHist(gray)
        
        decoded_objects = decode(enhanced)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_clahe(image_path):
    """Decode using CLAHE (Contrast Limited Adaptive Histogram Equalization)"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        decoded_objects = decode(enhanced)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_rotation(image_path, angle):
    """Decode by rotating the image"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return False, "Failed to load image"
        
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h))
        
        gray = cv2.cvtColor(rotated, cv2.COLOR_BGR2GRAY)
        decoded_objects = decode(gray)
        
        if decoded_objects:
            results = []
            for obj in decoded_objects:
                results.append({
                    'type': obj.type,
                    'data': obj.data.decode('utf-8'),
                    'quality': obj.quality,
                    'rotation': angle
                })
            return True, results
    except Exception as e:
        return False, str(e)
    return False, "No barcode found"

def decode_with_zxing_java(image_path):
    """Decode using ZXing Java library"""
    javase_jar = "javase-3.5.0.jar"
    core_jar = "core-3.5.0.jar"
    jcommander_jar = "jcommander-1.82.jar"
    
    # Check if JAR files exist
    if not all(os.path.exists(jar) for jar in [javase_jar, core_jar, jcommander_jar]):
        return False, "ZXing JAR files not found"
    
    try:
        command = [
            "java", "-cp",
            f"{javase_jar};{core_jar};{jcommander_jar}",
            "com.google.zxing.client.j2se.CommandLineRunner",
            image_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and "No barcode found" not in result.stdout:
            return True, result.stdout
        else:
            return False, "No barcode found with ZXing"
    except Exception as e:
        return False, str(e)

def main():
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_decoder.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found!")
        sys.exit(1)
    
    print("=" * 80)
    print("COMPREHENSIVE PDF417 BARCODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}")
    
    # Get image info
    try:
        img = cv2.imread(image_path)
        if img is not None:
            print(f"Image size: {img.shape}")
    except:
        pass
    
    print("=" * 80)
    
    methods = [
        ("pyzbar with PIL", decode_with_pyzbar_pil),
        ("OpenCV with pyzbar", decode_with_opencv_pyzbar),
        ("Grayscale conversion", decode_with_grayscale),
        ("Binary threshold", decode_with_binary_threshold),
        ("Otsu's threshold", decode_with_otsu_threshold),
        ("Adaptive threshold", decode_with_adaptive_threshold),
        ("Contrast enhancement", decode_with_contrast_enhancement),
        ("CLAHE enhancement", decode_with_clahe),
    ]
    
    # Try all methods
    for idx, (method_name, method_func) in enumerate(methods, 1):
        print(f"\n[{idx}] Trying: {method_name}...")
        success, result = method_func(image_path)
        
        if success:
            print(f"\n{'='*80}")
            print(f"✓ SUCCESS! Decoded with: {method_name}")
            print(f"{'='*80}")
            
            if isinstance(result, list):
                for obj in result:
                    print(f"\nType: {obj['type']}")
                    print(f"Data: {obj['data']}")
                    if 'quality' in obj:
                        print(f"Quality: {obj['quality']}")
                    
                    # Save to file
                    with open("decoded_pdf417.txt", "w", encoding='utf-8') as f:
                        f.write(obj['data'])
                    print(f"\n✓ Decoded text saved to 'decoded_pdf417.txt'")
            else:
                print(result)
            
            print(f"{'='*80}")
            return
    
    # Try rotations
    print(f"\n[{len(methods)+1}] Trying with rotations...")
    for angle in [90, 180, 270]:
        print(f"  Rotating {angle}°...")
        success, result = decode_with_rotation(image_path, angle)
        if success:
            print(f"\n{'='*80}")
            print(f"✓ SUCCESS! Decoded with {angle}° rotation")
            print(f"{'='*80}")
            
            if isinstance(result, list):
                for obj in result:
                    print(f"\nType: {obj['type']}")
                    print(f"Data: {obj['data']}")
                    
                    # Save to file
                    with open("decoded_pdf417.txt", "w", encoding='utf-8') as f:
                        f.write(obj['data'])
                    print(f"\n✓ Decoded text saved to 'decoded_pdf417.txt'")
            
            print(f"{'='*80}")
            return
    
    # Try ZXing
    print(f"\n[{len(methods)+2}] Trying with ZXing Java library...")
    success, result = decode_with_zxing_java(image_path)
    if success:
        print(f"\n{'='*80}")
        print(f"✓ SUCCESS! Decoded with ZXing")
        print(f"{'='*80}")
        print(result)
        print(f"{'='*80}")
        return
    
    # All methods failed
    print(f"\n{'='*80}")
    print("✗ DECODING FAILED")
    print(f"{'='*80}")
    print("\nAll decoding methods failed. Possible reasons:")
    print("1. The image does not contain a valid PDF417 barcode")
    print("2. The barcode is damaged or of very poor quality")
    print("3. The image is the wrong file")
    print("4. The barcode format is not PDF417")
    print("\nSuggestions:")
    print("- Download the actual quiz image directly")
    print("- Try scanning with a phone camera first")
    print("- Ensure the image is clear and well-lit")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
