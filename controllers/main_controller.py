from models.manuale_model import ManualeModel
from models.negozio_model import NegozioModel
from models.app_model import AppModel              
from views.manuale_view import ManualeView
from views.negozio_view import NegozioView
from views.app_view import AppView                  
from controllers.manuale_controller import ManualeController
from controllers.negozio_controller import NegozioController
from controllers.app_controller import AppController 
from models.brother_model import BrotherModel
from views.brother_view import BrotherView
from controllers.brother_controller import BrotherController

# Import dei moduli MT
from models.mt_model import MTModel
from views.mt_view import MTView
from controllers.mt_controller import MTController

# Per poter generare i file JSON vuoti al volo
import os
import json

class MainController:
    def __init__(self, view):
        self.view = view

        # =====================================================================
        # 1. INIZIALIZZAZIONE STATICA DEI MODULI STORICI
        # =====================================================================
        
        # Modulo Zebra
        self.model_zebra = ManualeModel()
        self.view_zebra = ManualeView(self.view.container_area)
        self.ctrl_zebra = ManualeController(self.model_zebra, self.view_zebra)

        # Modulo Brother
        self.model_brother = BrotherModel()
        self.view_brother = BrotherView(self.view.container_area)
        self.ctrl_brother = BrotherController(self.model_brother, self.view_brother)

        # Modulo Problemi App
        self.model_app = AppModel()
        self.view_app = AppView(self.view.container_area)
        self.ctrl_app = AppController(self.model_app, self.view_app)

        # Modulo Negozi (CORRETTO: Passato solo il container!)
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi)

        # Modulo MT
        self.model_mt = MTModel()
        self.view_mt = MTView(self.view.container_area)
        self.ctrl_mt = MTController(self.model_mt, self.view_mt)

        # =====================================================================
        # 2. COLLEGAMENTO COMANDI E PULSANTE GESTIONE
        # =====================================================================
        self.collega_bottoni_dinamici()
        self.view.imposta_controller_per_creazione(self)

        # Mostra la schermata iniziale all'avvio
        self.view.mostra_sezione(self.view_zebra)

    def collega_bottoni_dinamici(self):
        """Associa a ogni bottone della barra laterale la sua vista o azione."""
        for sezione in self.view.configurazione_sezioni:
            id_sez = sezione["id"]
            nome_db = sezione["db"]
            tipo_sez = sezione.get("tipo", "manuale")
            
            btn = self.view.bottoni_sidebar.get(id_sez)
            if btn:
                btn.configure(command=lambda db=nome_db, t=tipo_sez: self.apri_sezione_dinamica(db, t))

    def apri_sezione_dinamica(self, nome_db, tipo_sezione):
        """Reindirizza il click del bottone sul rispettivo modulo storico o dinamico."""
        if nome_db == "database_manuale.json":
            self.view.mostra_sezione(self.view_zebra)
        elif nome_db == "database_brother.json":
            self.view.mostra_sezione(self.view_brother)
        elif nome_db == "problemi_app.json":
            self.view.mostra_sezione(self.view_app)
        elif nome_db == "database_mt.json":
            self.view.mostra_sezione(self.view_mt)
        elif nome_db == "database_negozi.json":
            self.view.mostra_sezione(self.view_negozi)
        else:
            # SOLUZIONE PER I MODULI DINAMICI:
            # Creiamo un modello standard (punta a database_manuale.json di default)
            nuovo_modello = ManualeModel()
            
            # Sostituiamo il database aggirando l'init rigido se il tuo DAO espone il file_path
            # Altrimenti, se anche il DAO è fisso, usiamo il trucco di riassegnare il file al volo:
            if hasattr(nuovo_modello, 'dao'):
                nuovo_modello.dao.file_path = os.path.join(self.view.cartella_progetto, "data", nome_db)
                if hasattr(nuovo_modello, 'carica_dati'):
                    nuovo_modello.carica_dati() # Ricarica i dati dal file corretto

            nuova_vista = ManualeView(self.view.container_area)
            ManualeController(nuovo_modello, nuova_vista)
            
            # Ora la View può cambiare schermata senza eccezioni!
            self.view.mostra_sezione(nuova_vista)

    def aggiungi_nuova_categoria(self, nome_categoria, nome_file_json):
        """Crea in modo autonomo il file JSON vuoto su disco e aggiorna l'interfaccia."""
        id_nuovo = nome_categoria.lower().replace(" ", "_")
        nuova_sez = {
            "id": id_nuovo,
            "testo": f"📋 {nome_categoria}",
            "db": nome_file_json,
            "tipo": "manuale"
        }
        
        # RISOLTO: Creiamo fisicamente il file .json in modo nativo, evitando di chiamare ManualeModel
        percorso_nuovo_db = os.path.join(self.view.cartella_progetto, "data", nome_file_json)
        if not os.path.exists(percorso_nuovo_db):
            try:
                with open(percorso_nuovo_db, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4) # Scrive una lista vuota [] su disco
            except Exception as e:
                print(f"Errore nella scrittura fisica del file JSON: {e}")

        # Aggiorna l'interfaccia grafica
        self.view.configurazione_sezioni.append(nuova_sez)
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()

    def rimuovi_categoria(self, id_categoria):
        """Rimuove una categoria dalla configurazione e aggiorna la UI."""
        self.view.configurazione_sezioni = [s for s in self.view.configurazione_sezioni if s["id"] != id_categoria]
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()