FROM python:3.11-slim

RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-heb libtesseract-dev

WORKDIR /app
COPY ../requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# הגדרת משתנה סביבה כדי שפייתון יזהה את התיקייה הנוכחית
ENV PYTHONPATH=/app

CMD ["uvicorn", "images_service.main:app", "--host", "0.0.0.0", "--port", "8000"]