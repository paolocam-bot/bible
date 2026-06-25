import customtkinter as ctk
import os
import sys
import json
from PIL import Image

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Holly-HelpDesK")
        self.geometry("1100x650")

        # 1. PERCORSO LOGO UNIVERSALE (Funziona in VS Code e in Nuitka/PyInstaller)
        if "__compiled__" in globals():
            self.cartella_progetto = os.path.dirname(os.path.abspath(sys.argv[0]))
        elif getattr(sys, 'frozen', False):
            self.cartella_progetto = os.path.dirname(os.path.abspath(sys.executable))
        else:
            cartella_views = os.path.dirname(os.path.abspath(__file__))
            self.cartella_progetto = os.path.dirname(cartella_views)
        
        percorso_logo = os.path.join(self.cartella_progetto, "data", "app.png")
        self.percorso_config = os.path.join(self.cartella_progetto, "data", "config_app.json")

        # Carica il file di configurazione esterno o usa quello di default
        self.carica_configurazione()

        # Layout: 2 colonne (Menu laterale e Area Contenuto)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 2. Sidebar di Navigazione Globale
        self.sidebar_globale = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_globale.grid(row=0, column=0, sticky="nsew")
        self.sidebar_globale.pack_propagate(False)

        # Caricamento Logo Visivo nella Sidebar
        try:
            pil_img = Image.open(percorso_logo)
            logo_sidebar = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(120, 120))
            self.lbl_logo = ctk.CTkLabel(self.sidebar_globale, image=logo_sidebar, text="")
            self.lbl_logo.pack(padx=20, pady=(25, 20))
        except Exception as e:
            print(f"Impossibile caricare il logo nella sidebar: {e}")
            self.lbl_logo = ctk.CTkLabel(self.sidebar_globale, text="⚙️ HUB UTILITY", font=ctk.CTkFont(size=16, weight="bold"))
            self.lbl_logo.pack(padx=20, pady=20)

        # Contenitore per i bottoni delle categorie (per pulirli e ridisegnarli facilmente)
        self.menu_bottoni_frame = ctk.CTkFrame(self.sidebar_globale, fg_color="transparent")
        self.menu_bottoni_frame.pack(fill="both", expand=True)

        # 3. CONTENITORE AREA MODULI ALTERNABILI
        self.container_area = ctk.CTkFrame(self, fg_color="transparent")
        self.container_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container_area.grid_columnconfigure(0, weight=1)
        self.container_area.grid_rowconfigure(0, weight=1)

        # Inizializza il dizionario dei bottoni e disegna la sidebar
        self.bottoni_sidebar = {}
        self.aggiorna_sidebar_grafica()

    def carica_configurazione(self):
        """Legge le categorie dal file JSON esterno se esiste, altrimenti usa il default."""
        if os.path.exists(self.percorso_config):
            try:
                with open(self.percorso_config, "r", encoding="utf-8") as f:
                    self.configurazione_sezioni = json.load(f)
                    return
            except Exception:
                pass
        
        # Configurazione di fallback iniziale se il file non esiste
        self.configurazione_sezioni = [
            {"id": "zebra",    "testo": "🖨️ Assistente Zebra",       "db": "database_manuale.json",   "tipo": "manuale"},
            {"id": "brother",  "testo": "🖨️ Assistente Brother",     "db": "database_brother.json",   "tipo": "manuale"},
            {"id": "app",      "testo": "💻 Problemi App GDV BI",    "db": "problemi_app.json",       "tipo": "manuale"},
            {"id": "mt",       "testo": "💰 Anomalie App METODO",    "db": "database_mt.json",        "tipo": "manuale"},
            {"id": "negozi",   "testo": "🏬 Anagrafica Negozi",      "db": "database_negozi.json",    "tipo": "negozio"}
        ]
        self.salva_configurazione()

    def salva_configurazione(self):
        """Salva lo stato attuale delle categorie nel file JSON."""
        os.makedirs(os.path.dirname(self.percorso_config), exist_ok=True)
        with open(self.percorso_config, "w", encoding="utf-8") as file:
            json.dump(self.configurazione_sezioni, file, indent=4, ensure_ascii=False)

    def aggiorna_sidebar_grafica(self):
        """Svuota e ricostruisce i bottoni nella sidebar (utile dopo un inserimento o rimozione)."""
        # Elimina i vecchi bottoni a schermo
        for widget in self.menu_bottoni_frame.winfo_children():
            widget.destroy()
        
        self.bottoni_sidebar.clear()

        # Ridisegna i bottoni basandosi sulla configurazione aggiornata
        for sezione in self.configurazione_sezioni:
            btn = ctk.CTkButton(self.menu_bottoni_frame, text=sezione["testo"], anchor="w")
            btn.pack(fill="x", padx=15, pady=5)
            self.bottoni_sidebar[sezione["id"]] = btn

    def mostra_sezione(self, frame_sezione):
        """Nasconde gli altri frame e porta in primo piano quello selezionato."""
        frame_sezione.grid(row=0, column=0, sticky="nsew")
        frame_sezione.tkraise()

    def imposta_controller_per_creazione(self, controller):
        """Riceve il controller per poter invocare la creazione o rimozione delle categorie."""
        self.controller_riferimento = controller
        
        # Crea il pulsante di gestione in fondo alla sidebar
        self.btn_aggiungi_cat = ctk.CTkButton(
            self.sidebar_globale, 
            text="⚙️ Gestisci Categorie", 
            fg_color="#27ae60", 
            hover_color="#219653",
            command=self.apri_popup_gestione_categorie
        )
        self.btn_aggiungi_cat.pack(side="bottom", fill="x", padx=15, pady=15)

    def apri_popup_gestione_categorie(self):
        """Apre una finestra popup per aggiungere o rimuovere le categorie esistenti."""
        popup = ctk.CTkToplevel(self)
        popup.title("Gestione Categorie")
        popup.geometry("450x650")
        popup.after(100, lambda: popup.focus())
        popup.grab_set()

        # --- SEZIONE 1: RIMOZIONE CATEGORIE ESISTENTI ---
        lbl_rimuovi = ctk.CTkLabel(popup, text="❌ Rimuovi Categorie Esistenti:", font=ctk.CTkFont(weight="bold"))
        lbl_rimuovi.pack(pady=(10, 5), padx=20, anchor="w")

        # Frame con scrollbar per listare i bottoni attuali
        scroll_frame = ctk.CTkScrollableFrame(popup, height=120)
        scroll_frame.pack(fill="x", padx=20, pady=5)

        def elimina_categoria(id_da_eliminare):
            self.controller_riferimento.rimuovi_categoria(id_da_eliminare)
            popup.destroy()

        for sezione in self.configurazione_sezioni:
            # Non permettiamo di cancellare l'anagrafica negozi principale o zebra per sicurezza grafica iniziale
            if sezione["id"] == "negozi":
                continue
                
            item_frame = ctk.CTkFrame(scroll_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            lbl_item = ctk.CTkLabel(item_frame, text=sezione["testo"], anchor="w")
            lbl_item.pack(side="left", padx=5, fill="x", expand=True)
            
            btn_del = ctk.CTkButton(
                item_frame, text="❌", width=30, fg_color="#c0392b", hover_color="#e74c3c",
                command=lambda id_sez=sezione["id"]: elimina_categoria(id_sez)
            )
            btn_del.pack(side="right", padx=5)

        # Separatore visivo
        separatore = ctk.CTkFrame(popup, height=2, fg_color="gray")
        separatore.pack(fill="x", padx=20, pady=15)

        # --- SEZIONE 2: AGGIUNTA NUOVA CATEGORIA ---
        lbl_aggiungi = ctk.CTkLabel(popup, text="➕ Aggiungi Nuova Categoria:", font=ctk.CTkFont(weight="bold"))
        lbl_aggiungi.pack(pady=(0, 5), padx=20, anchor="w")

        lbl_nome = ctk.CTkLabel(popup, text="Nome Assistente (es: Epson):")
        lbl_nome.pack(pady=2)
        entry_nome = ctk.CTkEntry(popup, width=300)
        entry_nome.pack(pady=2)

        lbl_db = ctk.CTkLabel(popup, text="Nome File Database (es: database_epson.json):")
        lbl_db.pack(pady=2)
        entry_db = ctk.CTkEntry(popup, width=300)
        entry_db.pack(pady=2)

        def conferma_aggiunta():
            nome = entry_nome.get().strip()
            db_file = entry_db.get().strip()
            if nome and db_file:
                if not db_file.endswith(".json"):
                    db_file += ".json"
                self.controller_riferimento.aggiungi_nuova_categoria(nome, db_file)
                popup.destroy()

        btn_conferma = ctk.CTkButton(popup, text="Salva e Crea", fg_color="#27ae60", hover_color="#219653", command=conferma_aggiunta)
        btn_conferma.pack(pady=15)