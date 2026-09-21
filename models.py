import json
import os

def load_json(filepath, default_value):
    if not os.path.exists(filepath):
        return default_value
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return default_value

def save_json(filepath, data):
    backup_path = filepath + ".bak"
    if os.path.exists(filepath):
        os.replace(filepath, backup_path)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
