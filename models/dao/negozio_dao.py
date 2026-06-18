import json
import os

class NegozioDAO:
    def __init__(self, file_path="data/database_negozi.json"):
        self.file_path = file_path

    def leggi_tutti_negozi(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                dati = json.load(f)
                return dati.get("negozi", [])
        except (json.JSONDecodeError, IOError):
            return []