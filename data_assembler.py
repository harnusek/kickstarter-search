import os
import json

directory = "data/"

if __name__ == "__main__":
    with open("kickstarter_bulk.NDJSON", "w") as bulk:
        for doc_name in os.listdir(directory):
            if doc_name.startswith("."):
                continue
            with open(directory + doc_name) as doc_file:
                doc = json.load(doc_file)
                # test/rework doc
                bulk.write(json.dumps(doc, ensure_ascii=False) + ",\n")
