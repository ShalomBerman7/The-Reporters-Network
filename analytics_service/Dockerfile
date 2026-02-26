FROM python:3.11-slim
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-heb
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV PYTHONPATH=/app
CMD ["python", "analytics_service/main.py"]