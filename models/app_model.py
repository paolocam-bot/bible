import os
from models.dao.manuale_dao import ManualeDAO
from models.problema import Problema

class AppModel:
    def __init__(self):
        # Calcoliamo il percorso specifico per i problemi dell'app
        cartella_progetto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        percorso_app_json = os.path.join(cartella_progetto, "data", "problemi_app.json")
        
        # Inizializziamo il DAO dicendogli di puntare a problemi_app.json
        self.dao = ManualeDAO(percorso_app_json)
        self.problemi = []
        self.carica_dati()

    def carica_dati(self):
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
        return self.problemi

    def cerca_problema(self, query):
        """Cerca corrispondenze nel titolo o nelle parole chiave del problema dell'app."""
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
        """Delega al DAO il salvataggio dei dati correnti in memoria."""
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

    def aggiungere_problema(self, problema): # chiamato anche aggiungi_problema a seconda del controller
        self.problemi.append(problema)
        self.salva_dati()

    def aggiungi_problema(self, problema):
        self.problemi.append(problema)
        self.salva_dati()

    def elimina_problema(self, id_problema):
        self.problemi = [p for p in self.problemi if p.id != id_problema]
        self.salva_dati() 

    def modifica_problema(self, id_problema, dati_aggiornati):
        """Trova il problema tramite ID e aggiorna i suoi attributi."""
        for prob in self.problemi:
            if prob.id == id_problema:
                prob.titolo = dati_aggiornati["titolo"]
                prob.parole_chiave = dati_aggiornati["parole_chiave"]
                prob.descrizione = dati_aggiornati["descrizione"]
                prob.soluzioni = dati_aggiornati["soluzioni"]
                break
        self.salva_dati()