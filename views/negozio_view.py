import customtkinter as ctk


class NegozioView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.negozio_in_modifica_codice = None  # Tiene traccia se stiamo modificando un negozio esistente

        # Configurazione layout (1 colonna principale)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # 1. Intestazione modulo
        self.lbl_titolo = ctk.CTkLabel(
            self, 
            text="🏢 Gestione Anagrafica Negozi", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_titolo.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # --- 2. FORM DI INSERIMENTO / MODIFICA ---
        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Campi del form distribuiti su griglia
        lbl_cod = ctk.CTkLabel(self.form_frame, text="Cod. Breve:")
        lbl_cod.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_codice = ctk.CTkEntry(self.form_frame, width=90, placeholder_text="es. N01")
        self.entry_codice.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        lbl_nome = ctk.CTkLabel(self.form_frame, text="Nome Negozio:")
        lbl_nome.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_nome = ctk.CTkEntry(self.form_frame, width=150, placeholder_text="es. Milano Duomo")
        self.entry_nome.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        lbl_coord = ctk.CTkLabel(self.form_frame, text="Coordinatore/trice:")
        lbl_coord.grid(row=0, column=4, padx=5, pady=5, sticky="w")
        self.entry_coordinatore = ctk.CTkEntry(self.form_frame, width=150, placeholder_text="Nome responsabile")
        self.entry_coordinatore.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        lbl_clifor = ctk.CTkLabel(self.form_frame, text="Cod. Cli/For:")
        lbl_clifor.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_clifor = ctk.CTkEntry(self.form_frame, width=90, placeholder_text="es. 401001")
        self.entry_clifor.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        lbl_conto = ctk.CTkLabel(self.form_frame, text="Ragione / Conto:")
        lbl_conto.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_conto = ctk.CTkEntry(self.form_frame, placeholder_text="es. S.R.L. Logistica Ges")
        self.entry_conto.grid(row=1, column=3, columnspan=3, padx=5, pady=5, sticky="ew")

        self.form_frame.grid_columnconfigure(3, weight=1)

        # Frame Bottoni Azione Form
        self.azioni_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.azioni_frame.grid(row=2, column=0, columnspan=6, padx=5, pady=5, sticky="e")

        self.btn_elimina = ctk.CTkButton(self.azioni_frame, text="Elimina Negozio", fg_color="#c0392b", hover_color="#e74c3c", width=110, command=self._on_elimina_click)
        self.btn_annulla = ctk.CTkButton(self.azioni_frame, text="Annulla", fg_color="#7f8c8d", hover_color="#95a5a6", width=80, command=self._pulisci_form)
        self.btn_salva = ctk.CTkButton(self.azioni_frame, text="Aggiungi Negozio", fg_color="#27ae60", hover_color="#2ecc71", width=120, command=self._on_salva_click)
        self.btn_salva.pack(side="right", padx=2)

        # 3. Barra di Ricerca Avanzata
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Cerca in tempo reale per nome negozio o per coordinatrice..."
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda event: self._on_ricerca_dinamica())

        self.search_btn = ctk.CTkButton(self.search_frame, text="Cerca")
        self.search_btn.grid(row=0, column=1, sticky="e")

        # 4. Area risultati condivisibile
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Anagrafiche Negozi Trovate")
        self.results_frame.grid(row=3, column=0, sticky="nsew")

    def imposta_controller(self, controller):
        self.controller = controller

    def mostra_negozi(self, lista_negozi):
        """Svuota la griglia e renderizza graficamente la lista dei negozi con i loro info."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not lista_negozi:
            lbl_no_res = ctk.CTkLabel(self.results_frame, text="Nessun negozio trovato con i criteri inseriti.", font=ctk.CTkFont(slant="italic"))
            lbl_no_res.pack(pady=20)
            return

        for n in lista_negozi:
            card = ctk.CTkFrame(self.results_frame, fg_color=("gray85", "gray25"))
            card.pack(fill="x", padx=5, pady=5, ipadx=10, ipady=10)
            
            # Contenitore destro per i tasti di gestione rapida della card
            btn_container = ctk.CTkFrame(card, fg_color="transparent")
            btn_container.pack(side="right", fill="y", padx=5)

            # Sostituito side="center" errato con side="right" per correggere il TclError
            btn_edit_card = ctk.CTkButton(btn_container, text="✏️", width=30, fg_color="transparent", hover_color="#d35400",
                                         command=lambda negozio=n: self._carica_negozio_in_form(negozio))
            btn_edit_card.pack(side="right", padx=5)

            # Layout dati interno alla schedina
            lbl_nome = ctk.CTkLabel(card, text=f"🏬 {n.nome} ({n.codice_breve})", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_nome.pack(anchor="w")
            
            lbl_coord = ctk.CTkLabel(card, text=f"👩‍💼 Coordinatrice: {n.coordinatore}", font=ctk.CTkFont(size=13))
            lbl_coord.pack(anchor="w", pady=(2, 0))

            lbl_info = ctk.CTkLabel(
                card, 
                text=f"🔑 Cod. Cli/For: {n.codclifor}  |  📝 Ragione/Conto: {n.descrizione_conto}", 
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            lbl_info.pack(anchor="w", pady=(5, 0))

    def ottieni_testo_ricerca(self):
        return self.search_entry.get()

    def _on_ricerca_dinamica(self):
        if self.controller and hasattr(self.controller, "esegui_ricerca"):
            self.controller.esegui_ricerca()

    def _carica_negozio_in_form(self, negozio):
        """Riempie i widget superiori per avviare la modifica o eliminazione del record."""
        self.negozio_in_modifica_codice = negozio.codice_breve
        
        self.entry_codice.delete(0, "end")
        self.entry_codice.insert(0, negozio.codice_breve)
        self.entry_codice.configure(state="disabled") # Il codice breve funge da chiave primaria e non si tocca
        
        self.entry_nome.delete(0, "end")
        self.entry_nome.insert(0, negozio.nome)
        
        self.entry_coordinatore.delete(0, "end")
        self.entry_coordinatore.insert(0, negozio.coordinatore)
        
        self.entry_clifor.delete(0, "end")
        self.entry_clifor.insert(0, negozio.codclifor)
        
        self.entry_conto.delete(0, "end")
        self.entry_conto.insert(0, negozio.descrizione_conto)

        # Cambia veste grafica ai pulsanti
        self.btn_salva.configure(text="Salva Modifiche", fg_color="#d35400", hover_color="#e67e22")
        self.btn_annulla.pack(side="left", padx=2)
        self.btn_elimina.pack(side="left", padx=2)

    def _pulisci_form(self):
        self.negozio_in_modifica_codice = None
        self.entry_codice.configure(state="normal")
        self.entry_codice.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_coordinatore.delete(0, "end")
        self.entry_clifor.delete(0, "end")
        self.entry_conto.delete(0, "end")

        self.btn_salva.configure(text="Aggiungi Negozio", fg_color="#27ae60", hover_color="#2ecc71")
        self.btn_ann

    def _on_salva_click(self):
        cod = self.entry_codice.get().strip()
        nome = self.entry_nome.get().strip()
        coord = self.entry_coordinatore.get().strip()
        clifor = self.entry_clifor.get().strip()
        conto = self.entry_conto.get().strip()

        if not (cod and nome):
            return # Codice e nome sono obbligatori

        if self.controller:
            if self.negozio_in_modifica_codice:
                if hasattr(self.controller, "modifica_negozio_esistente"):
                    self.controller.modifica_negozio_esistente(self.negozio_in_modifica_codice, nome, coord, clifor, conto)
            else:
                if hasattr(self.controller, "aggiungi_nuovo_negozio"):
                    self.controller.aggiungi_nuovo_negozio(cod, nome, coord, clifor, conto)
            
            self._pulisci_form()

    def _on_elimina_click(self):
        """Rimuove il negozio selezionato tramite controller e svuota i campi."""
        if self.negozio_in_modifica_codice and self.controller:
            if hasattr(self.controller, "elimina_negozio_esistente"):
                self.controller.elimina_negozio_esistente(self.negozio_in_modifica_codice)
            self._pulisci_form()