import customtkinter as ctk
from datetime import datetime

class TaskView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.task_in_modifica_id = None # Tiene traccia se stiamo modificando una task esistente

        # Titolo della Sezione
        lbl_titolo = ctk.CTkLabel(self, text="📋 Registro Task & Interventi Conclusi", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titolo.pack(pady=(10, 20), anchor="w", padx=10)

        # --- FORM DI INSERIMENTO / MODIFICA ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="x", padx=10, pady=5)

        # Riga 1: Data, Operatore e Stato
        lbl_data = ctk.CTkLabel(self.form_frame, text="Data:")
        lbl_data.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_data = ctk.CTkEntry(self.form_frame, width=120)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        lbl_op = ctk.CTkLabel(self.form_frame, text="Operatore:")
        lbl_op.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_operatore = ctk.CTkEntry(self.form_frame, width=150, placeholder_text="Nome tecnico")
        self.entry_operatore.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        lbl_stato = ctk.CTkLabel(self.form_frame, text="Stato:")
        lbl_stato.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.combo_stato = ctk.CTkComboBox(self.form_frame, values=["Risolto", "Da finire / Incompleto", "In attesa feedback"], width=180)
        self.combo_stato.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        # Riga 2: Note
        lbl_note = ctk.CTkLabel(self.form_frame, text="Note / Dettagli Intervento:")
        lbl_note.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_note = ctk.CTkEntry(self.form_frame, placeholder_text="Descrivi cosa è stato fatto o cosa manca...")
        self.entry_note.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="ew")
        
        self.form_frame.grid_columnconfigure(3, weight=1)

        # Contenitore per i bottoni di azione sulla destra
        self.azioni_btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.azioni_btn_frame.grid(row=1, column=4, columnspan=2, padx=5, pady=5, sticky="e")

        # Bottone Annulla Modifica (Nascosto di default)
        self.btn_annulla = ctk.CTkButton(self.azioni_btn_frame, text="Annulla", fg_color="#7f8c8d", hover_color="#95a5a6", width=80, command=self._pulisci_form)

        # Bottone di Azione Principale
        self.btn_azione = ctk.CTkButton(self.azioni_btn_frame, text="Inserisci Task", fg_color="#2980b9", hover_color="#3498db", width=110, command=self._on_azione_click)
        self.btn_azione.pack(side="right", padx=2)

        # --- TABELLA VISUALIZZAZIONE ---
        header_table = ctk.CTkFrame(self, fg_color="#34495e", height=30)
        header_table.pack(fill="x", padx=10, pady=(15, 0))
        
        ctk.CTkLabel(header_table, text="Data", text_color="white", font=ctk.CTkFont(weight="bold"), width=100, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Operatore", text_color="white", font=ctk.CTkFont(weight="bold"), width=120, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Stato", text_color="white", font=ctk.CTkFont(weight="bold"), width=160, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Note / Dettagli", text_color="white", font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left", padx=10, fill="x", expand=True)

        self.scroll_table = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def imposta_controller(self, controller):
        self.controller = controller
        self.aggiorna_tabella()

    def _on_azione_click(self):
        data = self.entry_data.get().strip()
        op = self.entry_operatore.get().strip()
        stato = self.combo_stato.get()
        note = self.entry_note.get().strip()

        if not (data and op and note):
            return

        if self.controller:
            if self.task_in_modifica_id:
                # Siamo in modalità modifica: aggiorniamo la task esistente
                self.controller.aggiorna_task_esistente(self.task_in_modifica_id, data, op, stato, note)
            else:
                # Siamo in modalità inserimento standard
                self.controller.aggiungi_task(data, op, stato, note)
            
            self._pulisci_form()

    def _carica_task_in_form(self, task):
        """Prepara il form superiore per la modifica dei dati di una task selezionata."""
        self.task_in_modifica_id = task["id"]
        
        # Inserisce i dati nei campi widget
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, task["data"])
        
        self.entry_operatore.delete(0, "end")
        self.entry_operatore.insert(0, task["operatore"])
        
        self.combo_stato.set(task["stato"])
        
        self.entry_note.delete(0, "end")
        self.entry_note.insert(0, task["note"])

        # Trasforma la grafica in modalità Modifica
        self.btn_azione.configure(text="Salva Modifica", fg_color="#d35400", hover_color="#e67e22")
        self.btn_annulla.pack(side="left", padx=2)

    def _pulisci_form(self):
        """Resetta il form riportandolo allo stato di inserimento nuovo record."""
        self.task_in_modifica_id = None
        self.entry_note.delete(0, "end")
        self.entry_operatore.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.combo_stato.set("Risolto")
        
        # Ripristina i bottoni grafici originari
        self.btn_azione.configure(text="Inserisci Task", fg_color="#2980b9", hover_color="#3498db")
        self.btn_annulla.pack_forget()

    def aggiorna_tabella(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        if not self.controller:
            return

        tasks = self.controller.ottieni_tutte_task()
        for i, task in enumerate(reversed(tasks)):
            bg_riga = "#2c3e50" if i % 2 == 0 else "transparent"
            riga = ctk.CTkFrame(self.scroll_table, fg_color=bg_riga, height=35)
            riga.pack(fill="x", pady=1)
            riga.pack_propagate(False)

            colore_stato = "#2ecc71" if task["stato"] == "Risolto" else ("#e67e22" if "Da finire" in task["stato"] else "#f1c40f")

            ctk.CTkLabel(riga, text=task["data"], width=100, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(riga, text=task["operatore"], width=120, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(riga, text=task["stato"], text_color=colore_stato, width=160, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
            ctk.CTkLabel(riga, text=task["note"], anchor="w").pack(side="left", padx=10, fill="x", expand=True)
            
            # Pulsante Elimina (🗑️)
            btn_del = ctk.CTkButton(riga, text="🗑️", width=25, fg_color="transparent", hover_color="#c0392b", 
                                    command=lambda t_id=task["id"]: self.controller.elimina_task(t_id))
            btn_del.pack(side="right", padx=5)

            # Pulsante Modifica (✏️)
            btn_edit = ctk.CTkButton(riga, text="✏️", width=25, fg_color="transparent", hover_color="#d35400", 
                                     command=lambda t=task: self._carica_task_in_form(t))
            btn_edit.pack(side="right", padx=2)