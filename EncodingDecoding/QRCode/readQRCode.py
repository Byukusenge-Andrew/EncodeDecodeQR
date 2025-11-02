import cv2, numpy, sys
if len(sys.argv) > 1:
    inputImage = cv2.imread(sys.argv[1])
else:
    print("No input image found!")
    sys.exit()
qrDecoder = cv2.QRCodeDetector()
data, _, foundQRCodeImg = qrDecoder.detectAndDecode(inputImage)
if len(data) > 0:
    print("Decoded Data :\n*******************\n{}\n*******************".format(data))
    cv2.imshow("Detected QRCode", numpy.uint8(foundQRCodeImg))
    cv2.imwrite("found_qr_code.png", foundQRCodeImg)
else:
    print("No QR Code detected!")
    sys.exit()
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break

cv2.destroyAllWindows()