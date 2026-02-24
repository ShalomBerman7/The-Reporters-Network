import pytesseract
from PIL import Image

class OCREngine:
    def __init__(self, tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def get_text(self, image_path):
        try:
            image = Image.open(image_path)
            return pytesseract.image_to_string(image, lang='heb+eng')
        except Exception as e:
            return f'error: {str(e)}'
