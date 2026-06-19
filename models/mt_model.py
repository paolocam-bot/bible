from models.dao.manuale_dao import ManualeDAO
from models.problema import Problema

class MTModel:
    def __init__(self):
        # Forza il DAO a usare il file specifico per l'applicazione MT
        import os
        cartella_progetto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        file_specifico = os.path.join(cartella_progetto, "data", "database_mt.json")
        
        self.dao = ManualeDAO(file_path=file_specifico)
        self.problemi = []
        self.carica_dati()

    def carica_dati(self):
        dati_grezzi = self.dao.leggi_tutti_problemi()
        self.problemi = [
            # Usiamo il passaggio posizionale per evitare il TypeError riscontrato prima
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
        self.problemi.append(problema)
        self.salva_dati()

    def elimina_problema(self, id_problema):
        self.problemi = [p for p in self.problemi if p.id != id_problema]
        self.salva_dati() 

    def modifica_problema(self, id_problema, dati_aggiornati):
        for prob in self.problemi:
            if prob.id == id_problema:
                prob.titolo = dati_aggiornati["titolo"]
                prob.parole_chiave = dati_aggiornati["parole_chiave"]
                prob.descrizione = dati_aggiornati["descrizione"]
                prob.soluzioni = dati_aggiornati["soluzioni"]
                break
        self.salva_dati()