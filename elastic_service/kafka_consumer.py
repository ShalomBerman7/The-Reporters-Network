import json
import os
from confluent_kafka import Consumer
from shared.logger import get_logger


class KafkaConsumer:
    def __init__(self, topics, group_id='elastic_group'):

        if isinstance(topics, str):
            self.topics = [topics]
        else:
            self.topics = topics

        self.logger = get_logger('KafkaConsumer')

        servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')

        conf = {
            'bootstrap.servers': servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.partition.eof': False
        }

        self.consumer = Consumer(conf)
        self.consumer.subscribe(self.topics)
        self.logger.info(f"Consumer connected to {servers}")

    def listen(self, save_to_elastic):
        self.logger.info(f"Listening to topic: {self.topics}")

        try:
            while True:
                msg = self.consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == 3:
                        continue
                    self.logger.error(f"Consumer error: {msg.error()}")
                    continue

                data = json.loads(msg.value().decode('utf-8'))

                file_name = data.get('file_name', 'unknown')
                self.logger.info(f"New message received: {file_name}")

                save_to_elastic(data)

        finally:
            self.consumer.close()
