import os
import json
from google.cloud import firestore

FIRESTORE_RULES = "config/firestore_rules.json"
STRUCTURED_DATA_DIR = "structured_data"

def load_firestore_rules(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def validate_record(record):
    return all(key in record and record[key] for key in ["name", "calories"])

def sync_firestore():
    db = firestore.Client()
    rules = load_firestore_rules(FIRESTORE_RULES)

    for file_name in os.listdir(STRUCTURED_DATA_DIR):
        api_name = file_name.split("_")[0].capitalize()
        collection_path = rules.get(api_name, "")
        
        with open(os.path.join(STRUCTURED_DATA_DIR, file_name), "r") as f:
            data = json.load(f)
        
        for record in data:
            if validate_record(record):
                doc_ref = db.collection(collection_path).document(record["name"])
                existing_data = doc_ref.get().to_dict()
                if existing_data != record:
                    doc_ref.set(record)
                    print(f"Sincronizado: {record['name']} en {collection_path}")
