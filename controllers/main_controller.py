from models.manuale_model import ManualeModel
from models.negozio_model import NegozioModel
from models.app_model import AppModel              
from views.manuale_view import ManualeView
from views.app_view import AppView                  
from controllers.manuale_controller import ManualeController
from controllers.negozio_controller import NegozioController
from controllers.app_controller import AppController 
from models.brother_model import BrotherModel
from views.brother_view import BrotherView
from controllers.brother_controller import BrotherController

# IMPORT ESATTO (Tutti i nomi delle classi ora coincidono al 100% con i loro file)
from views.negozio_view import NegozioView

# Import dei moduli MT
from models.mt_model import MTModel
from views.mt_view import MTView
from controllers.mt_controller import MTController

# Import del nuovo modulo registro task
from models.task_model import TaskModel
from views.task_view import TaskView

import os
import json
import uuid

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

        # Modulo Negozi
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi)

        # Modulo MT
        self.model_mt = MTModel()
        self.view_mt = MTView(self.view.container_area)
        self.ctrl_mt = MTController(self.model_mt, self.view_mt)

        # INIZIALIZZAZIONE DEL NUOVO REGISTRO TASK FISSO
        self.model_task = TaskModel(self.view.cartella_progetto)
        self.view_task = TaskView(self.view.container_area)
        self.view_task.imposta_controller(self)

        # =====================================================================
        # 2. COLLEGAMENTO COMANDI E PULSANTE GESTIONE
        # =====================================================================
        self.collega_bottoni_dinamici()
        self.view.imposta_controller_per_creazione(self)

        # Aggancia l'evento click al bottone fisso Registro Task
        self.view.btn_registro_task.configure(command=lambda: self.view.mostra_sezione(self.view_task))

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
            nuovo_modello = ManualeModel()
            if hasattr(nuovo_modello, 'dao'):
                nuovo_modello.dao.file_path = os.path.join(self.view.cartella_progetto, "data", nome_db)
                if hasattr(nuovo_modello, 'carica_dati'):
                    nuovo_modello.carica_dati()

            nuova_vista = ManualeView(self.view.container_area)
            ManualeController(nuovo_modello, nuova_vista)
            self.view.mostra_sezione(nuova_vista)

    # =====================================================================
    # 3. METODI LOGICI PER LA GESTIONE DELLE TASK REGISTRATE
    # =====================================================================
    def ottieni_tutte_task(self):
        return self.model_task.leggi_task()

    def aggiungi_task(self, data, operatore, stato, note):
        tasks = self.model_task.leggi_task()
        nuova_task = {
            "id": str(uuid.uuid4())[:8], # Genera un ID compatto univoco
            "data": data,
            "operatore": operatore,
            "stato": stato,
            "note": note
        }
        tasks.append(nuova_task)
        self.model_task.salva_task(tasks)
        self.view_task.aggiorna_tabella()

    def elimina_task(self, task_id):
        tasks = self.model_task.leggi_task()
        tasks = [t for t in tasks if t["id"] != task_id]
        self.model_task.salva_task(tasks)
        self.view_task.aggiorna_tabella()

    # =====================================================================
    # 4. AGGIUNTA E RIMOZIONE CATEGORIE DINAMICHE
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

    def rimuovi_categoria(self, id_categoria):
        self.view.configurazione_sezioni = [s for s in self.view.configurazione_sezioni if s["id"] != id_categoria]
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()

    def aggiorna_task_esistente(self, task_id, data, operatore, stato, note):
        """Trova la task tramite ID e aggiorna i suoi dati salvandoli nel file JSON."""
        tasks = self.model_task.leggi_task()
        
        for task in tasks:
            # Forziamo entrambi gli ID a stringa per evitare bug se il vecchio ID era un numero
            if str(task["id"]) == str(task_id):
                task["data"] = data
                task["operatore"] = operatore
                task["stato"] = stato
                task["note"] = note
                break
                
        self.model_task.salva_task(tasks)
        self.view_task.aggiorna_tabella() # Rinfresca lo schermo con i dati nuovi