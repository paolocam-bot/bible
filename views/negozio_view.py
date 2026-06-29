import customtkinter as ctk
from utils.stile import Stile  # <-- Importazione del Design System Centralizzato

class NegozioView(ctk.CTkFrame):
    def __init__(self, master, controller=None):
        super().__init__(master, fg_color="transparent")
        self.controller = controller
        self.negozio_in_modifica_codice = None  # Tiene traccia se stiamo modificando un negozio esistente

        # Configurazione layout (1 colonna principale)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # =====================================================================
        # 1. INTESTAZIONE MODULO
        # =====================================================================
        self.lbl_titolo = ctk.CTkLabel(
            self, 
            text="🏢 Gestione Anagrafica Negozi", 
            font=Stile.FONT_TITOLO,
            text_color=Stile.TEXT_MAIN
        )
        self.lbl_titolo.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # =====================================================================
        # 2. FORM DI INSERIMENTO / MODIFICA ANAGRAFICA
        # =====================================================================
        self.form_frame = ctk.CTkFrame(self, corner_radius=Stile.CORNER_RADIUS_CARD, fg_color=Stile.BG_CARD)
        self.form_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15), ipadx=10, ipady=10)
        
        # Campi del form distribuiti su griglia con stili centralizzati
        lbl_cod = ctk.CTkLabel(self.form_frame, text="Cod. Breve:", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
        lbl_cod.grid(row=0, column=0, padx=8, pady=6, sticky="w")
        self.entry_codice = ctk.CTkEntry(
            self.form_frame, width=90, placeholder_text="es. N01",
            font=Stile.FONT_NORMALE, corner_radius=Stile.CORNER_RADIUS_INPUT,
            text_color=Stile.TEXT_MAIN, placeholder_text_color=Stile.TEXT_MUTED
        )
        self.entry_codice.grid(row=0, column=1, padx=8, pady=6, sticky="w")

        lbl_nome = ctk.CTkLabel(self.form_frame, text="Nome Negozio:", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
        lbl_nome.grid(row=0, column=2, padx=8, pady=6, sticky="w")
        self.entry_nome = ctk.CTkEntry(
            self.form_frame, width=160, placeholder_text="es. Milano Duomo",
            font=Stile.FONT_NORMALE, corner_radius=Stile.CORNER_RADIUS_INPUT,
            text_color=Stile.TEXT_MAIN, placeholder_text_color=Stile.TEXT_MUTED
        )
        self.entry_nome.grid(row=0, column=3, padx=8, pady=6, sticky="w")

        lbl_coord = ctk.CTkLabel(self.form_frame, text="Coordinatore/trice:", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
        lbl_coord.grid(row=0, column=4, padx=8, pady=6, sticky="w")
        self.entry_coordinatore = ctk.CTkEntry(
            self.form_frame, width=160, placeholder_text="Nome responsabile",
            font=Stile.FONT_NORMALE, corner_radius=Stile.CORNER_RADIUS_INPUT,
            text_color=Stile.TEXT_MAIN, placeholder_text_color=Stile.TEXT_MUTED
        )
        self.entry_coordinatore.grid(row=0, column=5, padx=8, pady=6, sticky="w")

        lbl_clifor = ctk.CTkLabel(self.form_frame, text="Cod. Cli/For:", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
        lbl_clifor.grid(row=1, column=0, padx=8, pady=6, sticky="w")
        self.entry_clifor = ctk.CTkEntry(
            self.form_frame, width=90, placeholder_text="es. 401001",
            font=Stile.FONT_NORMALE, corner_radius=Stile.CORNER_RADIUS_INPUT,
            text_color=Stile.TEXT_MAIN, placeholder_text_color=Stile.TEXT_MUTED
        )
        self.entry_clifor.grid(row=1, column=1, padx=8, pady=6, sticky="w")

        lbl_conto = ctk.CTkLabel(self.form_frame, text="Ragione / Conto:", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
        lbl_conto.grid(row=1, column=2, padx=8, pady=6, sticky="w")
        self.entry_conto = ctk.CTkEntry(
            self.form_frame, placeholder_text="es. S.R.L. Logistica Ges",
            font=Stile.FONT_NORMALE, corner_radius=Stile.CORNER_RADIUS_INPUT,
            text_color=Stile.TEXT_MAIN, placeholder_text_color=Stile.TEXT_MUTED
        )
        self.entry_conto.grid(row=1, column=3, columnspan=3, padx=8, pady=6, sticky="ew")

        self.form_frame.grid_columnconfigure(3, weight=1)

        # Frame Bottoni Azione Form
        self.azioni_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.azioni_frame.grid(row=2, column=0, columnspan=6, padx=5, pady=8, sticky="e")

        # Estrazione colori semantici per l'interfaccia coerente
        colore_sfondo_add, colore_testo_add = Stile.ottieni_stile_stato("risolto")
        colore_sfondo_del, colore_testo_del = Stile.ottieni_stile_stato("eliminato")
        colore_sfondo_mod, colore_testo_mod = Stile.ottieni_stile_stato("lavorazione")

        self.btn_elimina = ctk.CTkButton(
            self.azioni_frame, text="Elimina Negozio", 
            fg_color=colore_sfondo_del, text_color=colore_testo_del,
            hover_color=("#dc3545", "#842029"), width=120, font=Stile.FONT_BADGE,
            corner_radius=Stile.CORNER_RADIUS_INPUT, command=self._on_elimina_click
        )
        self.btn_annulla = ctk.CTkButton(
            self.azioni_frame, text="Annulla", 
            fg_color=Stile.BTN_SECONDARY_BG, text_color=Stile.BTN_SECONDARY_TEXT,
            hover_color=Stile.BTN_SECONDARY_HOVER, width=90, font=Stile.FONT_BADGE,
            corner_radius=Stile.CORNER_RADIUS_INPUT, command=self._pulisci_form
        )
        self.btn_salva = ctk.CTkButton(
            self.azioni_frame, text="Aggiungi Negozio", 
            fg_color=colore_sfondo_add, text_color=colore_testo_add,
            hover_color=("#198754", "#0f5132"), width=130, font=Stile.FONT_BADGE,
            corner_radius=Stile.CORNER_RADIUS_INPUT, command=self._on_salva_click
        )
        self.btn_salva.pack(side="right", padx=4)

        # Conserviamo i riferimenti dei colori di aggiunta per ripristinarli dinamicamente in pulisci_form
        self._colore_verde_add = colore_sfondo_add
        self._colore_testo_add = colore_testo_add
        self._colore_arancio_mod = colore_sfondo_mod
        self._colore_testo_mod = colore_testo_mod

        # =====================================================================
        # 3. BARRA DI RICERCA AVANZATA
        # =====================================================================
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.search_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Cerca in tempo reale per nome negozio o per coordinatrice...",
            height=38, font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN,
            placeholder_text_color=Stile.TEXT_MUTED, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda event: self._on_ricerca_dinamica())

        self.search_btn = ctk.CTkButton(
            self.search_frame, text="Cerca", width=100, height=38, font=Stile.FONT_BADGE,
            fg_color=Stile.BTN_PRIMARY_BG, hover_color=Stile.BTN_PRIMARY_HOVER,
            text_color=Stile.BTN_PRIMARY_TEXT, corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.search_btn.grid(row=0, column=1, sticky="e")

        # =====================================================================
        # 4. AREA RISULTATI (ScrollableFrame)
        # =====================================================================
        self.results_frame = ctk.CTkScrollableFrame(
            self, label_text="Anagrafiche Negozi Trovate",
            label_font=Stile.FONT_BADGE, label_text_color=Stile.BTN_PRIMARY_BG,
            fg_color=Stile.BG_PRINCIPALE
        )
        self.results_frame.grid(row=3, column=0, sticky="nsew")

    def imposta_controller(self, controller):
        self.controller = controller

    def mostra_negozi(self, lista_negozi):
        """Svuota la griglia e renderizza graficamente la lista dei negozi con i loro info."""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not lista_negozi:
            lbl_no_res = ctk.CTkLabel(
                self.results_frame, text="Nessun negozio trovato con i criteri inseriti.", 
                font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MUTED
            )
            lbl_no_res.pack(pady=20)
            return

        for n in lista_negozi:
            card = ctk.CTkFrame(self.results_frame, fg_color=Stile.BG_CARD, corner_radius=Stile.CORNER_RADIUS_CARD)
            card.pack(fill="x", padx=5, pady=5, ipadx=12, ipady=12)
            
            # Contenitore destro per i tasti di gestione rapida della card
            btn_container = ctk.CTkFrame(card, fg_color="transparent")
            btn_container.pack(side="right", fill="y", padx=5)

            btn_edit_card = ctk.CTkButton(
                btn_container, text="✏️", width=34, height=34,
                fg_color="transparent", hover_color=Stile.BTN_SECONDARY_HOVER,
                text_color=Stile.TEXT_MAIN, font=ctk.CTkFont(size=14),
                command=lambda negozio=n: self._carica_negozio_in_form(negozio)
            )
            btn_edit_card.pack(side="right", padx=5)

            # Layout dati interno alla schedina
            lbl_nome = ctk.CTkLabel(card, text=f"🏬 {n.nome} ({n.codice_breve})", font=Stile.FONT_SUBTITLE, text_color=Stile.TEXT_MAIN)
            lbl_nome.pack(anchor="w")
            
            lbl_coord = ctk.CTkLabel(card, text=f"👩‍💼 Coordinatrice: {n.coordinatore}", font=Stile.FONT_NORMALE, text_color=Stile.TEXT_MAIN)
            lbl_coord.pack(anchor="w", pady=(2, 0))

            lbl_info = ctk.CTkLabel(
                card, 
                text=f"🔑 Cod. Cli/For: {n.codclifor}  |  📝 Ragione/Conto: {n.descrizione_conto}", 
                font=Stile.FONT_NORMALE,
                text_color=Stile.TEXT_MUTED
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

        # Cambia veste grafica ai pulsanti (Modalità Modifica)
        self.btn_salva.configure(
            text="Salva Modifiche", 
            fg_color=self._colore_arancio_mod, 
            text_color=self._colore_testo_mod,
            hover_color=("#e67e22", "#d35400")
        )
        self.btn_annulla.pack(side="left", padx=4)
        self.btn_elimina.pack(side="left", padx=4)

    def _pulisci_form(self):
        """Completa ed esegue il reset del form, nascondendo i pulsanti contestuali."""
        self.negozio_in_modifica_codice = None
        self.entry_codice.configure(state="normal")
        self.entry_codice.delete(0, "end")
        self.entry_nome.delete(0, "end")
        self.entry_coordinatore.delete(0, "end")
        self.entry_clifor.delete(0, "end")
        self.entry_conto.delete(0, "end")

        # Ripristina la configurazione iniziale del bottone principale
        self.btn_salva.configure(
            text="Aggiungi Negozio", 
            fg_color=self._colore_verde_add, 
            text_color=self._colore_testo_add,
            hover_color=("#198754", "#0f5132")
        )
        
        # Rimozione sicura dei bottoni extra della modalità modifica
        self.btn_annulla.pack_forget()
        self.btn_elimina.pack_forget()

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