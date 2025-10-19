import json

def replace_with_json_dict(text, json_path):
    """
    Replace substrings in `text` based on a JSON dictionary loaded from `json_path`.
    
    Args:
        text (str): Input text
        json_path (str): Path to JSON file containing {"old": "new", ...}
    
    Returns:
        str: Text with replacements applied
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        replacements = json.load(f)
    
    # Apply replacements
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text