import os
import json

class Database:
    FILE = "students.txt"

    @classmethod
    def load(cls):
        if not os.path.exists(cls.FILE):
            cls._initialize()
        try:
            with open(cls.FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    @classmethod
    def save(cls, data):
        with open(cls.FILE, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def clear(cls):
        cls._initialize()

    @classmethod
    def _initialize(cls):
        with open(cls.FILE, "w") as f:
            f.write("[]")
