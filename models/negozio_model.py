from models.dao.negozio_dao import NegozioDAO
from models.negozio import Negozio

class NegozioModel:
    def __init__(self):
        self.dao = NegozioDAO()
        self.negozi = []
        self.carica_dati()

    def carica_dati(self):
        dati_grezzi = self.dao.leggi_tutti_negozi()
        self.negozi = [
            Negozio(
                n["codice_breve"],
                n["nome"],
                n["coordinatore"],
                n["codclifor"],
                n["descrizione_conto"]
            )
            for n in dati_grezzi
        ]

    def ottieni_tutti(self):
        return self.negozi

    def cerca_negozi(self, query):
        """Cerca corrispondenze sia nel nome del negozio che nel nome del coordinatore."""
        query = query.lower().strip()
        if not query:
            return self.negozi

        risultati = []
        for n in self.negozi:
            # Verifica se la query è inclusa nel nome del negozio o nel coordinatore
            if query in n.nome.lower() or query in n.coordinatore.lower():
                risultati.append(n)
        return risultati