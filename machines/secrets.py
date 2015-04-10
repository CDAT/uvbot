import json
import os

__all__ = [
    'SECRETS',
]

json_path = os.path.join(os.path.dirname(__file__), 'secrets.json')
with open(json_path, 'r') as fin:
    SECRETS = json.load(fin)
