import os
from models.dao.manuale_dao import ManualeDAO
from models.problema import Problema

class ManualeBaseModel:
    def __init__(self, nome_file_json=None):
        """
        Modello generico per la gestione dei manuali di assistenza.
        Se nome_file_json è None, il ManualeDAO userà il suo file di default (database_manuale.json).
        """
        if nome_file_json:
            # Calcoliamo il percorso assoluto all'interno della cartella 'data'
            # (Adattando la logica già presente nei modelli specifici)
            cartella_progetto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            percorso_specifico = os.path.join(cartella_progetto, "data", nome_file_json)
            self.dao = ManualeDAO(file_path=percorso_specifico)
        else:
            self.dao = ManualeDAO() # Usa il default del DAO
            
        self.problemi = []
        self.carica_dati()

    def carica_dati(self):
        """Carica i dati grezzi dal DAO e istanzia gli oggetti Problema."""
        dati_grezzi = self.dao.leggi_tutti_problemi()
        self.problemi = [
            Problema(
                p["id"],
                p["titolo"],
                p["parole_chiave"],
                p["descrizione"],
                p["soluzioni"]
            )
            for p in dati_grezzi
        ]

    def ottieni_tutti(self):
        """Restituisce tutti i problemi in memoria."""
        return self.problemi

    def cerca_problema(self, query):
        """Cerca corrispondenze nel titolo o nelle parole chiave (case-insensitive)."""
        query = query.lower().strip()
        if not query:
            return None

        for prob in self.problemi:
            if query in prob.titolo.lower():
                return prob
            for kw in prob.parole_chiave:
                if query in kw.lower():
                    return prob
        return None
    
    def salva_dati(self):
        """Delega al DAO il salvataggio dello stato corrente."""
        dati_da_salvare = [
            {
                "id": p.id,
                "titolo": p.titolo,
                "parole_chiave": p.parole_chiave,
                "descrizione": p.descrizione,
                "soluzioni": p.soluzioni
            }
            for p in self.problemi
        ]
        self.dao.scrivi_tutti_problemi(dati_da_salvare)

    def aggiungi_problema(self, problema):
        """Aggiunge un problema e salva su file."""
        self.problemi.append(problema)
        self.salva_dati()

    def aggiungere_problema(self, problema):
        """Alias per retrocompatibilità con alcuni controller (es. Brother/App)."""
        self.aggiungi_problema(problema)

    def elimina_problema(self, id_problema):
        """Rimuove un problema tramite ID e salva su file."""
        self.problemi = [p for p in self.problemi if p.id != id_problema]
        self.salva_dati() 

    def modifica_problema(self, id_problema, dati_aggiornati):
        """Aggiorna i dati di un problema esistente e salva su file."""
        for prob in self.problemi:
            if prob.id == id_problema:
                prob.titolo = dati_aggiornati["titolo"]
                prob.parole_chiave = dati_aggiornati["parole_chiave"]
                prob.descrizione = dati_aggiornati["descrizione"]
                prob.soluzioni = dati_aggiornati["soluzioni"]
                break
        self.salva_dati()