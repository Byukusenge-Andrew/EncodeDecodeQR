"""
Data Matrix Decoder - Complete Implementation
Decodes Data Matrix barcodes (ECC 200 and other variants)
"""

from pylibdmtx.pylibdmtx import decode
from PIL import Image
import sys
import os

def decode_datamatrix(image_path):
    """
    Decode Data Matrix barcode from image
    
    Args:
        image_path: Path to the image file
    
    Returns:
        List of decoded data or None
    """
    
    if not os.path.exists(image_path):
        print(f"❌ Error: Image file '{image_path}' not found!")
        return None
    
    print("=" * 80)
    print("DATA MATRIX BARCODE DECODER")
    print("=" * 80)
    print(f"Image: {image_path}\n")
    
    try:
        # Load image
        image = Image.open(image_path)
        print(f"Image size: {image.size}")
        print(f"Image mode: {image.mode}\n")
        
        # Decode Data Matrix
        print("Decoding Data Matrix barcode...\n")
        decoded_results = decode(image)
        
        if not decoded_results:
            print("❌ No Data Matrix barcode found!")
            print("\nPossible reasons:")
            print("  - The image doesn't contain a Data Matrix barcode")
            print("  - The barcode is damaged or unclear")
            print("  - Image quality is too low")
            print("  - Wrong barcode type (not Data Matrix)")
            return None
        
        # Process results
        print(f"✅ Successfully decoded {len(decoded_results)} Data Matrix barcode(s)\n")
        print("=" * 80)
        
        decoded_data_list = []
        
        for i, result in enumerate(decoded_results, 1):
            try:
                # Decode bytes to string
                decoded_text = result.data.decode('utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, try latin-1 or show raw bytes
                try:
                    decoded_text = result.data.decode('latin-1')
                except:
                    decoded_text = str(result.data)
            
            decoded_data_list.append(decoded_text)
            
            # Display result
            print(f"Data Matrix #{i}")
            print(f"  Decoded Text: {decoded_text}")
            print(f"  Data Length: {len(decoded_text)} characters")
            print(f"  Raw Bytes: {result.data}")
            
            # Position and size info if available
            if hasattr(result, 'rect'):
                rect = result.rect
                print(f"  Position: x={rect.left}, y={rect.top}")
                print(f"  Size: {rect.width} x {rect.height} pixels")
            
            print("-" * 80)
        
        # Save decoded data to file
        output_file = "decoded_datamatrix.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            for i, data in enumerate(decoded_data_list, 1):
                f.write(f"Data Matrix #{i}:\n")
                f.write(f"{data}\n")
                f.write("\n")
        
        print(f"\n💾 Decoded data saved to: {output_file}")
        print("=" * 80)
        
        return decoded_data_list
        
    except Exception as e:
        print(f"❌ Error during decoding: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python decode_datamatrix.py <image_path>")
        print("\nExample:")
        print("  python decode_datamatrix.py datamatrix.png")
        sys.exit(1)
    
    image_path = sys.argv[1]
    results = decode_datamatrix(image_path)
    
    if results:
        print("\n✅ DECODING SUCCESSFUL!")
        print(f"Total decoded messages: {len(results)}")
        for i, data in enumerate(results, 1):
            print(f"\n{i}. {data}")
    else:
        print("\n❌ DECODING FAILED")
        sys.exit(1)
