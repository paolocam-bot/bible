import customtkinter as ctk
import os
from PIL import Image

class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Holly-HelpDesK")
        self.geometry("1100x650")

        # Percorso dinamico per raggiungere la cartella 'data' dalla cartella 'views'
        cartella_views = os.path.dirname(os.path.abspath(__file__))
        cartella_progetto = os.path.dirname(cartella_views)
        percorso_logo = os.path.join(cartella_progetto, "data", "app.png")

        # Applica il logo alla barra del titolo
        try:
            from tkinter import PhotoImage
            
            # Salviamo l'immagine come variabile di istanza (self.) così Python non la cancella dalla memoria!
            self.img_icona = PhotoImage(file=percorso_logo)
            
            # Applichiamo l'icona un attimo dopo l'avvio per dare tempo a Windows di creare la barra del titolo
            self.after(200, lambda: self.wm_iconphoto(False, self.img_icona))
        except Exception as e:
            print(f"Impossibile caricare il logo della barra del titolo: {e}")

        # Layout: 2 colonne (Menu laterale e Area Contenuto)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # 1. Sidebar di Navigazione Globale
        self.sidebar_globale = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_globale.grid(row=0, column=0, sticky="nsew")
        self.sidebar_globale.pack_propagate(False) # Evita che la sidebar si rimpicciolisca

        # Caricamento e inserimento del Logo visivo al posto del testo "HUB UTILITY"
        try:
            # Apriamo l'immagine usando PIL (Pillow)
            pil_img = Image.open(percorso_logo)
            
            # Definiamo la dimensione del logo nella sidebar (es. 120 pixel di larghezza per 120 di altezza)
            logo_sidebar = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(120, 120))
            
            # Creiamo la Label inserendo l'immagine ed eliminando il testo (text="")
            self.lbl_logo = ctk.CTkLabel(self.sidebar_globale, image=logo_sidebar, text="")
            self.lbl_logo.pack(padx=20, pady=(25, 20)) # Un po' di margine sopra e sotto
            
        except Exception as e:
            # Fallback di sicurezza: se l'immagine non viene trovata, rimette il testo per non far crashare l'app
            print(f"Impossibile caricare il logo nella sidebar: {e}")
            self.lbl_logo = ctk.CTkLabel(
                self.sidebar_globale, 
                text="⚙️ HUB UTILITY", 
                font=ctk.CTkFont(size=16, weight="bold")
            )
            self.lbl_logo.pack(padx=20, pady=20)

        # Bottoni del menu (Tutti ancorati a ovest 'w' e con lo stesso padding)
        self.btn_zebra = ctk.CTkButton(self.sidebar_globale, text="🖨️ Assistente Zebra", anchor="w")
        self.btn_zebra.pack(fill="x", padx=15, pady=5)

        self.btn_brother = ctk.CTkButton(self.sidebar_globale, text="🖨️ Assistente Brother", anchor="w")
        self.btn_brother.pack(fill="x", padx=15, pady=5)

        self.btn_app = ctk.CTkButton(self.sidebar_globale, text="💻 Problemi App GDV BI", anchor="w")
        self.btn_app.pack(fill="x", padx=15, pady=5)

         # AGGIUNTO: Bottone per accedere alla sezione MT
        self.btn_mt = ctk.CTkButton(self.sidebar_globale, text="💰 Anomalie App METODO", anchor="w")
        self.btn_mt.pack(fill="x", padx=15, pady=5)

        self.btn_negozi = ctk.CTkButton(self.sidebar_globale, text="🏬 Anagrafica Negozi", anchor="w")
        self.btn_negozi.pack(fill="x", padx=15, pady=5)

       

        # 2. Contenitore dove inseriremo i moduli alternabili
        self.container_area = ctk.CTkFrame(self, fg_color="transparent")
        self.container_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container_area.grid_columnconfigure(0, weight=1)
        self.container_area.grid_rowconfigure(0, weight=1)


    def mostra_sezione(self, frame_sezione):
        """Nasconde gli altri frame e porta in primo piano quello selezionato."""
        frame_sezione.grid(row=0, column=0, sticky="nsew")
        frame_sezione.tkraise()