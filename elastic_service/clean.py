from elasticsearch import Elasticsearch

es = Elasticsearch(["http://localhost:9200"])
INDEX_NAME = "reporters_network"

if es.indices.exists(index=INDEX_NAME):
    es.indices.delete(index=INDEX_NAME)
    print(f"Index '{INDEX_NAME}' deleted successfully. Ready for a fresh start!")
else:
    print("Index does not exist. Nothing to delete.")