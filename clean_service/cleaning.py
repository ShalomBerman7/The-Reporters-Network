import re


class DataCleaner:
    def clean_text(self, text):
        if not text:
            return ""
        cleaned = re.sub(r'[^\w\sא-ת]', '', text)
        cleaned = " ".join(cleaned.split())
        return cleaned

    def process_message(self, data):
        raw_text = data.get('text', '')
        cleaned_text = self.clean_text(raw_text)

        processed_data = {
            **data,
            "clean text": cleaned_text,
            "status": "cleaned"
        }
        return processed_data
