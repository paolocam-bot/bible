import customtkinter as ctk

class NegozioView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        # Configurazione layout (1 colonna principale)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # 1. Intestazione modulo
        self.lbl_titolo = ctk.CTkLabel(
            self, 
            text="Gestione Anagrafica Negozi", 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_titolo.grid(row=0, column=0, sticky="w", pady=(0, 20))

        # 2. Barra di Ricerca Avanzata
        self.search_frame = ctk.CTkFrame(self, fg_color="transparent")
        # Rimosso fill="x", ci pensa già sticky="ew" ad allargarlo da destra a sinistra
        self.search_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.search_frame.grid_columnconfigure(0, weight=1)

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            placeholder_text="Cerca per nome negozio o per coordinatrice..."
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.search_btn = ctk.CTkButton(self.search_frame, text="Cerca")
        self.search_btn.grid(row=0, column=1, sticky="e")

        # 3. Area risultati condivisibile (ScrollableFrame per contenere la lista dei negozi)
        self.results_frame = ctk.CTkScrollableFrame(self, label_text="Anagrafiche Negozi Trovate")
        self.results_frame.grid(row=2, column=0, sticky="nsew")

    def mostra_negozi(self, lista_negozi):
        """Svuota la griglia e renderizza graficamente la lista dei negozi con le loro info."""
        # Pulisce i vecchi risultati
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        if not lista_negozi:
            lbl_no_res = ctk.CTkLabel(self.results_frame, text="Nessun negozio trovato con i criteri inseriti.", font=ctk.CTkFont(slant="italic"))
            lbl_no_res.pack(pady=20)
            return

        # Genera una "schedina" visiva per ogni negozio trovato
        for n in lista_negozi:
            card = ctk.CTkFrame(self.results_frame, fg_color=("gray85", "gray25"))
            card.pack(fill="x", padx=5, pady=5, ipadx=10, ipady=10)
            
            # Layout interno alla schedina
            lbl_nome = ctk.CTkLabel(card, text=f"🏬 {n.nome} ({n.codice_breve})", font=ctk.CTkFont(size=14, weight="bold"))
            lbl_nome.pack(anchor="w")
            
            lbl_coord = ctk.CTkLabel(card, text=f"👩‍💼 Coordinatrice: {n.coordinatore}", font=ctk.CTkFont(size=13))
            lbl_coord.pack(anchor="w", pady=(2, 0))

           
           # Sposta il colore fuori da CTkFont e inseriscilo in CTkLabel come text_color
            lbl_info = ctk.CTkLabel(
                card, 
                text=f"🔑 Cod. Cli/For: {n.codclifor}  |  📝 Ragione/Conto: {n.descrizione_conto}", 
                font=ctk.CTkFont(size=11),
                text_color="gray"
            )
            lbl_info.pack(anchor="w", pady=(5, 0))

    def ottieni_testo_ricerca(self):
        return self.search_entry.get()