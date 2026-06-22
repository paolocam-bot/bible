import customtkinter as ctk

class BrotherView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar interna
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=12)
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(0, 12))
        self.sidebar.pack_propagate(False)

        self.sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="🖨️ ERRORI BROTHER",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.sidebar_title.pack(padx=15, pady=(20, 10), anchor="w")

        separator = ctk.CTkFrame(self.sidebar, height=2, fg_color=("gray75", "gray30"))
        separator.pack(fill="x", padx=15, pady=(0, 10))

        self.buttons_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        self.buttons_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Area Centrale
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=0)
        self.main_area.grid_rowconfigure(1, weight=1)

        # Barra di ricerca
        self.search_frame = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="🔍 Cerca anomalia o errore Brother (es. inceppamento, offline)...",
            height=38
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 12))

        self.search_btn = ctk.CTkButton(
            self.search_frame, text="Cerca", width=100, height=38, font=ctk.CTkFont(weight="bold")
        )
        self.search_btn.grid(row=0, column=1, sticky="e")

        # Scheda Dettagli
        self.content_card = ctk.CTkFrame(self.main_area, corner_radius=12)
        self.content_card.grid(row=1, column=0, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.content_card, text="Seleziona una problematica Brother", font=ctk.CTkFont(size=22, weight="bold"), justify="left", anchor="w"
        )
        self.title_label.pack(fill="x", anchor="w", padx=25, pady=(25, 5))

        self.desc_label = ctk.CTkLabel(
            self.content_card, text="Usa la barra superiore o seleziona un guasto dall'indice a sinistra.",
            font=ctk.CTkFont(size=13, slant="italic"), text_color=("gray50", "gray60"), justify="left", anchor="w"
        )
        self.desc_label.pack(fill="x", anchor="w", padx=25, pady=(0, 20))

        # Pulsanti CRUD
        self.actions_frame = ctk.CTkFrame(self.content_card, fg_color="transparent")
        self.actions_frame.pack(fill="x", padx=25, pady=(0, 15))

        self.btn_add = ctk.CTkButton(self.actions_frame, text="➕ Aggiungi", width=90, fg_color="green", hover_color="darkgreen")
        self.btn_add.pack(side="left", padx=5)

        self.btn_edit = ctk.CTkButton(self.actions_frame, text="📝 Modifica", width=90)
        self.btn_edit.pack(side="left", padx=5)

        self.btn_delete = ctk.CTkButton(self.actions_frame, text="🗑️ Elimina", width=90, fg_color="red", hover_color="darkred")
        self.btn_delete.pack(side="left", padx=5)

        # Frame Procedure
        self.steps_frame = ctk.CTkScrollableFrame(
            self.content_card, label_text="📌 FASI DI RIPRISTINO STAMPANTE",
            label_font=ctk.CTkFont(size=12, weight="bold"), label_text_color=("#1f538d", "#a9cde2"), fg_color=("gray95", "gray18")
        )
        self.steps_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.content_card.bind("<Configure>", self._adatta_lunghezza_testo)

    def popola_sidebar(self, lista_problemi, on_button_click_callback):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        for prob in lista_problemi:
            item_frame = ctk.CTkFrame(self.buttons_frame, fg_color="transparent", height=40, cursor="hand2")
            item_frame.pack(fill="x", padx=5, pady=3)

            lbl_testo = ctk.CTkLabel(
                item_frame, text=f"• {prob.titolo}", font=ctk.CTkFont(size=12, weight="normal"),
                justify="left", anchor="w", wraplength=230, cursor="hand2"
            )
            lbl_testo.pack(fill="both", expand=True, padx=10, pady=5)

            for widget in (item_frame, lbl_testo):
                widget.bind("<Button-1>", lambda e, p=prob: on_button_click_callback(p))
                widget.bind("<Enter>", lambda e, f=item_frame: f.configure(fg_color=("gray80", "gray28")))
                widget.bind("<Leave>", lambda e, f=item_frame: f.configure(fg_color="transparent"))

    def aggiorna_dettagli(self, titolo, descrizione, soluzioni):
        self.title_label.configure(text=titolo)
        self.desc_label.configure(text=descrizione)
        self._adatta_lunghezza_testo()

        for widget in self.steps_frame.winfo_children():
            widget.destroy()

        for i, sol in enumerate(soluzioni, 1):
            step_container = ctk.CTkFrame(self.steps_frame, fg_color=("white", "gray24"), corner_radius=8)
            step_container.pack(fill="x", padx=8, pady=5, ipadx=10, ipady=8)
            
            lbl_num = ctk.CTkLabel(
                step_container, text=f"STEP {i}", font=ctk.CTkFont(size=11, weight="bold"),
                text_color="white", fg_color=("#1f538d", "#246ab7"), corner_radius=4, width=60, height=22
            )
            lbl_num.pack(side="left", anchor="n", padx=(5, 10), pady=2)

            lbl_testo = ctk.CTkLabel(
                step_container, text=sol, font=ctk.CTkFont(size=12, weight="normal"), justify="left", anchor="w", wraplength=520
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