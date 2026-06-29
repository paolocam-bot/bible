import os
import csv
import shutil  # Gestione della copia fisica del file
from datetime import datetime, timedelta
from collections import Counter

class TaskController:
    def __init__(self, model, view, main_controller):
        self.model = model
        self.view = view
        self.main_controller = main_controller

    def ottieni_nomi_negozi(self):
        if self.main_controller and hasattr(self.main_controller, "ottieni_nomi_negozi"):
            return self.main_controller.ottieni_nomi_negozi()
        return ["Nessun Negozio Registrato"]

    def ottieni_tutte_task(self):
        tasks = self.model.leggi_task()
        self.elabora_e_aggiorna_dashboard(tasks)
        return tasks

    def aggiungi_task(self, data, negozio, operatore, stato, note):
        tasks = self.model.leggi_task()
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
        self.model.salva_task(tasks)
        
        # --- OPERAZIONI DI ESPORTAZIONE E SICUREZZA ---
        self._esporta_task_in_csv_parallelo(tasks)
        self._esegui_backup_sicurezza()
        
        self.view.aggiorna_tabella()

    def aggiorna_task_esistente(self, task_id, data, negozio, operatore, stato, note):
        tasks = self.model.leggi_task()
        for task in tasks:
            if str(task.get("id")) == str(task_id):
                task["data"] = data
                task["negozio"] = negozio
                task["operatore"] = operatore
                task["stato"] = stato
                task["note"] = note
                break
                
        self.model.salva_task(tasks)
        
        # --- OPERAZIONI DI ESPORTAZIONE E SICUREZZA ---
        self._esporta_task_in_csv_parallelo(tasks)
        self._esegui_backup_sicurezza()
        
        self.view.aggiorna_tabella()

    def elimina_task(self, task_id):
        tasks = self.model.leggi_task()
        tasks = [t for t in tasks if str(t.get("id")) != str(task_id)]
        self.model.salva_task(tasks)
        
        # --- OPERAZIONI DI ESPORTAZIONE E SICUREZZA ---
        self._esporta_task_in_csv_parallelo(tasks)
        self._esegui_backup_sicurezza()
        
        self.view.aggiorna_tabella()

    # =====================================================================
    # GESTIONE BACKUP (SOLO LOCALE)
    # =====================================================================
    def _esegui_backup_sicurezza(self):
        """Genera una copia cronologica del file JSON esclusivamente nella memoria locale."""
        try:
            # 1. Recupero del percorso del file JSON di produzione
            percorso_originario_json = os.path.join(self.main_controller.view.cartella_progetto, "data", "registro_task.json")
            
            if not os.path.exists(percorso_originario_json):
                return
            
            # 2. Creazione della sottocartella locale 'data/backups' se non esiste
            cartella_backup_locale = os.path.join(self.main_controller.view.cartella_progetto, "data", "backups")
            os.makedirs(cartella_backup_locale, exist_ok=True)
            
            # 3. Generazione del file con la data odierna (es. backup_task_20260629.json)
            stringa_data = datetime.now().strftime("%Y%m%d")
            nome_file_backup = f"backup_task_{stringa_data}.json"
            percorso_backup_locale = os.path.join(cartella_backup_locale, nome_file_backup)
            
            # 4. Copia fisica locale dei dati
            shutil.copy2(percorso_originario_json, percorso_backup_locale)
            
        except Exception as e:
            print(f"❌ Errore durante l'esecuzione del backup locale: {e}")

    def elabora_e_aggiorna_dashboard(self, tasks):
        pendenti = 0
        completati_oggi = 0
        negozi_settimana = []
        
        oggi_str = datetime.now().strftime("%d/%m/%Y")
        limite_settimana = datetime.now() - timedelta(days=7)
        
        for task in tasks:
            stato = task.get("stato", "")
            data_str = task.get("data", "")
            if "Da finire" in stato or "In attesa" in stato:
                pendenti += 1
            if stato == "Risolto" and oggi_str in data_str:
                completati_oggi += 1
            if data_str:
                try:
                    data_pulita = data_str.split()[0]
                    data_obj = datetime.strptime(data_pulita, "%d/%m/%Y")
                    if data_obj >= limite_settimana and task.get("negozio"):
                        negozi_settimana.append(task.get("negozio"))
                except Exception:
                    pass

        if negozi_settimana:
            conteggio = Counter(negozi_settimana)
            negozio_top, ricorrenze = conteggio.most_common(1)[0]
            negozio_critico_testo = f"{negozio_top} ({ricorrenze} int)"
        else:
            negozio_critico_testo = "Nessuno"

        self.view.aggiorna_dashboard(pendenti, completati_oggi, negozio_critico_testo)

    def _esporta_task_in_csv_parallelo(self, tasks):
        """Genera il file CSV sul server condiviso (La logica originaria non è stata toccata)."""
        try:
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