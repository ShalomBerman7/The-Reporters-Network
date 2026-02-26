import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from analytics_service.consumer import KafkaConsumer
from analytics_service.kafka_publisher import KafkaPublisher
from analytics_service.text_analyzer import TextAnalyzer
from shared.logger import get_logger

logger = get_logger('AnalyticsService')


def main():
    logger.info("Starting Analytics Service...")

    analyzer = TextAnalyzer()
    consumer = KafkaConsumer(topics=['CLEAN'], group_id='analytics_group')
    publisher = KafkaPublisher()

    def handle_message(clean_data):
        try:
            file_name = clean_data.get('file_name', 'unknown')

            analyzed_data = analyzer.process_message(clean_data)

            publisher.publish('ANALYTICS', analyzed_data)

            logger.info(f"Successfully analyzed and published: {file_name}")

        except Exception as e:
            logger.error(f"Failed to analyze message: {e}")

    try:
        consumer.listen(get_data=handle_message)
    except KeyboardInterrupt:
        logger.info("Analytics Service stopped by user")


if __name__ == "__main__":
    main()