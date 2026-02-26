import os
import sys
from elasticsearch import Elasticsearch

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from kafka_consumer import KafkaConsumer
from shared.logger import get_logger


logger = get_logger("ElasticService")

ES_URL = os.getenv('ELASTICSEARCH_URL', "http://localhost:9200")
es = Elasticsearch(ES_URL)
INDEX_NAME = "reporters_network"


def create_index_if_not_exists():
    mapping = {
        "mappings": {
            "properties": {
                "image_id": {"type": "keyword"},
                "file_name": {"type": "keyword"},
                "format": {"type": "keyword"},
                "text": {"type": "text", "analyzer": "standard"},
                "content": {"type": "text", "analyzer": "standard"},
                "created_at": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss||strict_date_optional_time"},
                "dimensions": {"type": "keyword"},
                "status": {"type": "keyword"}
            }
        }
    }
    try:
        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME, body=mapping)
            logger.info(f"Created new index: {INDEX_NAME} with professional mapping")
        else:
            logger.info(f"Index '{INDEX_NAME}' exists and is ready")
    except Exception as e:
        logger.error(f"Error during index creation: {e}")


def save_to_elastic(data):
    image_id = data.get('image_id')
    if not image_id:
        logger.warning("Message received without image_id. Ignoring.")
        return

    try:
        es.update(
            index=INDEX_NAME,
            id=image_id,
            body={"doc": data, "doc_as_upsert": True}
        )
        logger.info(f"Indexed/Updated image: {image_id} (Source: {data.get('file_name', 'unknown')})")
    except Exception as e:
        logger.error(f"Failed to index image {image_id}: {e}")

create_index_if_not_exists()
consumer = KafkaConsumer(topics=['RAW', 'CLEAN', 'ANALYTICS'], group_id='elastic_indexer_group')
consumer.listen(save_to_elastic)
