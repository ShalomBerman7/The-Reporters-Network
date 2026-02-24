import os
import uuid
from datetime import datetime
from PIL import Image


class MetadataExtractor:
    def get_metadata_from_image(self, image_path, text):
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                file_format = img.format
                color_mode = img.mode
            file_stats = os.stat(image_path)
            file_size_kb = round(file_stats.st_size / 1024, 2)
            creation_time = datetime.fromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            metadata = {
                "image_id": str(uuid.uuid4()),
                "file_name": os.path.basename(image_path),
                "format": file_format,
                "dimensions": f"{width}x{height}",
                "width": width,
                "height": height,
                "size_kb": file_size_kb,
                "color_mode": color_mode,
                "created_at": creation_time,
                "text": text
            }
            return metadata
        except Exception as e:
            return {"error": f"Failed to extract metadata: {str(e)}"}
