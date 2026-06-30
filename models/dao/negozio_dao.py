import json
import os
import sys

class NegozioDAO:
    def __init__(self, file_path=None):
        # 1. QUI VA INSERITO IL BLOCCO: Uguale a sopra
        if "__compiled__" in globals():
            cartella_progetto = os.path.dirname(os.path.abspath(sys.argv[0]))
        elif getattr(sys, 'frozen', False):
            cartella_progetto = os.path.dirname(os.path.abspath(sys.executable))
        else:
            cartella_dao = os.path.dirname(os.path.abspath(__file__))
            cartella_models = os.path.dirname(cartella_dao)
            cartella_progetto = os.path.dirname(cartella_models)

        # 2. Usi "cartella_progetto" impostando il file di default dei negozi
        if file_path is None:
            self.file_path = os.path.join(cartella_progetto, "data", "database_negozi.json")
        else:
            nome_file = os.path.basename(file_path)
            self.file_path = os.path.join(cartella_progetto, "data", nome_file)

    def leggi_tutti_negozi(self):
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                dati = json.load(f)
                # Gestiamo sia se è un dizionario {"negozi": [...]} sia se fosse una lista pura
                if isinstance(dati, dict):
                    return dati.get("negozi", [])
                elif isinstance(dati, list):
                    return dati
                return []
        except (json.JSONDecodeError, IOError):
            return []

    def scrivi_tutti_negozi(self, dati):
        """Salva i negozi mantenendo la struttura a dizionario originale dell'anagrafica."""
        cartella_data = os.path.dirname(self.file_path)
        if not os.path.exists(cartella_data):
            os.makedirs(cartella_data, exist_ok=True)

        # Mantiene la struttura {"negozi": [...]} come richiesto dal tuo lettore originale
        output = {"negozi": dati}

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(output, file, indent=4, ensure_ascii=False)
        
    def modifica_negozio(self, codice_breve_target, nuovo_nome, nuovo_coordinatore, nuovo_codclifor, nuova_descrizione):
        """Cerca il negozio tramite il codice originale e ne aggiorna i campi."""
        # 1. Carica la lista attuale dei negozi (oggetti Negozio)
        negozi = self.leggi_tutti_negozi()
        trovato = False

        # 2. Cerca il record corrispondente usando la dot notation (oggetti)
        for n in negozi:
            if n.codice_breve == codice_breve_target:
                # Aggiorna gli attributi dell'oggetto
                n.nome = nuovo_nome
                n.coordinatore = nuovo_coordinatore  # <-- Corretto (o al posto della e)
                n.codclifor = nuovo_codclifor
                n.descrizione_conto = nuova_descrizione
                trovato = True
                break  # Record trovato e aggiornato, usciamo dal ciclo

        # 3. Se l'ha trovato, sovrascrive il file JSON con la lista aggiornata
        if trovato:
            self.scrivi_tutti_negozi(negozi)
            return True
        
        print(f"Negozio con codice {codice_breve_target} non trovato.")
        return False