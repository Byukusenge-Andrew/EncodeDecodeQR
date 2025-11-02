"""
QR Code Decoder - Complete Implementation
Decodes all types of QR codes
"""

from pyzbar.pyzbar import decode
from PIL import Image
import cv2
import sys
import os

def decode_qrcode(image_path):
    """
    Decode QR code from image
    
    Args:
        image_path: Path to the image file
    
    Returns:
        List of decoded data or None
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return None
    
    print("=" * 80)
    print("QR CODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}\n")
    
    try:
        # Method 1: Try with pyzbar + PIL
        print("Method 1: Decoding with pyzbar + PIL...")
        pil_image = Image.open(image_path)
        decoded_pil = decode(pil_image)
        
        if decoded_pil:
            print("✅ Successfully decoded with pyzbar + PIL!\n")
            return process_results(decoded_pil, image_path)
        
        # Method 2: Try with pyzbar + OpenCV
        print("Method 2: Decoding with pyzbar + OpenCV...")
        cv_image = cv2.imread(image_path)
        decoded_cv = decode(cv_image)
        
        if decoded_cv:
            print("✅ Successfully decoded with pyzbar + OpenCV!\n")
            return process_results(decoded_cv, image_path)
        
        # Method 3: Try with OpenCV QRCodeDetector
        print("Method 3: Decoding with OpenCV QRCodeDetector...")
        qrDecoder = cv2.QRCodeDetector()
        data, vertices_array, _ = qrDecoder.detectAndDecode(cv_image)
        
        if data:
            print("✅ Successfully decoded with OpenCV QRCodeDetector!\n")
            print("=" * 80)
            print("✅ Found 1 QR code")
            print("=" * 80)
            print(f"\nQR Code #1")
            print(f"  Type: QRCODE")
            print(f"  Data: {data}")
            print(f"  Data Length: {len(data)} characters")
            
            if vertices_array is not None:
                print(f"  Vertices: {vertices_array}")
            
            print("-" * 80)
            
            # Save to file
            output_file = "decoded_qrcode.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"QR Code:\n")
                f.write(f"{data}\n")
            
            print(f"\n💾 Decoded data saved to: {output_file}")
            print("=" * 80)
            
            return [('QRCODE', data)]
        
        # Method 4: Try with grayscale
        print("Method 4: Decoding with grayscale conversion...")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        decoded_gray = decode(gray)
        
        if decoded_gray:
            print("✅ Successfully decoded with grayscale!\n")
            return process_results(decoded_gray, image_path)
        
        # Method 5: Try with preprocessing
        print("Method 5: Decoding with image preprocessing...")
        _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        decoded_binary = decode(binary)
        
        if decoded_binary:
            print("✅ Successfully decoded with binary threshold!\n")
            return process_results(decoded_binary, image_path)
        
        print("❌ No QR code found with any method!")
        print("\nPossible reasons:")
        print("  - The image doesn't contain a QR code")
        print("  - The QR code is damaged or unclear")
        print("  - Image quality is too low")
        return None
        
    except Exception as e:
        print(f"❌ Error during decoding: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def process_results(decoded_objects, image_path):
    """Process and display decoded results"""
    
    print("=" * 80)
    print(f"✅ Found {len(decoded_objects)} QR code(s)")
    print("=" * 80)
    
    decoded_data_list = []
    
    for i, obj in enumerate(decoded_objects, 1):
        # Decode data
        try:
            qr_data = obj.data.decode('utf-8')
        except UnicodeDecodeError:
            try:
                qr_data = obj.data.decode('latin-1')
            except:
                qr_data = str(obj.data)
        
        qr_type = obj.type
        decoded_data_list.append((qr_type, qr_data))
        
        # Display information
        print(f"\nQR Code #{i}")
        print(f"  Type: {qr_type}")
        print(f"  Data: {qr_data}")
        print(f"  Raw Bytes: {obj.data}")
        
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
            print(f"  Polygon points: {obj.polygon}")
        
        print("-" * 80)
    
    # Save to file
    output_file = "decoded_qrcode.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, (qr_type, data) in enumerate(decoded_data_list, 1):
            f.write(f"QR Code #{i}\n")
            f.write(f"Type: {qr_type}\n")
            f.write(f"Data: {data}\n")
            f.write("\n")
    
    print(f"\n💾 Decoded data saved to: {output_file}")
    print("=" * 80)
    
    return decoded_data_list

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_qrcode.py <image_path>")
        print("\nExample:")
        print("  python decode_qrcode.py qrcode.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = decode_qrcode(image_path)
    
    if results:
        print("\n✅ DECODING SUCCESSFUL!")
        print(f"Total decoded QR codes: {len(results)}")
        for i, (qr_type, data) in enumerate(results, 1):
            print(f"\n{i}. [{qr_type}] {data}")
    else:
        print("\n❌ DECODING FAILED")
        sys.exit(1)
