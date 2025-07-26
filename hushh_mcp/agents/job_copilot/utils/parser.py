'''
import json
from consent_protocol import requestConsent, validateToken

def load_json(path: str, token: str) -> dict:
    if not validateToken(token):
        raise PermissionError("No consent")
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in file: {path}")

def save_json(path: str, data: dict, token: str) -> None:
    if not validateToken(token):
        raise PermissionError("No consent")
    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary")
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise IOError(f"Failed to write to file {path}: {e}")
    '''