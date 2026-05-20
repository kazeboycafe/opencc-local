import json
import logging

# Simple cache to avoid reading JSON file multiple times
_REPLACEMENTS_CACHE = {}

def load_replacements(json_path):
    """
    Load replacement dictionary from JSON file with caching.
    Returns empty dict if file missing or invalid.
    """
    if json_path in _REPLACEMENTS_CACHE:
        return _REPLACEMENTS_CACHE[json_path]
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            replacements = json.load(f)
        _REPLACEMENTS_CACHE[json_path] = replacements
        return replacements
    except FileNotFoundError:
        logging.warning(f"Extra replacement file not found: {json_path}")
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in {json_path}: {e}")
    except Exception as e:
        logging.error(f"Failed to load {json_path}: {e}")
    
    _REPLACEMENTS_CACHE[json_path] = {}
    return {}

def replace_with_json_dict(text, json_path):
    """Legacy function for compatibility; uses load_replacements."""
    replacements = load_replacements(json_path)
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text