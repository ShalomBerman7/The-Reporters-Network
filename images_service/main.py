from fastapi import FastAPI
from images_service.load_images import ImageIngestionService

app = FastAPI()
service = ImageIngestionService()

@app.get("/process")
def get_images():
    return service.run_images_data()
