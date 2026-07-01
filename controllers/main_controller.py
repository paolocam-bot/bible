import os
import json

# Import dei Modelli
from models.manuale_model import ManualeModel
from models.negozio_model import NegozioModel
from models.app_model import AppModel              
from models.brother_model import BrotherModel
from models.mt_model import MTModel
from models.task_model import TaskModel

# Import delle Viste
from views.manuale_view import ManualeView
from views.app_view import AppView                  
from views.negozio_view import NegozioView
from views.brother_view import BrotherView
from views.mt_view import MTView
from views.task_view import TaskView

# IMPORT DEI CONTROLLER NECESSARI
from controllers.negozio_controller import NegozioController
from controllers.base_knowledge_controller import BaseKnowledgeController
from controllers.task_controller import TaskController

class MainController:
    def __init__(self, view):
        self.view = view

        # =====================================================================
        # 1. INIZIALIZZAZIONE CON BASEKNOWLEDGECONTROLLER (Ex moduli storici)
        # =====================================================================
        self.model_zebra = ManualeModel()
        self.view_zebra = ManualeView(self.view.container_area)
        self.ctrl_zebra = BaseKnowledgeController(self.model_zebra, self.view_zebra, "Manuale Zebra")

        self.model_brother = BrotherModel()
        self.view_brother = BrotherView(self.view.container_area)
        self.ctrl_brother = BaseKnowledgeController(self.model_brother, self.view_brother, "Guasto Brother")

        self.model_app = AppModel()
        self.view_app = AppView(self.view.container_area)
        self.ctrl_app = BaseKnowledgeController(self.model_app, self.view_app, "Anomalia Applicazione")

        self.model_mt = MTModel()
        self.view_mt = MTView(self.view.container_area)
        self.ctrl_mt = BaseKnowledgeController(self.model_mt, self.view_mt, "Segnalazione MT")

        # =====================================================================
        # 2. INIZIALIZZAZIONE MODULI CORE & GESTIONALI
        # =====================================================================
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi, self)

        # Modulo Registro Task (Refactored con il suo Controller dedicato)
        self.model_task = TaskModel(self.view.cartella_progetto)
        self.view_task = TaskView(self.view.container_area)
        self.ctrl_task = TaskController(self.model_task, self.view_task, self)
        self.view_task.imposta_controller(self.ctrl_task)

        # =====================================================================
        # 3. COLLEGAMENTO COMANDI E NAVIGAZIONE
        # =====================================================================
        self.collega_bottoni_dinamici()
        self.view.imposta_controller_per_creazione(self)

        self.view.btn_registro_task.configure(command=lambda: self.view.mostra_sezione(self.view_task))
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
        """Reindirizza il click del bottone sul modulo corretto o ne crea uno dinamico."""
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
            nuovo_modello = ManualeModel()
            if hasattr(nuovo_modello, 'dao'):
                nuovo_modello.dao.file_path = os.path.join(self.view.cartella_progetto, "data", nome_db)
                if hasattr(nuovo_modello, 'carica_dati'):
                    nuovo_modello.carica_dati()

            nuova_vista = ManualeView(self.view.container_area)
            config_sezione = next((s for s in self.view.configurazione_sezioni if s["db"] == nome_db), None)
            titolo_popup = config_sezione["testo"].replace("📋 ", "").strip() if config_sezione else "Manuale Custom"
            
            BaseKnowledgeController(nuovo_modello, nuova_vista, titolo_popup)
            
            # 🛠️ RISOLTO: Sistemato il typo da nueva_vista a nuova_vista
            self.view.mostra_sezione(nuova_vista)

    def ottieni_nomi_negozi(self):
        """Mantenuto qui perché serve al TaskController per popolare la ComboBox dei negozi."""
        try:
            if hasattr(self.model_negozi, "carica_dati"):
                self.model_negozi.carica_dati()
            negozi_attuali = self.model_negozi.ottieni_tutti()
            nomi_unici = list(set([n.nome for n in negozi_attuali if n.nome]))
            return sorted(nomi_unici, key=str.lower)
        except Exception as e:
            print(f"Errore nel recupero nomi negozi ordinati: {e}")
        return ["Nessun Negozio Registrato"]

    # =====================================================================
    # 5. AGGIUNTA E RIMOZIONE CATEGORIE DINAMICHE
    # =====================================================================
    def aggiungi_nuova_categoria(self, nome_categoria, nome_file_json):
        id_nuovo = nome_categoria.lower().replace(" ", "_")
        nuova_sez = {
            "id": id_nuovo,
            "testo": f"📋 {nome_categoria}",
            "db": nome_file_json,
            "tipo": "manuale"
        }
        
        percorso_nuovo_db = os.path.join(self.view.cartella_progetto, "data", nome_file_json)
        if not os.path.exists(percorso_nuovo_db):
            try:
                with open(percorso_nuovo_db, "w", encoding="utf-8") as f:
                    json.dump([], f, indent=4)
            except Exception as e:
                print(f"Errore nella scrittura fisica del file JSON: {e}")

        self.view.configurazione_sezioni.append(nuova_sez)
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()
        
        # 🚀 AUTO-APERTURA ISTANTANEA: Apre la nuova sezione appena viene creata
        self.apri_sezione_dinamica(nome_file_json, "manuale")

    def rimuovi_categoria(self, id_categoria):
        self.view.configurazione_sezioni = [s for s in self.view.configurazione_sezioni if s["id"] != id_categoria]
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()