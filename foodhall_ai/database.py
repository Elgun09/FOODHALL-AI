import json
from pathlib import Path

class Database:

    def __init__(self):
        self.file = Path("data.json")

    def load(self):
        if not self.file.exists():
            return {}

        with open(self.file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

database = Database()
