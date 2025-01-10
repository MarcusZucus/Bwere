import os
import json

RAW_DATA_DIR = "raw_data"
STRUCTURED_DATA_DIR = "structured_data"
MAPPINGS_FILE = "config/mappings.json"

def load_mappings(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def normalize_record(record, mapping):
    normalized = {}
    for key, path in mapping.items():
        keys = path.split(".")
        value = record
        for k in keys:
            if "[" in k:
                k, index = k[:-1].split("[")
                value = value.get(k, [])[int(index)]
            else:
                value = value.get(k)
            if value is None:
                break
        normalized[key] = value
    return normalized

def normalize_data():
    os.makedirs(STRUCTURED_DATA_DIR, exist_ok=True)
    mappings = load_mappings(MAPPINGS_FILE)

    for file_name in os.listdir(RAW_DATA_DIR):
        api_name = file_name.split(".")[0].capitalize()
        mapping = mappings.get(api_name, {})
        
        with open(os.path.join(RAW_DATA_DIR, file_name), "r") as f:
            raw_data = json.load(f)

        structured_data = [normalize_record(record, mapping) for record in raw_data]
        with open(os.path.join(STRUCTURED_DATA_DIR, f"{api_name.lower()}_structured.json"), "w") as f:
            json.dump(structured_data, f, indent=4)
