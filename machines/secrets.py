import json
import os

__all__ = [
    'SECRETS',
]

if 'KW_BUILDBOT_PRODUCTION' in os.environ:
    json_path = os.path.join(os.path.dirname(__file__), 'secrets.json')
    with open(json_path, 'r') as fin:
        SECRETS = json.load(fin)
else:
    class DummySecrets(object):
        def __init__(self, types):
            self.types = types
        def __getitem__(self, name):
            if len(self.types) == 1:
                return self.types[0]()
            return DummySecrets(self.types[1:])
    SECRETS = DummySecrets((DummySecrets, str,))
