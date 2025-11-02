from pyzxing import BarCodeReader
import sys
import os

if len(sys.argv) < 2:
    print("Usage: python decode_with_pyzxing.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

if not os.path.exists(image_path):
    print(f"Error: Image file '{image_path}' not found!")
    sys.exit(1)

print("=" * 60)
print("Decoding PDF417 with pyzxing")
print("=" * 60)
print(f"Image: {image_path}\n")

try:
    # Create a barcode reader
    reader = BarCodeReader()
    
    # Decode the barcode
    result = reader.decode(image_path)
    
    # Check if the barcode was decoded
    if result:
        print("✓ Barcode decoded successfully!\n")
        
        for idx, barcode in enumerate(result):
            print(f"Barcode #{idx + 1}:")
            print(f"  Format: {barcode.get('format', 'Unknown')}")
            
            # Try to get the decoded text
            if 'parsed' in barcode:
                try:
                    decoded_text = barcode['parsed'].decode('utf-8')
                except:
                    decoded_text = str(barcode['parsed'])
            elif 'raw' in barcode:
                decoded_text = barcode['raw']
            else:
                decoded_text = str(barcode)
            
            print(f"  Decoded Text:")
            print(f"  {decoded_text}")
            print()
            
            # Save to file
            with open("decoded_pdf417.txt", "w", encoding='utf-8') as f:
                f.write(decoded_text)
            print(f"✓ Decoded text saved to 'decoded_pdf417.txt'")
    else:
        print("✗ No barcode detected or decoding failed.")
        print("\nTroubleshooting:")
        print("1. Make sure the image is clear and well-lit")
        print("2. Try scanning the barcode with your phone camera")
        print("3. The image might be too low quality or damaged")
        
except Exception as e:
    print(f"✗ Error during decoding: {e}")
    print("\nMake sure pyzxing is installed:")
    print("  pip install pyzxing")
    
print("\n" + "=" * 60)
