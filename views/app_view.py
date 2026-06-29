import customtkinter as ctk
from utils.stile import Stile  # <-- Importazione del Design System Centralizzato

class AppView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Layout Responsivo
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =====================================================================
        # 1. SIDEBAR INTERNA (Indice problemi applicazione)
        # =====================================================================
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=Stile.CORNER_RADIUS_CARD, fg_color=Stile.BG_CARD)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.sidebar.pack_propagate(False)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="💻 ERRORI APPLICAZIONE",
            font=Stile.FONT_SUBTITLE,
            text_color=Stile.TEXT_MAIN
        )
        self.sidebar_title.pack(padx=15, pady=(20, 10), anchor="w")

        # Separatore coordinato con i bordi del tema
        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color=Stile.BTN_SECONDARY_BG)
        separator.pack(fill="x", padx=15, pady=(0, 10))

        self.buttons_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # =====================================================================
        # 2. AREA CONTENUTO CENTRALE
        # =====================================================================
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=0)
        self.main_area.grid_rowconfigure(1, weight=1)

        # BARRA DI RICERCA SOFTWARE
        self.search_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Cerca anomalia o codice errore applicativo...",
            height=38,
            font=Stile.FONT_NORMALE,
            text_color=Stile.TEXT_MAIN,
            placeholder_text_color=Stile.TEXT_MUTED,
            corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        self.search_btn = ctk.CTkButton(
            self.search_frame, 
            text="Cerca", 
            width=100, 
            height=38,
            font=Stile.FONT_BADGE,
            fg_color=Stile.BTN_PRIMARY_BG,
            hover_color=Stile.BTN_PRIMARY_HOVER,
            text_color=Stile.BTN_PRIMARY_TEXT,
            corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.search_btn.grid(row=0, column=1, sticky="e")

        # SCHEDA DETTAGLI
        self.content_card = ctk.CTkFrame(self.main_area, corner_radius=Stile.CORNER_RADIUS_CARD, fg_color=Stile.BG_CARD)
        self.content_card.grid(row=1, column=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.content_card,
            text="Seleziona una problematica",
            font=Stile.FONT_TITOLO,
            text_color=Stile.TEXT_MAIN,
            justify="left",
            anchor="w"
        )
        self.title_label.pack(fill="x", anchor="w", padx=25, pady=(25, 5))

        self.desc_label = ctk.CTkLabel(
            self.content_card,
            text="Usa la barra di ricerca o seleziona un ticket dall'indice software.",
            font=Stile.FONT_NORMALE,
            text_color=Stile.TEXT_MUTED,
            justify="left",
            anchor="w"
        )
        self.desc_label.pack(fill="x", anchor="w", padx=25, pady=(0, 20))

        # FRAME AZIONI CRUDS
        self.actions_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=25, pady=(0, 15))

        # Estrazione degli stili semantici per i bottoni CRUD
        colore_sfondo_add, colore_testo_add = Stile.ottieni_stile_stato("risolto")
        colore_sfondo_del, colore_testo_del = Stile.ottieni_stile_stato("eliminato")

        self.btn_add = ctk.CTkButton(
            self.actions_frame, 
            text="➕ Aggiungi", 
            width=95,
            font=Stile.FONT_BADGE,
            fg_color=colore_sfondo_add,
            hover_color=("#198754", "#0f5132"), # Hover verde coordinato
            text_color=colore_testo_add,
            corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.btn_add.pack(side="left", padx=5)

        self.btn_edit = ctk.CTkButton(
            self.actions_frame, 
            text="📝 Modifica", 
            width=95,
            font=Stile.FONT_BADGE,
            fg_color=Stile.BTN_SECONDARY_BG,
            hover_color=Stile.BTN_SECONDARY_HOVER,
            text_color=Stile.BTN_SECONDARY_TEXT,
            corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.btn_edit.pack(side="left", padx=5)

        self.btn_delete = ctk.CTkButton(
            self.actions_frame, 
            text="🗑️ Elimina", 
            width=95,
            font=Stile.FONT_BADGE,
            fg_color=colore_sfondo_del,
            hover_color=("#dc3545", "#842029"), # Hover rosso coordinato
            text_color=colore_testo_del,
            corner_radius=Stile.CORNER_RADIUS_INPUT
        )
        self.btn_delete.pack(side="left", padx=5)

        # STEPS FRAME
        self.steps_frame = ctk.CTkScrollableFrame(
            self.content_card, 
            label_text="📌 PROCEDURE DI RIPRISTINO SOFTWARE",
            label_font=Stile.FONT_BADGE,
            label_text_color=Stile.BTN_PRIMARY_BG,
            fg_color=Stile.BG_PRINCIPALE
        )
        self.steps_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.content_card.bind("<Configure>", self._adatta_lunghezza_testo)

    def popola_sidebar(self, lista_problemi, on_button_click_callback):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        # Colore hover per gli elementi della lista coerente con il tema
        colore_hover_riga = ("#e2e8f0", "#334155")

        for prob in lista_problemi:
            item_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent", height=40, cursor="hand2")
            item_frame.pack(fill="x", padx=5, pady=3)

            lbl_testo = ctk.CTkLabel(
                item_frame,
                text=f"• {prob.titolo}",
                font=Stile.FONT_NORMALE,
                text_color=Stile.TEXT_MAIN,
                justify="left",
                anchor="w",
                wraplength=230,
                cursor="hand2"
            )
            lbl_testo.pack(fill="both", expand=True, padx=10, pady=5)

            for widget in (item_frame, lbl_testo):
                widget.bind("<Button-1>", lambda e, p=prob: on_button_click_callback(p))
                widget.bind("<Enter>", lambda e, f=item_frame: f.configure(fg_color=colore_hover_riga))
                widget.bind("<Leave>", lambda e, f=item_frame: f.configure(fg_color="transparent"))

    def aggiorna_dettagli(self, titolo, descrizione, solutions):
        self.title_label.configure(text=titolo)
        self.desc_label.configure(text=descrizione)
        self._adatta_lunghezza_testo()

        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        # Generazione dei badge STEP usando i colori semantici corretti
        sfondo_badge_step, testo_badge_step = Stile.ottieni_stile_stato("in attesa")

        for i, sol in enumerate(solutions, 1):
            step_container = ctk.CTkFrame(self.steps_frame, fg_color=Stile.BG_CARD, corner_radius=Stile.CORNER_RADIUS_CARD)
            step_container.pack(fill="x", padx=8, pady=5, ipadx=10, ipady=8)
            
            lbl_num = ctk.CTkLabel(
                step_container, 
                text=f"STEP {i}", 
                font=Stile.FONT_BADGE,
                text_color=testo_badge_step,
                fg_color=sfondo_badge_step,
                corner_radius=4,
                width=55,
                height=22
            )
            lbl_num.pack(side="left", anchor="n", padx=(5, 10), pady=2)

            lbl_testo = ctk.CTkLabel(
                step_container,
                text=sol,
                font=Stile.FONT_NORMALE,
                text_color=Stile.TEXT_MAIN,
                justify="left",
                anchor="w",
                wraplength=520
            )
            lbl_testo.pack(side="left", fill="x", expand=True, padx=2)
            
            step_container.bind("<Configure>", lambda e, l=lbl_testo: l.configure(wraplength=max(200, e.width - 90)))

    def _adatta_lunghezza_testo(self, event=None):
        larghezza_attuale = self.content_card.winfo_width()
        if larghezza_attuale > 100:
            spazio_utile = larghezza_attuale - 50
            self.title_label.configure(wraplength=spazio_utile)
            self.desc_label.configure(wraplength=spazio_utile)

    def ottieni_testo_ricerca(self):
        return self.search_entry.get()