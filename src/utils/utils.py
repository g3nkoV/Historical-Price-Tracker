# Crossowe funkcje w projekcie
from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
import os

def open_cv_preprocess(image_path):

    #image = cv2.imread(r"str(image_path)")
    image_path = str(image_path)

    # Load the image
    image = cv2.imread(image_path)

    print(f"Attempting to load image from: {image_path}")
    if image is None:
        print(f"Błąd: Nie można otworzyć zdjęcia w {image_path}")
        return None


    print("Image loaded successfully")

    # Resize the image to double its size to increase the accuracy of OCR on smaller text
    #h, w) = image.shape[:2]
    #image = cv2.resize(image, (w * 0.5, h * 0.5))

    #image = get_grayscale(image)
    #image = remove_noise(image)
    #image = thresholding(image)
    #image = dilate(image)
    image = erode(image)
    #image = canny(image)
    #image = opening(image)
    #image = match_template(image)


    return image


# Funkcja do przetwarzania wstępnego obrazu dla OCR
def PIL_preprocess(image_path):
    image = Image.open(image_path)
    # Konwersja do skali szarości
    image = image.convert('L')
    # Zwiększenie kontrastu
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2)
    # Zastosowanie rozmycia, aby zmniejszyć szum
    image = image.filter(ImageFilter.MedianFilter(size=3))
    # Binaryzacja obrazu
    threshold = 200
    image= image.point(lambda p: p > threshold and 255)
    return image

#Dodatkowe funkcje do czytania paragonów

#Ustawienie skali szarości zdjęcia - lepiej czyta png
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#Usunięcie szumu przez wykorzystanie rozmycia medianowego (środkowego)
def remove_noise(image):
    return cv2.medianBlur(image, 5)

#Progowanie obrazu - uzyskanie obrazu binarnego metodą OTSU. Zasadniczo grupuje piksele na ciemne i jasne
#Foreground i background
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

#Dylatacja - przydaje się w momencie gdy pewne znaki są przerwane. Wzmacnia litery
def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

#Erozja - rozrzedza znaki, które są bardzo grube i mogą wtedy na siebie nachodzić. Odwrotność dilate
def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

#Otwarcie - odpowiada za dobra kolejność - najpierw erosion a potem dilate
def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

#Detekcja krawędzi Canny'ego
def canny(image):
    return cv2.Canny(image, 100, 200)

#Wykrrycie pochylenia zdjęcia - w przypadku paragonow nie potrzebne. Dla dokumentów skanowanych albo zdjęć
def deskew(image):
    coords = np.column_stack(np.where(image>0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle =-(90 + angle)
    else:
        angle = -angle
    (h,w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center,angle,1.0)
    rotated = cv2.warpAffine(image, M, (w,h),flags = cv2.INTER_CUBIC, borderMode = cv2.BORDER_REPLICATE)

    return rotated

#Template matching
def match_template(image, template):
    return cv2.matchTemplate(image,template,cv2.TM_CCORR_NORMED)