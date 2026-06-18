import json
import os

class ManualeDAO:
    def __init__(self, file_path=None):
        # Se non viene passato un percorso, calcola quello di default per il manuale
        if file_path is None:
            cartella_progetto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.file_path = os.path.join(cartella_progetto, "data", "database_manuale.json")
        else:
            self.file_path = file_path

    def leggi_tutti_problemi(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                dati = json.load(f)
                
                # Mantiene la flessibilità in lettura per sicurezza
                if isinstance(dati, dict):
                    return dati.get("problematiche", [])
                elif isinstance(dati, list):
                    return dati
                return []
        except (json.JSONDecodeError, IOError):
            return []
        
    def scrivi_tutti_problemi(self, dati):
        """Sovrascrive il file JSON salvando SEMPRE una lista pura di dati (evita conflitti)."""
        # CORREZIONE: Eliminiamo l'if-else sul nome del file.
        # Salviamo la lista pura sia per l'app che per il manuale.
        output = dati 

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4, ensure_ascii=False)