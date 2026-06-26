import customtkinter as ctk
from datetime import datetime

class TaskView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.task_in_modifica_id = None 

        # Titolo della Sezione
        lbl_titolo = ctk.CTkLabel(self, text="📋 Registro Task & Interventi Conclusi", font=ctk.CTkFont(size=20, weight="bold"))
        lbl_titolo.pack(pady=(10, 15), anchor="w", padx=10)

        # --- FORM DI INSERIMENTO / MODIFICA ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.pack(fill="x", padx=10, pady=5)

        # Configurazione colonne griglia del Form
        self.form_frame.grid_columnconfigure(1, weight=1)
        self.form_frame.grid_columnconfigure(3, weight=1)
        self.form_frame.grid_columnconfigure(5, weight=1)
        self.form_frame.grid_columnconfigure(7, weight=1)

        # Riga 0: Data, Negozio, Operatore e Stato
        lbl_data = ctk.CTkLabel(self.form_frame, text="Data:")
        lbl_data.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_data = ctk.CTkEntry(self.form_frame, width=110)
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        lbl_negozio = ctk.CTkLabel(self.form_frame, text="Negozio:")
        lbl_negozio.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.combo_negozio = ctk.CTkComboBox(self.form_frame, values=["Nessun Negozio"], width=180)
        self.combo_negozio.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        lbl_op = ctk.CTkLabel(self.form_frame, text="Operatore:")
        lbl_op.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.entry_operatore = ctk.CTkEntry(self.form_frame, width=130, placeholder_text="Nome tecnico")
        self.entry_operatore.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        lbl_stato = ctk.CTkLabel(self.form_frame, text="Stato:")
        lbl_stato.grid(row=0, column=6, padx=5, pady=5, sticky="w")
        self.combo_stato = ctk.CTkComboBox(self.form_frame, values=["Risolto", "Da finire / Incompleto", "In attesa feedback"], width=160)
        self.combo_stato.grid(row=0, column=7, padx=5, pady=5, sticky="ew")

        # Riga 1 & 2: Campo Note ampio (Cambiamo in CTkTextbox per avere più righe)
        lbl_note = ctk.CTkLabel(self.form_frame, text="Note / Dettagli:")
        lbl_note.grid(row=1, column=0, padx=5, pady=(5, 0), sticky="nw")
        
        # CTkTextbox gestisce nativamente il testo esteso su più righe
        self.entry_note = ctk.CTkTextbox(self.form_frame, height=65, activate_scrollbars=True)
        self.entry_note.grid(row=1, column=1, columnspan=7, padx=5, pady=5, sticky="ew")

        # Riga 3: Contenitore Pulsanti di Azione (Allineati a destra in basso)
        self.azioni_btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.azioni_btn_frame.grid(row=2, column=1, columnspan=7, padx=5, pady=(0, 5), sticky="e")

        self.btn_annulla = ctk.CTkButton(self.azioni_btn_frame, text="Annulla", fg_color="#7f8c8d", hover_color="#95a5a6", width=70, command=self._pulisci_form)
        self.btn_azione = ctk.CTkButton(self.azioni_btn_frame, text="Inserisci Task", fg_color="#2980b9", hover_color="#3498db", width=110, command=self._on_azione_click)
        self.btn_azione.pack(side="right", padx=2)

        # --- BARRA DI RICERCA TASK ---
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=10, pady=(10, 0))
        
        lbl_cerca = ctk.CTkLabel(self.search_frame, text="🔍 Filtra Task:", font=ctk.CTkFont(weight="bold"))
        lbl_cerca.pack(side="left", padx=(0, 10))
        
        self.entry_ricerca = ctk.CTkEntry(self.search_frame, placeholder_text="Digita una data (gg/mm/aaaa) o il nome di un negozio per filtrare...", width=400)
        self.entry_ricerca.pack(side="left", fill="x", expand=True)
        self.entry_ricerca.bind("<KeyRelease>", lambda event: self.aggiorna_tabella())

        # --- TABELLA VISUALIZZAZIONE ---
        header_table = ctk.CTkFrame(self, fg_color="#34495e", height=30)
        header_table.pack(fill="x", padx=10, pady=(10, 0))
        
        ctk.CTkLabel(header_table, text="Data", text_color="white", font=ctk.CTkFont(weight="bold"), width=90, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Negozio", text_color="white", font=ctk.CTkFont(weight="bold"), width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Operatore", text_color="white", font=ctk.CTkFont(weight="bold"), width=110, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Stato", text_color="white", font=ctk.CTkFont(weight="bold"), width=150, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(header_table, text="Note / Dettagli", text_color="white", font=ctk.CTkFont(weight="bold"), anchor="w").pack(side="left", padx=10, fill="x", expand=True)

        self.scroll_table = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def imposta_controller(self, controller):
        self.controller = controller
        self.aggiorna_opzioni_negozi()
        self.aggiorna_tabella()

    def _on_azione_click(self):
        data = self.entry_data.get().strip()
        negozio = self.combo_negozio.get()
        op = self.entry_operatore.get().strip()
        stato = self.combo_stato.get()
        # Per la Textbox serve estrarre il testo partendo da riga 1, carattere 0 fino alla fine
        note = self.entry_note.get("1.0", "end").strip()

        if not (data and op and note):
            return

        if self.controller:
            if self.task_in_modifica_id:
                self.controller.aggiorna_task_esistente(self.task_in_modifica_id, data, negozio, op, stato, note)
            else:
                self.controller.aggiungi_task(data, negozio, op, stato, note)
            
            self._pulisci_form()

    def _carica_task_in_form(self, task):
        self.task_in_modifica_id = task["id"]
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, task["data"])
        
        if task.get("negozio") in self.combo_negozio.cget("values"):
            self.combo_negozio.set(task["negozio"])
        
        self.entry_operatore.delete(0, "end")
        self.entry_operatore.insert(0, task["operatore"])
        self.combo_stato.set(task["stato"])
        
        # Pulizia e inserimento corretti per la Textbox
        self.entry_note.delete("1.0", "end")
        self.entry_note.insert("1.0", task["note"])

        self.btn_azione.configure(text="Salva Modifica", fg_color="#d35400", hover_color="#e67e22")
        self.btn_annulla.pack(side="left", padx=2)

    def _pulisci_form(self):
        self.task_in_modifica_id = None
        self.entry_note.delete("1.0", "end")
        self.entry_operatore.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.combo_stato.set("Risolto")
        if self.combo_negozio.cget("values"):
            self.combo_negozio.set(self.combo_negozio.cget("values")[0])
        
        self.btn_azione.configure(text="Inserisci Task", fg_color="#2980b9", hover_color="#3498db")
        self.btn_annulla.pack_forget()

    def aggiorna_tabella(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        if not self.controller:
            return

        testo_ricerca = self.entry_ricerca.get().strip().lower()
        tasks = self.controller.ottieni_tutte_task()
        
        i = 0
        for task in reversed(tasks):
            negozio_task = task.get("negozio", "").lower()
            data_task = task.get("data", "").lower()
            
            if testo_ricerca and (testo_ricerca not in negozio_task and testo_ricerca not in data_task):
                continue

            bg_riga = "#2c3e50" if i % 2 == 0 else "transparent"
            
            # Usiamo un layout a griglia (grid) sulla riga invece del pack, così i pulsanti rimangono ancorati a destra
            riga = ctk.CTkFrame(self.scroll_table, fg_color=bg_riga, height=40)
            riga.pack(fill="x", pady=2, padx=5)
            riga.grid_columnconfigure(4, weight=1) # La colonna delle note si espande, le altre sono fisse

            colore_stato = "#2ecc71" if task["stato"] == "Risolto" else ("#e67e22" if "Da finire" in task["stato"] else "#f1c40f")

            # Colonne allineate con larghezze stabili
            ctk.CTkLabel(riga, text=task["data"], width=85, anchor="w").grid(row=0, column=0, padx=5, sticky="w")
            ctk.CTkLabel(riga, text=task.get("negozio", "N/D"), width=130, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, padx=5, sticky="w")
            ctk.CTkLabel(riga, text=task["operatore"], width=100, anchor="w").grid(row=0, column=2, padx=5, sticky="w")
            ctk.CTkLabel(riga, text=task["stato"], text_color=colore_stato, width=130, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=0, column=3, padx=5, sticky="w")
            
            # Note troncate visivamente se troppo lunghe per non spingere i bottoni fuori dallo schermo
            lbl_nota_testo = task["note"].replace("\n", " ")
            if len(lbl_nota_testo) > 60:
                lbl_nota_testo = lbl_nota_testo[:57] + "..."
                
            ctk.CTkLabel(riga, text=lbl_nota_testo, anchor="w", justify="left").grid(row=0, column=4, padx=5, sticky="ew")
            
            # Contenitore pulsanti ancorato rigidamente a destra (Colonna 5)
            btn_frame = ctk.CTkFrame(riga, fg_color="transparent")
            btn_frame.grid(row=0, column=5, padx=5, sticky="e")

            btn_edit = ctk.CTkButton(btn_frame, text="✏️", width=28, height=28, fg_color="transparent", hover_color="#d35400", 
                                     command=lambda t=task: self._carica_task_in_form(t))
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(btn_frame, text="🗑️", width=28, height=28, fg_color="transparent", hover_color="#c0392b", 
                                    command=lambda t_id=task["id"]: self.controller.elimina_task(t_id))
            btn_del.pack(side="left", padx=2)
            
            i += 1

    def aggiorna_opzioni_negozi(self):
        """Ricarica la lista alfabetica e attiva il filtro dinamico durante la digitazione."""
        if self.controller and hasattr(self.controller, "ottieni_nomi_negozi"):
            tutti_i_negozi = self.controller.ottieni_nomi_negozi()
            if tutti_i_negozi:
                self.combo_negozio.configure(values=tutti_i_negozi)
                
                if self.combo_negozio.get() not in tutti_i_negozi:
                    self.combo_negozio.set(tutti_i_negozi[0])

                def filtra_negozi_al_volo(event):
                    testo_inserito = self.combo_negozio.get().strip().lower()
                    if not testo_inserito:
                        self.combo_negozio.configure(values=tutti_i_negozi)
                    else:
                        filtrati = [n for n in tutti_i_negozi if testo_inserito in n.lower()]
                        if filtrati:
                            self.combo_negozio.configure(values=filtrati)
                        else:
                            self.combo_negozio.configure(values=["Nessun riscontro"])

                self.combo_negozio.bind("<KeyRelease>", filtra_negozi_al_volo)