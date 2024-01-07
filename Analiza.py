import pytesseract
pytesseract.pytesseract.tesseract_cmd=r"D:\\Program Files (x86)\\Tesseract_OCR\\tesseract.exe"
from PIL import Image
import os


# Path to the directory containing all your png receipts
directory_path = './Paragony'
all_pngs = [f for f in os.listdir(directory_path) if f.endswith('.png')]

if(all_pngs):
# Process only the first png file for testing purposes
    first_png = all_pngs[0]
    image_path = os.path.join(directory_path, first_png)
    receipt_image = Image.open(image_path)

    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(receipt_image, lang='pol')

    # Output the extracted text
    print(text)
else:
    print("No PNG files found in the directory.")



#print(text)


#result = reader.readtext('./Paragony/2019.09.16_24001587120190916599614.jpg.png',detail=0)

#print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
