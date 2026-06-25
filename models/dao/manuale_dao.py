import json
import os
import sys

class ManualeDAO:
    def __init__(self, file_path=None):
        # 1. QUI VA INSERITO IL BLOCCO: Calcola la cartella in base a come è avviata l'app
        if "__compiled__" in globals():
            # Se siamo su Nuitka, sys.argv[0] è il percorso reale del file main.exe
            cartella_progetto = os.path.dirname(os.path.abspath(sys.argv[0]))
        elif getattr(sys, 'frozen', False):
            # Se siamo su PyInstaller
            cartella_progetto = os.path.dirname(os.path.abspath(sys.executable))
        else:
            # Se siamo in sviluppo su VS Code
            cartella_dao = os.path.dirname(os.path.abspath(__file__))
            cartella_models = os.path.dirname(cartella_dao)
            cartella_progetto = os.path.dirname(cartella_models)

        # 2. Subito dopo, usi "cartella_progetto" per stabilire il percorso del file JSON
        if file_path is None:
            self.file_path = os.path.join(cartella_progetto, "data", "database_manuale.json")
        else:
            nome_file = os.path.basename(file_path)
            self.file_path = os.path.join(cartella_progetto, "data", nome_file)

    # ... a seguire tutti gli altri metodi (leggi_tutti_problemi, ecc.) indendati correttamente

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
        output = dati 

        # Assicurati che la cartella 'data' esista sul PC prima di scrivere, altrimenti creala
        cartella_data = os.path.dirname(self.file_path)
        if not os.path.exists(cartella_data):
            os.makedirs(cartella_data, exist_ok=True)

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4, ensure_ascii=False)