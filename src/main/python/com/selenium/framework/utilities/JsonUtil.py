import json


class JsonUtil:
    def __init__(self, data_path):
        self.data_path = data_path

    def load_json(self, data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
            self.list = self.data['data']
            return self.list
