"""
1D Barcode Decoder - Complete Implementation
Decodes all types of 1D barcodes (EAN, UPC, Code128, etc.)
"""

from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import sys
import os

def decode_barcode(image_path):
    """
    Decode 1D barcode from image
    
    Args:
        image_path: Path to the image file
    
    Returns:
        List of decoded data or None
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return None
    
    print("=" * 80)
    print("1D BARCODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}\n")
    
    try:
        # Method 1: Try with PIL
        print("Method 1: Decoding with PIL...")
        pil_image = Image.open(image_path)
        decoded_pil = decode(pil_image)
        
        if decoded_pil:
            print("✅ Successfully decoded with PIL!\n")
            return process_results(decoded_pil, image_path)
        
        # Method 2: Try with OpenCV
        print("Method 2: Decoding with OpenCV...")
        cv_image = cv2.imread(image_path)
        decoded_cv = decode(cv_image)
        
        if decoded_cv:
            print("✅ Successfully decoded with OpenCV!\n")
            return process_results(decoded_cv, image_path)
        
        # Method 3: Try with grayscale
        print("Method 3: Decoding with grayscale conversion...")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        decoded_gray = decode(gray)
        
        if decoded_gray:
            print("✅ Successfully decoded with grayscale!\n")
            return process_results(decoded_gray, image_path)
        
        # Method 4: Try with preprocessing
        print("Method 4: Decoding with image preprocessing...")
        # Apply thresholding
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        decoded_binary = decode(binary)
        
        if decoded_binary:
            print("✅ Successfully decoded with binary threshold!\n")
            return process_results(decoded_binary, image_path)
        
        # Method 5: Try with adaptive thresholding
        print("Method 5: Decoding with adaptive thresholding...")
        adaptive = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                        cv2.THRESH_BINARY, 11, 2)
        decoded_adaptive = decode(adaptive)
        
        if decoded_adaptive:
            print("✅ Successfully decoded with adaptive thresholding!\n")
            return process_results(decoded_adaptive, image_path)
        
        print("❌ No barcode found with any method!")
        print("\nPossible reasons:")
        print("  - The image doesn't contain a 1D barcode")
        print("  - The barcode is damaged or unclear")
        print("  - Image quality is too low")
        print("  - Barcode type not supported")
        return None
        
    except Exception as e:
        print(f"❌ Error during decoding: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def process_results(decoded_objects, image_path):
    """Process and display decoded results"""
    
    print("=" * 80)
    print(f"✅ Found {len(decoded_objects)} barcode(s)")
    print("=" * 80)
    
    decoded_data_list = []
    
    for i, obj in enumerate(decoded_objects, 1):
        # Decode data
        try:
            barcode_data = obj.data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                barcode_data = obj.data.decode('latin-1')
            except:
                barcode_data = str(obj.data)
        
        barcode_type = obj.type
        decoded_data_list.append((barcode_type, barcode_data))
        
        # Display information
        print(f"\nBarcode #{i}")
        print(f"  Type: {barcode_type}")
        print(f"  Data: {barcode_data}")
        print(f"  Raw Bytes: {obj.data}")
        
        # Position information
        if hasattr(obj, 'rect'):
            rect = obj.rect
            print(f"  Position: x={rect.left}, y={rect.top}")
            print(f"  Size: {rect.width} x {rect.height} pixels")
        
        # Quality
        if hasattr(obj, 'quality'):
            print(f"  Quality: {obj.quality}")
        
        print("-" * 80)
    
    # Save to file
    output_file = "decoded_barcode.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (barcode_type, data) in enumerate(decoded_data_list, 1):
            f.write(f"Barcode #{i}\n")
            f.write(f"Type: {barcode_type}\n")
            f.write(f"Data: {data}\n")
            f.write("\n")
    
    print(f"\n💾 Decoded data saved to: {output_file}")
    print("=" * 80)
    
    return decoded_data_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_barcode.py <image_path>")
        print("\nExample:")
        print("  python decode_barcode.py barcode.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = decode_barcode(image_path)
    
    if results:
        print("\n✅ DECODING SUCCESSFUL!")
        print(f"Total decoded barcodes: {len(results)}")
        for i, (barcode_type, data) in enumerate(results, 1):
            print(f"\n{i}. [{barcode_type}] {data}")
    else:
        print("\n❌ DECODING FAILED")
        sys.exit(1)
