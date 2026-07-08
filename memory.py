from datetime import datetime

class Memory:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = {
            "value": value,
            "time": datetime.now().isoformat()
        }

    def get(self, key):
        item = self.data.get(key)
        if item:
            return item["value"]
        return None

memory = Memory()
