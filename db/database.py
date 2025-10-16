import os
import pickle
from typing import List

class Database:
    def __init__(self):
        os.makedirs("db", exist_ok=True)
        self.path = os.path.join("db", "students.data")
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.path):
            print(f"[DEBUG][DB] Creating new data file at {self.path}")
            with open(self.path, "wb") as f:
                pickle.dump([], f)

    def read_from_file(self) -> List:
        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)
                return data
        except Exception as e:
            print(f"[ERROR][DB] Failed reading {self.path}: {e}")
            return []

    def write_to_file(self, data_list: List):
        try:
            with open(self.path, "wb") as f:
                pickle.dump(data_list, f)
        except Exception as e:
            print(f"[ERROR][DB] Failed writing {self.path}: {e}")

    def clear_all(self):
        self.write_to_file([])
        
