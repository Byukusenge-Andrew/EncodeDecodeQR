"""
Aztec Code Decoder - Complete Implementation
Decodes Aztec barcodes using multiple methods
"""

from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import sys
import os

def decode_aztec(image_path):
    """
    Decode Aztec code from image
    
    Args:
        image_path: Path to the image file
    
    Returns:
        List of decoded data or None
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return None
    
    print("=" * 80)
    print("AZTEC CODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}\n")
    
    try:
        # Method 1: Try with pyzbar + PIL
        print("Method 1: Decoding with pyzbar + PIL...")
        pil_image = Image.open(image_path)
        decoded_pil = decode(pil_image)
        
        if decoded_pil:
            aztec_results = [obj for obj in decoded_pil if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with pyzbar + PIL!\n")
                return process_results(aztec_results, image_path)
        
        # Method 2: Try with pyzbar + OpenCV
        print("Method 2: Decoding with pyzbar + OpenCV...")
        cv_image = cv2.imread(image_path)
        decoded_cv = decode(cv_image)
        
        if decoded_cv:
            aztec_results = [obj for obj in decoded_cv if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with pyzbar + OpenCV!\n")
                return process_results(aztec_results, image_path)
        
        # Method 3: Try with grayscale
        print("Method 3: Decoding with grayscale conversion...")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        decoded_gray = decode(gray)
        
        if decoded_gray:
            aztec_results = [obj for obj in decoded_gray if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with grayscale!\n")
                return process_results(aztec_results, image_path)
        
        # Method 4: Try with binary threshold
        print("Method 4: Decoding with binary threshold...")
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        decoded_binary = decode(binary)
        
        if decoded_binary:
            aztec_results = [obj for obj in decoded_binary if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with binary threshold!\n")
                return process_results(aztec_results, image_path)
        
        # Method 5: Try with Otsu's thresholding
        print("Method 5: Decoding with Otsu's thresholding...")
        _, otsu = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        decoded_otsu = decode(otsu)
        
        if decoded_otsu:
            aztec_results = [obj for obj in decoded_otsu if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with Otsu's thresholding!\n")
                return process_results(aztec_results, image_path)
        
        # Method 6: Try with adaptive thresholding
        print("Method 6: Decoding with adaptive thresholding...")
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 2)
        decoded_adaptive = decode(adaptive)
        
        if decoded_adaptive:
            aztec_results = [obj for obj in decoded_adaptive if obj.type == 'AZTEC']
            if aztec_results:
                print("✅ Successfully decoded with adaptive thresholding!\n")
                return process_results(aztec_results, image_path)
        
        print("❌ No Aztec code found with any method!")
        print("\nPossible reasons:")
        print("  - The image doesn't contain an Aztec code")
        print("  - The Aztec code is damaged or unclear")
        print("  - Image quality is too low")
        print("  - The code requires specialized pyztec library")
        return None
        
    except Exception as e:
        print(f"❌ Error during decoding: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def process_results(decoded_objects, image_path):
    """Process and display decoded results"""
    
    print("=" * 80)
    print(f"✅ Found {len(decoded_objects)} Aztec code(s)")
    print("=" * 80)
    
    decoded_data_list = []
    
    for i, obj in enumerate(decoded_objects, 1):
        # Decode data
        try:
            aztec_data = obj.data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                aztec_data = obj.data.decode('latin-1')
            except:
                aztec_data = str(obj.data)
        
        aztec_type = obj.type
        decoded_data_list.append((aztec_type, aztec_data))
        
        # Display information
        print(f"\nAztec Code #{i}")
        print(f"  Type: {aztec_type}")
        print(f"  Data: {aztec_data}")
        print(f"  Raw Bytes: {obj.data}")
        print(f"  Data Length: {len(aztec_data)} characters")
        
        # Position information
        if hasattr(obj, 'rect'):
            rect = obj.rect
            print(f"  Position: x={rect.left}, y={rect.top}")
            print(f"  Size: {rect.width} x {rect.height} pixels")
        
        # Quality
        if hasattr(obj, 'quality'):
            print(f"  Quality: {obj.quality}")
        
        # Polygon points
        if hasattr(obj, 'polygon'):
            print(f"  Polygon points: {len(obj.polygon)} vertices")
        
        print("-" * 80)
    
    # Save to file
    output_file = "decoded_aztec.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (aztec_type, data) in enumerate(decoded_data_list, 1):
            f.write(f"Aztec Code #{i}\n")
            f.write(f"Type: {aztec_type}\n")
            f.write(f"Data: {data}\n")
            f.write("\n")
    
    print(f"\n💾 Decoded data saved to: {output_file}")
    print("=" * 80)
    
    return decoded_data_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_aztec.py <image_path>")
        print("\nExample:")
        print("  python decode_aztec.py aztec.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = decode_aztec(image_path)
    
    if results:
        print("\n✅ DECODING SUCCESSFUL!")
        print(f"Total decoded Aztec codes: {len(results)}")
        for i, (aztec_type, data) in enumerate(results, 1):
            print(f"\n{i}. [{aztec_type}] {data}")
    else:
        print("\n❌ DECODING FAILED")
        sys.exit(1)
