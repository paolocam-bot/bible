import json
import os
from models.dao.manuale_dao import ManualeDAO
from models.problema import Problema

class ManualeModel:
    def __init__(self):
        self.dao = ManualeDAO() # Usa il default: database_manuale.json
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
        """Cerca corrispondenze nel titolo o nelle parole chiave del problema."""
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
        # Convertiamo gli oggetti Problema in dizionari dict prima di inviarli al DAO
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
        # Il modello non sa COME viene salvato il file, ci pensa il DAO
        self.dao.scrivi_tutti_problemi(dati_da_salvare)

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