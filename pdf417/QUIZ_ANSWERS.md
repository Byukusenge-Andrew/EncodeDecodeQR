# PDF417 Barcode Quiz Answers

## Question 1a: What kind of barcode is this?
**Answer:** PDF417 Code

## Question 1b: Were you able to decode it successfully?
**Answer:** Yes

## Question 1c: What is the decoded text? (or failure message)
**Answer:** 
```
1 1977 8 00036890 240228022034B AZIRAMWABO Gabriel
```

### Decoded Information Analysis:
- **1** - Possible ID type or category
- **1977** - Likely birth year
- **8** - Possible gender code or region code
- **00036890** - ID number
- **240228022034B** - Possible issue date (24-02-28) and reference number
- **AZIRAMWABO Gabriel** - Full name

## Question 1d: Link to the script you used
**Script Location:** `d:\Copy of studies\Y3\Embedded\codes\QRCode\pdf417\comprehensive_decoder.py`

**GitHub Repository:** https://github.com/benax-rw/Computer-Vision-for-Intelligent-Robotics-Part-01/tree/master/EncodingDecoding

### Decoding Methods Used:
The comprehensive decoder implements multiple approaches:
1. pyzbar with PIL
2. OpenCV with pyzbar
3. Grayscale conversion
4. Binary thresholding
5. Otsu's thresholding
6. Adaptive thresholding
7. Contrast enhancement (Histogram Equalization)
8. CLAHE (Contrast Limited Adaptive Histogram Equalization)
9. Image rotation (90°, 180°, 270°)
10. ZXing Java library

### Technical Implementation:
- **Primary Library:** pyzbar (Python wrapper for ZBar)
- **Image Processing:** OpenCV (cv2)
- **Preprocessing:** Multiple threshold techniques and contrast enhancement
- **Fallback:** ZXing Java library for robust decoding

### Dependencies:
```
opencv-python>=4.5.0
pyzbar>=0.1.9
Pillow>=8.0.0
numpy>=1.19.0
```

---
**Student:** Byukusenge Andrew  
**Date:** November 2, 2025  
**Course:** Y3 Embedded Systems
