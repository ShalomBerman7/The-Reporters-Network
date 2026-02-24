import json
import os
from confluent_kafka import Consumer
from shared.logger import get_logger


class KafkaConsumer:
    def __init__(self):
        self.logger = get_logger('KafkaConsumer')
        servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')

        conf = {
            'bootstrap.servers': servers,
            'group.id': 'clean-service-group',
            'auto.offset.reset': 'earliest',
            'enable.partition.eof': False
        }

        self.consumer = Consumer(conf)
        self.logger.info(f"Consumer connected to {servers}")

    def listen(self, topic, callback):
        self.consumer.subscribe([topic])
        self.logger.info(f"Listening to topic: {topic}")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    self.logger.error(f"Consumer error: {msg.error()}")
                    break

                data = json.loads(msg.value().decode('utf-8'))

                file_name = data.get('file_name', 'unknown')
                self.logger.info(f"New message received: {file_name}")

                callback(data)

        finally:
            self.consumer.close()
