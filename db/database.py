import os
import pickle
from typing import List

class Database:
    """
    Database class for storing and loading student data.
    """

    def __init__(self):
        """
        Initializes the database
        Creates the "students.data" file if it doesn't already exist.
        """
        os.makedirs("db", exist_ok=True)  
        self.path = os.path.join("db", "students.data")
        print(f"[DB] Using {self.path}")  
        self._ensure_file()

    def _ensure_file(self):
        """
        Ensures the existence of the student data file.
        This file stores the serialized list of student data.
        """
        if not os.path.exists(self.path):
            print(f"[DEBUG][DB] Creating new data file at {self.path}")
            with open(self.path, "wb") as f:
                pickle.dump([], f)

    def read_from_file(self) -> List:
        """
        Reads data from the file (`students.data`).
        """
        try:
            with open(self.path, "rb") as f:
                data = pickle.load(f)
                return data
        except Exception as e:
            print(f"[ERROR][DB] Failed reading {self.path}: {e}")
            return [] 

    def write_to_file(self, data_list: List):
        """
        Writes the given list of data to the file (`students.data`).
        """
        try:
            with open(self.path, "wb") as f:
                pickle.dump(data_list, f) 
        except Exception as e:
            print(f"[ERROR][DB] Failed writing {self.path}: {e}")

    def clear_all(self):
        """
        Clears all data in the database by overwriting the file with an empty list.
        """
        self.write_to_file([]) 
