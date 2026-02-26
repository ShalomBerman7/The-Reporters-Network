import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kafka_publisher import KafkaPublisher
from clean_service.kafka_consumer import KafkaConsumer
from clean_service.cleaning import DataCleaner
from shared.logger import get_logger

logger = get_logger('CleanService-Main')


def main():
    logger.info("Starting Clean Service...")

    cleaner = DataCleaner()
    consumer = KafkaConsumer()
    publisher = KafkaPublisher()

    def handle_message(raw_data):
        try:
            file_name = raw_data.get('file_name', 'unknown')

            cleaned_data = cleaner.process_message(raw_data)

            publisher.publish('CLEAN', cleaned_data)

            logger.info(f"Successfully cleaned and published: {file_name}")
            pretty_json = json.dumps(cleaned_data, indent=4, ensure_ascii=False)
            logger.info(f"Full processed data:\n{pretty_json}")

        except Exception as e:
            logger.error(f"Failed to process and publish: {e}")

    try:
        consumer.listen(topic='RAW', callback=handle_message)
    except KeyboardInterrupt:
        logger.info("Clean Service stopped by user")


if __name__ == "__main__":
    main()
