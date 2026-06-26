import os
import json

class TaskModel:
    def __init__(self, cartella_progetto=None):
        if not cartella_progetto:
            cartella_progetto = os.getcwd()
            
        self.file_path = os.path.join(cartella_progetto, "data", "registro_task.json")
        self._inizializza_db()

    def _inizializza_db(self):
        """Crea il file JSON vuoto se non esiste ancora."""
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4)

    def leggi_task(self):
        """Legge tutte le task salvate nel file JSON (Richiesto dal MainController)."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def salva_task(self, lista_task):
        """Sovrascrive il file JSON con la lista aggiornata (Richiesto dal MainController)."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(lista_task, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Errore nel salvataggio del registro task: {e}")
            return False