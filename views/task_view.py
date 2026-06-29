import customtkinter as ctk
from datetime import datetime
from utils.stile import Stile  # <-- Importazione del Design System Centralizzato

class TaskView(ctk.CTkFrame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self.task_in_modifica_id = None 

        # =====================================================================
        # 1. TITOLO DELLA SEZIONE
        # =====================================================================
        lbl_titolo = ctk.CTkLabel(
            self, text="📋 Registro Task & Interventi Conclusi", 
            font=Stile.FONT_TITOLO, text_color=Stile.TEXT_MAIN
        )
        lbl_titolo.pack(pady=(10, 15), anchor="w", padx=10)

        # =====================================================================
        # 2. DASHBOARD DELLE STATISTICHE (Stile coerente ed estrazione stati)
        # =====================================================================
        self.stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.stats_frame.pack(fill="x", padx=10, pady=(0, 15))

        # Configurazione a 3 colonne uguali e responsive
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1, uniform="equal")

        # Recupero dei colori di stato centralizzati dal modulo Stile
        bg_del, txt_del = Stile.ottieni_stile_stato("eliminato")     # Rosso / Task Pendenti
        bg_ris, txt_ris = Stile.ottieni_stile_stato("risolto")       # Verde / Completati Oggi
        bg_lav, txt_lav = Stile.ottieni_stile_stato("lavorazione")   # Arancio-Giallo / Critico

        # Card 1: Task Pendenti (In corso)
        self.card_pendenti = ctk.CTkFrame(self.stats_frame, fg_color=bg_del, corner_radius=Stile.CORNER_RADIUS_CARD)
        self.card_pendenti.grid(row=0, column=0, padx=6, pady=5, sticky="nsew")
        self.lbl_val_pendenti = ctk.CTkLabel(self.card_pendenti, text="0", font=ctk.CTkFont(size=26, weight="bold"), text_color=txt_del)
        self.lbl_val_pendenti.pack(pady=(12, 0))
        ctk.CTkLabel(self.card_pendenti, text="🔴 Task in Corso", font=Stile.FONT_BADGE, text_color=txt_del).pack(pady=(0, 12))

        # Card 2: Interventi Completati Oggi
        self.card_oggi = ctk.CTkFrame(self.stats_frame, fg_color=bg_ris, corner_radius=Stile.CORNER_RADIUS_CARD)
        self.card_oggi.grid(row=0, column=1, padx=6, pady=5, sticky="nsew")
        self.lbl_val_oggi = ctk.CTkLabel(self.card_oggi, text="0", font=ctk.CTkFont(size=26, weight="bold"), text_color=txt_ris)
        self.lbl_val_oggi.pack(pady=(12, 0))
        ctk.CTkLabel(self.card_oggi, text="🟢 Completati Oggi", font=Stile.FONT_BADGE, text_color=txt_ris).pack(pady=(0, 12))

        # Card 3: Negozio più Problematico (Settimana)
        self.card_critico = ctk.CTkFrame(self.stats_frame, fg_color=bg_lav, corner_radius=Stile.CORNER_RADIUS_CARD)
        self.card_critico.grid(row=0, column=2, padx=6, pady=5, sticky="nsew")
        self.lbl_val_critico = ctk.CTkLabel(self.card_critico, text="Nessuno", font=ctk.CTkFont(size=15, weight="bold"), text_color=txt_lav)
        self.lbl_val_critico.pack(pady=(16, 0))
        ctk.CTkLabel(self.card_critico, text="📊 Top Critico (Settimana)", font=Stile.FONT_BADGE, text_color=txt_lav).pack(pady=(0, 12))

        # =====================================================================
        # 3. FORM DI INSERIMENTO / MODIFICA (Campi uniformati ed estesi)
        # =====================================================================
        self.form_frame = ctk.CTkFrame(self, corner_radius=Stile.CORNER_RADIUS_CARD, fg_color=Stile.BG_CARD)
        self.form_frame.pack(fill="x", padx=10, pady=5, ipadx=10, ipady=10)

        # Configurazione colonne griglia del Form
        self.form_frame.grid_columnconfigure((1, 3, 5, 7), weight=1)
        
        altezza_input = 38
        font_label = ctk.CTkFont(size=12, weight="bold")

        # Riga 0: Data, Negozio, Operatore e Stato
        lbl_data = ctk.CTkLabel(self.form_frame, text="Data:", font=font_label, text_color=Stile.TEXT_MAIN)
        lbl_data.grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.entry_data = ctk.CTkEntry(
            self.form_frame, height=altezza_input, font=Stile.FONT_NORMALE,
            text_color=Stile.TEXT_MAIN, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.entry_data.grid(row=0, column=1, padx=8, pady=6, sticky="ew")

        lbl_negozio = ctk.CTkLabel(self.form_frame, text="Negozio:", font=font_label, text_color=Stile.TEXT_MAIN)
        lbl_negozio.grid(row=0, column=2, padx=8, pady=6, sticky="w")
        self.combo_negozio = ctk.CTkComboBox(
            self.form_frame, values=["Nessun Negozio"], height=altezza_input, font=Stile.FONT_NORMALE,
            text_color=Stile.TEXT_MAIN, corner_radius=Stile.CORNER_RADIUS_INPUT, dropdown_font=Stile.FONT_NORMALE
        )
        self.combo_negozio.grid(row=0, column=3, padx=8, pady=6, sticky="ew")

        lbl_op = ctk.CTkLabel(self.form_frame, text="Operatore:", font=font_label, text_color=Stile.TEXT_MAIN)
        lbl_op.grid(row=0, column=4, padx=8, pady=6, sticky="w")
        self.entry_operatore = ctk.CTkEntry(
            self.form_frame, height=altezza_input, placeholder_text="Nome tecnico",
            font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN, 
            placeholder_text_color=Stile.TEXT_MUTED, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.entry_operatore.grid(row=0, column=5, padx=8, pady=6, sticky="ew")

        lbl_stato = ctk.CTkLabel(self.form_frame, text="Stato:", font=font_label, text_color=Stile.TEXT_MAIN)
        lbl_stato.grid(row=0, column=6, padx=8, pady=6, sticky="w")
        self.combo_stato = ctk.CTkComboBox(
            self.form_frame, values=["Risolto", "Da finire / Incompleto", "In attesa feedback"], 
            height=altezza_input, font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN,
            corner_radius=Stile.CORNER_RADIUS_INPUT, dropdown_font=Stile.FONT_NORMALE
        )
        self.combo_stato.grid(row=0, column=7, padx=8, pady=6, sticky="ew")

        # Riga 1: Campo Note ampio
        lbl_note = ctk.CTkLabel(self.form_frame, text="Note / Dettagli:", font=font_label, text_color=Stile.TEXT_MAIN)
        lbl_note.grid(row=1, column=0, padx=8, pady=(8, 0), sticky="nw")
        
        self.entry_note = ctk.CTkTextbox(
            self.form_frame, height=75, activate_scrollbars=True, font=Stile.FONT_NORMALE,
            text_color=Stile.TEXT_MAIN, fg_color=Stile.BG_PRINCIPALE, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.entry_note.grid(row=1, column=1, columnspan=7, padx=8, pady=8, sticky="ew")

        # Riga 2: Contenitore Pulsanti di Azione Form
        self.azioni_btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.azioni_btn_frame.grid(row=2, column=1, columnspan=7, padx=5, pady=(5, 0), sticky="e")

        self.btn_annulla = ctk.CTkButton(
            self.azioni_btn_frame, text="Annulla", 
            fg_color=Stile.BTN_SECONDARY_BG, text_color=Stile.BTN_SECONDARY_TEXT,
            hover_color=Stile.BTN_SECONDARY_HOVER, width=90, height=36, font=Stile.FONT_BADGE,
            corner_radius=Stile.CORNER_RADIUS_INPUT, command=self._pulisci_form
        )
        self.btn_azione = ctk.CTkButton(
            self.azioni_btn_frame, text="Inserisci Task", 
            fg_color=Stile.BTN_PRIMARY_BG, text_color=Stile.BTN_PRIMARY_TEXT,
            hover_color=Stile.BTN_PRIMARY_HOVER, width=130, height=36, font=Stile.FONT_BADGE,
            corner_radius=Stile.CORNER_RADIUS_INPUT, command=self._on_azione_click
        )
        self.btn_azione.pack(side="right", padx=4)

        # Referenze per i colori dinamici delle azioni nel controller
        self._colore_blu_add = Stile.BTN_PRIMARY_BG
        self._colore_arancio_mod = txt_lav

        # =====================================================================
        # 4. BARRA DI RICERCA TASK
        # =====================================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.pack(fill="x", padx=10, pady=(15, 0))
        
        lbl_cerca = ctk.CTkLabel(self.search_frame, text="🔍 Filtra Task:", font=Stile.FONT_SUBTITLE, text_color=Stile.TEXT_MAIN)
        lbl_cerca.pack(side="left", padx=(0, 10))
        
        self.entry_ricerca = ctk.CTkEntry(
            self.search_frame, placeholder_text="Digita una data (gg/mm/aaaa) o il nome di un negozio per filtrare...", 
            height=38, font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN,
            placeholder_text_color=Stile.TEXT_MUTED, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.entry_ricerca.pack(side="left", fill="x", expand=True)
        self.entry_ricerca.bind("<KeyRelease>", lambda event: self.aggiorna_tabella())

        # =====================================================================
        # 5. HEADER TABELLA DI VISUALIZZAZIONE
        # =====================================================================
        header_table = ctk.CTkFrame(self, fg_color=Stile.BTN_PRIMARY_BG, height=34, corner_radius=4)
        header_table.pack(fill="x", padx=10, pady=(12, 0))
        header_table.pack_propagate(False)
        
        ctk.CTkLabel(header_table, text="Data", text_color=Stile.BTN_PRIMARY_TEXT, font=Stile.FONT_BADGE, width=90, anchor="w").pack(side="left", padx=12, pady=3)
        ctk.CTkLabel(header_table, text="Negozio", text_color=Stile.BTN_PRIMARY_TEXT, font=Stile.FONT_BADGE, width=150, anchor="w").pack(side="left", padx=12, pady=3)
        ctk.CTkLabel(header_table, text="Operatore", text_color=Stile.BTN_PRIMARY_TEXT, font=Stile.FONT_BADGE, width=110, anchor="w").pack(side="left", padx=12, pady=3)
        ctk.CTkLabel(header_table, text="Stato", text_color=Stile.BTN_PRIMARY_TEXT, font=Stile.FONT_BADGE, width=150, anchor="w").pack(side="left", padx=12, pady=3)
        ctk.CTkLabel(header_table, text="Note / Dettagli", text_color=Stile.BTN_PRIMARY_TEXT, font=Stile.FONT_BADGE, anchor="w").pack(side="left", padx=12, pady=3, fill="x", expand=True)

        self.scroll_table = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def imposta_controller(self, controller):
        self.controller = controller
        self.aggiorna_opzioni_negozi()
        self.aggiorna_tabella()

    def aggiorna_dashboard(self, num_pendenti, num_oggi, negozio_critico):
        self.lbl_val_pendenti.configure(text=str(num_pendenti))
        self.lbl_val_oggi.configure(text=str(num_oggi))
        
        if len(negozio_critico) > 24:
            negozio_critico = negozio_critico[:21] + "..."
        self.lbl_val_critico.configure(text=negozio_critico)

    def _on_azione_click(self):
        data = self.entry_data.get().strip()
        negozio = self.combo_negozio.get()
        op = self.entry_operatore.get().strip()
        stato = self.combo_stato.get()
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
        
        self.entry_note.delete("1.0", "end")
        self.entry_note.insert("1.0", task["note"])

        # --- GESTIONE DINAMICA DEI COLORI DI MODIFICA ---
        if "Da finire" in task["stato"]:
            # Configurazione Giallo/Oro per i task incompleti
            colore_normale = ("#f1c40f", "#f39c12")
            colore_hover = ("#d4ac0d", "#d68910")
            colore_testo = "#000000"  # Testo nero sul giallo per massima leggibilità
        else:
            # Configurazione Arancione standard per gli altri stati in modifica
            colore_normale = ("#e67e22", "#d35400")
            colore_hover = ("#d35400", "#e67e22")
            colore_testo = "#FFFFFF"  # Testo bianco sull'arancione

        self.btn_azione.configure(
            text="Salva Modifica", 
            fg_color=colore_normale, 
            hover_color=colore_hover,
            text_color=colore_testo
        )
        self.btn_annulla.pack(side="left", padx=4)

    def _pulisci_form(self):
        self.task_in_modifica_id = None
        self.entry_note.delete("1.0", "end")
        self.entry_operatore.delete(0, "end")
        self.entry_data.delete(0, "end")
        self.entry_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.combo_stato.set("Risolto")
        if self.combo_negozio.cget("values"):
            self.combo_negozio.set(self.combo_negozio.cget("values")[0])
        
        # --- RIPRISTINO STATO INIZIALE PULSANTE (DESIGN SYSTEM) ---
        self.btn_azione.configure(
            text="Inserisci Task", 
            fg_color=Stile.BTN_PRIMARY_BG, 
            hover_color=Stile.BTN_PRIMARY_HOVER,
            text_color=Stile.BTN_PRIMARY_TEXT
        )
        self.btn_annulla.pack_forget()

    def aggiorna_tabella(self):
        for widget in self.scroll_table.winfo_children():
            widget.destroy()

        if not self.controller:
            return

        testo_ricerca = self.entry_ricerca.get().strip().lower()
        tasks = self.controller.ottieni_tutte_task()
        
        # Estrazione degli stati di colore per la colonna dinamica dello stato
        _, txt_color_ris = Stile.ottieni_stile_stato("risolto")
        _, txt_color_lav = Stile.ottieni_stile_stato("lavorazione")
        _, txt_color_err = Stile.ottieni_stile_stato("eliminato")

        i = 0
        for task in reversed(tasks):
            negozio_task = task.get("negozio", "").lower()
            data_task = task.get("data", "").lower()
            
            if testo_ricerca and (testo_ricerca not in negozio_task and testo_ricerca not in data_task):
                continue

            # Gestione del background alternato basato sul design system
            bg_riga = Stile.BG_CARD if i % 2 == 0 else Stile.BG_PRINCIPALE
            
            riga = ctk.CTkFrame(self.scroll_table, fg_color=bg_riga, height=38, corner_radius=Stile.CORNER_RADIUS_INPUT)
            riga.pack(fill="x", pady=2, padx=5)
            riga.pack_propagate(False)
            riga.grid_columnconfigure(4, weight=1) 

            # Colore condizionale semantico per l'etichetta dello stato
            if task["stato"] == "Risolto":
                colore_stato = txt_color_ris
            elif "Da finire" in task["stato"]:
                colore_stato = txt_color_lav
            else:
                colore_stato = txt_color_err

            ctk.CTkLabel(riga, text=task["data"], width=85, anchor="w", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN).grid(row=0, column=0, padx=12, sticky="w")
            ctk.CTkLabel(riga, text=task.get("negozio", "N/D"), width=130, anchor="w", font=Stile.FONT_SUBTITLE, text_color=Stile.TEXT_MAIN).grid(row=0, column=1, padx=12, sticky="w")
            ctk.CTkLabel(riga, text=task["operatore"], width=100, anchor="w", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN).grid(row=0, column=2, padx=12, sticky="w")
            ctk.CTkLabel(riga, text=task["stato"], text_color=colore_stato, width=130, anchor="w", font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=3, padx=12, sticky="w")
            
            lbl_nota_testo = task["note"].replace("\n", " ")
            if len(lbl_nota_testo) > 60:
                lbl_nota_testo = lbl_nota_testo[:57] + "..."
                
            ctk.CTkLabel(riga, text=lbl_nota_testo, anchor="w", justify="left", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MUTED).grid(row=0, column=4, padx=12, sticky="ew")
            
            btn_frame = ctk.CTkFrame(riga, fg_color="transparent")
            btn_frame.grid(row=0, column=5, padx=8, sticky="e")

            btn_edit = ctk.CTkButton(
                btn_frame, text="✏️", width=28, height=28, fg_color="transparent", hover_color=Stile.BTN_SECONDARY_HOVER, 
                text_color=Stile.TEXT_MAIN, command=lambda t=task: self._carica_task_in_form(t)
            )
            btn_edit.pack(side="left", padx=2)

            btn_del = ctk.CTkButton(
                btn_frame, text="🗑️", width=28, height=28, fg_color="transparent", hover_color=("#f8d7da", "#842029"), 
                text_color=Stile.TEXT_MAIN, command=lambda t_id=task["id"]: self.controller.elimina_task(t_id)
            )
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