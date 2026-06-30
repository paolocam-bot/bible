import os
import json
from models.dao.negozio_dao import NegozioDAO
from models.negozio import Negozio

class NegozioModel:
    def __init__(self):
        self.dao = NegozioDAO()
        self.negozi = []
        self.carica_dati()

    def carica_dati(self):
        """Carica i dati dal DAO e li ordina immediatamente in ordine alfabetico per nome."""
        dati_grezzi = self.dao.leggi_tutti_negozi()
        
        # Generiamo la lista di oggetti Negozio
        istanze_negozi = [
            Negozio(
                n["codice_breve"],
                n["nome"],
                n["coordinatore"],
                n["codclifor"],
                n["descrizione_conto"]
            )
            for n in dati_grezzi if n.get("nome")
        ]
        
        # ORDINE ALFABETICO REALE DI TUTTI GLI OGGETTI (A -> Z per il campo nome)
        self.negozi = sorted(istanze_negozi, key=lambda x: x.nome.lower())

    def ottieni_tutti(self):
        """Restituisce la lista, assicurandosi che mantenga l'ordine alfabetico."""
        if not self.negozi:
            self.carica_dati()
        return sorted(self.negozi, key=lambda x: x.nome.lower())

    def cerca_negozi(self, query):
        """Cerca corrispondenze sia nel nome del negozio che nel nome del coordinatore."""
        query = query.lower().strip()
        if not query:
            return self.negozi

        risultati = []
        for n in self.negozi:
            if query in n.nome.lower() or query in n.coordinatore.lower():
                risultati.append(n)
        return risultati

    def _salva_su_file(self):
        """Metodo interno per convertire la lista di oggetti in dizionari e salvarli tramite DAO."""
        dati_da_salvare = [
            {
                "codice_breve": n.codice_breve,
                "nome": n.nome,
                "coordinatore": n.coordinatore,
                "codclifor": n.codclifor,
                "descrizione_conto": n.descrizione_conto
            }
            # Salviamo mantenendo l'ordine alfabetico corrente
            for n in sorted(self.negozi, key=lambda x: x.nome.lower())
        ]
        
        try:
            # Mappiamo sul tuo metodo reale del DAO visto in precedenza
            if hasattr(self.dao, "scrivi_tutti_negozi"):
                self.dao.scrivi_tutti_negozi(dati_da_salvare)
            elif hasattr(self.dao, "salva_tutti_negozi"):
                self.dao.salva_tutti_negozi(dati_da_salvare)
            else:
                percorso = getattr(self.dao, "file_path", "data/database_negozi.json")
                os.makedirs(os.path.dirname(percorso), exist_ok=True)
                with open(percorso, "w", encoding="utf-8") as f:
                    json.dump({"negozi": dati_da_salvare}, f, indent=4, ensure_ascii=False)
                print("⚠️ Salvataggio eseguito in modalità fallback diretta sul file JSON.")
        except Exception as e:
            print(f"❌ Errore critico durante il salvataggio dei negozi: {e}")

    def aggiungi_negozio(self, codice_breve, nome, coordinatore, codclifor, descrizione_conto):
        """Aggiunge un nuovo negozio e aggiorna il database."""
        nuovo = Negozio(codice_breve, nome, coordinatore, codclifor, descrizione_conto)
        self.negozi.append(nuovo)
        self._salva_su_file()

    def modifica_negozio(self, codice_breve_target, nuovo_nome, nuovo_coordinatore, nuovo_codclifor, nuova_descrizione):
        """Trova il negozio tramite il codice_breve (chiave) e ne aggiorna i valori."""
        for n in self.negozi:
            if n.codice_breve == codice_breve_target:
                n.nome = nuovo_nome
                n.coordinatore = nuovo_coordinatore  # 🛠️ CORRETTO QUI: era nuevo_coordinatore
                n.codclifor = nuovo_codclifor
                n.descrizione_conto = nuova_descrizione
                break
        
        # Riordina immediatamente la lista locale per riflettere i cambi di nome in tabella
        self.negozi = sorted(self.negozi, key=lambda x: x.nome.lower())
        self._salva_su_file()