import json
import os


class DB:
    def __init__(self):
        self.db = {}
        self.path = os.path.join(os.getcwd(), "data.json")
        self.load()

    def load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                self.db = json.load(f)

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.db, f, indent=4)

    def get(self, key):
        return self.db.get(key)

    def set(self, key, value):
        self.db[key] = value
        self.save()

    def add(self, key, value):
        if key not in self.db:
            self.db[key] = []
        self.db[key].append(value)
        self.save()

    def delete(self, key):
        del self.db[key]
        self.save()

    def all(self):
        return self.db

    def clear(self):
        self.db = {}
        self.save()
