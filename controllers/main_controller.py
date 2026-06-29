import os
import json
import csv

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

class MainController:
    def __init__(self, view):
        self.view = view

        # =====================================================================
        # 1. INIZIALIZZAZIONE CON BASEKNOWLEDGECONTROLLER (Ex moduli storici)
        # =====================================================================
        
        # Modulo Zebra (Usa il manuale di default)
        self.model_zebra = ManualeModel()
        self.view_zebra = ManualeView(self.view.container_area)
        self.ctrl_zebra = BaseKnowledgeController(self.model_zebra, self.view_zebra, "Manuale Zebra")

        # Modulo Brother
        self.model_brother = BrotherModel()
        self.view_brother = BrotherView(self.view.container_area)
        self.ctrl_brother = BaseKnowledgeController(self.model_brother, self.view_brother, "Guasto Brother")

        # Modulo Problemi App
        self.model_app = AppModel()
        self.view_app = AppView(self.view.container_area)
        self.ctrl_app = BaseKnowledgeController(self.model_app, self.view_app, "Anomalia Applicazione")

        # Modulo MT
        self.model_mt = MTModel()
        self.view_mt = MTView(self.view.container_area)
        self.ctrl_mt = BaseKnowledgeController(self.model_mt, self.view_mt, "Segnalazione MT")

        # =====================================================================
        # 2. INIZIALIZZAZIONE MODULI CORE & GESTIONALI
        # =====================================================================
        
        # Modulo Negozi (Abilitata comunicazione tramite self)
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi, self)

        # Modulo Registro Task Fisso
        self.model_task = TaskModel(self.view.cartella_progetto)
        self.view_task = TaskView(self.view.container_area)
        self.view_task.imposta_controller(self)

        # =====================================================================
        # 3. COLLEGAMENTO COMANDI E NAVIGAZIONE
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
            # Creazione a runtime del modulo personalizzato tramite BaseKnowledgeController
            nuovo_modello = ManualeModel()
            if hasattr(nuovo_modello, 'dao'):
                nuovo_modello.dao.file_path = os.path.join(self.view.cartella_progetto, "data", nome_db)
                if hasattr(nuovo_modello, 'carica_dati'):
                    nuovo_modello.carica_dati()

            nuova_vista = ManualeView(self.view.container_area)
            
            # Recupera dinamicamente il nome pulito della sezione per i popup del controller
            config_sezione = next((s for s in self.view.configurazione_sezioni if s["db"] == nome_db), None)
            titolo_popup = config_sezione["testo"].replace("📋 ", "").strip() if config_sezione else "Manuale Custom"
            
            # Inizializza il BaseKnowledgeController unico!
            BaseKnowledgeController(nuovo_modello, nuova_vista, titolo_popup)
            self.view.mostra_sezione(nuova_vista)

    # =====================================================================
    # 4. METODI LOGICI PER LA GESTIONE DELLE TASK REGISTRATE + ESPORTAZIONE CSV
    # =====================================================================
    def _esporta_task_in_csv_parallelo(self, tasks):
        """Genera in parallelo un file CSV salvandolo sul server condiviso."""
        try:
            # Percorso UNC di rete Windows mantenuto intatto
            percorso_csv = r"\\SrvDati\Dati-P\Computer Paolo\registro_task.csv"
            os.makedirs(os.path.dirname(percorso_csv), exist_ok=True)
            
            colonne = ["id", "data", "negozio", "operatore", "stato", "note"]
            
            with open(percorso_csv, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=colonne, delimiter=";")
                writer.writeheader()
                for task in tasks:
                    task_pulita = task.copy()
                    if task_pulita.get("note"):
                        task_pulita["note"] = task_pulita["note"].replace("\n", " ").replace("\r", "")
                    writer.writerow(task_pulita)
        except Exception as e:
            print(f"❌ Errore durante la generazione del CSV sul server condiviso: {e}")

    def ottieni_nomi_negozi(self):
        """Recupera la lista dei nomi dei negozi e garantisce l'ordinamento A-Z."""
        try:
            if hasattr(self.model_negozi, "carica_dati"):
                self.model_negozi.carica_dati()
            negozi_attuali = self.model_negozi.ottieni_tutti()
            nomi_unici = list(set([n.nome for n in negozi_attuali if n.nome]))
            return sorted(nomi_unici, key=str.lower)
        except Exception as e:
            print(f"Errore nel recupero nomi negozi ordinati: {e}")
        return ["Nessun Negozio Registrato"]

    def ottieni_tutte_task(self):
        return self.model_task.leggi_task()

    def aggiungi_task(self, data, negozio, operatore, stato, note):
        tasks = self.model_task.leggi_task()
        nuovo_id = max([int(t.get("id", 0)) for t in tasks if str(t.get("id", "")).isdigit()], default=0) + 1
        
        nuova_task = {
            "id": nuovo_id,
            "data": data,
            "negozio": negozio,
            "operatore": operatore,
            "stato": stato,
            "note": note
        }
        tasks.append(nuova_task)
        self.model_task.salva_task(tasks)
        self._esporta_task_in_csv_parallelo(tasks)
        self.view_task.aggiorna_tabella()

    def aggiorna_task_esistente(self, task_id, data, negozio, operatore, stato, note):
        tasks = self.model_task.leggi_task()
        for task in tasks:
            if str(task.get("id")) == str(task_id):
                task["data"] = data
                task["negozio"] = negozio
                task["operatore"] = operatore
                task["stato"] = stato
                task["note"] = note
                break
                
        self.model_task.salva_task(tasks)
        self._esporta_task_in_csv_parallelo(tasks)
        self.view_task.aggiorna_tabella()

    def elimina_task(self, task_id):
        tasks = self.model_task.leggi_task()
        tasks = [t for t in tasks if str(t.get("id")) != str(task_id)]
        self.model_task.salva_task(tasks)
        self._esporta_task_in_csv_parallelo(tasks)
        self.view_task.aggiorna_tabella()

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

    def rimuovi_categoria(self, id_categoria):
        self.view.configurazione_sezioni = [s for s in self.view.configurazione_sezioni if s["id"] != id_categoria]
        self.view.salva_configurazione()
        self.view.aggiorna_sidebar_grafica()
        self.collega_bottoni_dinamici()