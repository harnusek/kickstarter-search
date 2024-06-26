import os
import json
from elasticsearch import Elasticsearch

directory = "data/"
es = Elasticsearch([{'host': '127.0.0.1', 'port': 9200}])

if __name__ == "__main__":
    for doc_name in os.listdir(directory):
        if doc_name.startswith("."):
            continue
        with open(directory + doc_name) as doc_file:
            doc = json.load(doc_file)
            doc_transformed = doc
            category = [{"name": doc["category"][0]}, {"name": doc["category"][1]}]
            doc_transformed["category"] = category
            es.index(index='kick', body=doc_transformed)
