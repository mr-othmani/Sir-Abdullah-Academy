import re

def normalize_phone(phone_str: str) -> str:
    cleaned = re.sub(r'[^\d+]', '', phone_str.strip())
    if cleaned.startswith("03"):
        return "+92" + cleaned[1:]
    elif cleaned.startswith("3") and len(cleaned) == 10:
        return "+92" + cleaned
    elif cleaned.startswith("92") and not cleaned.startswith("+"):
        return "+" + cleaned
    return cleaned

def sanitize_csv_field(value):
    if isinstance(value, str):
        if value.startswith(('=', '+', '-', '@')):
            return "'" + value
    return value
