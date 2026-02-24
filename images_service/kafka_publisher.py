import json
from confluent_kafka import Producer
from shared.logger import get_logger
import os


class KafkaPublisher:
    def __init__(self):
        servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')

        conf = {
            'bootstrap.servers': servers,
            'client.id': 'images-service'
        }
        self.logger = get_logger('KafkaPublisher')

        try:
            self.producer = Producer(conf)
            self.logger.info(f"Kafka Producer connected to {servers}")
        except Exception as e:
            self.logger.error(f"Failed to create Kafka Producer: {e}")

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f"Message delivery failed: {err}")
        else:
            self.logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

    def publish(self, topic, data):
        try:
            payload = json.dumps(data).encode('utf-8')
            self.producer.produce(topic, payload, callback=self.delivery_report)

            self.producer.flush()
        except Exception as e:
            self.logger.error(f"Error publishing to Kafka: {e}")
