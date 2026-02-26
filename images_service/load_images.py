import os
from pathlib import Path
from images_service.image_to_text import OCREngine
from images_service.metadata import MetadataExtractor
from images_service.kafka_publisher import KafkaPublisher


class ImageIngestionService:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.path_directory = self.base_dir / 'data' / 'tweet_images'
        self.ocr = OCREngine()
        self.metadata = MetadataExtractor()
        self.publisher = KafkaPublisher()

    def run_images_data(self):
        if not self.path_directory.exists():
            return f"Directory {self.path_directory} not found."

        results = []
        for filename in os.listdir(self.path_directory):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff')):
                full_path = self.path_directory / filename

                text = self.ocr.get_text(full_path)
                data = self.metadata.get_metadata_from_image(full_path, text)

                self.publisher.publish(topic='RAW', data=data)

                results.append(data)
        return results
