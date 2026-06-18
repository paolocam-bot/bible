import os

import customtkinter as ctk

class ProblemaDialog(ctk.CTkToplevel):
    def __init__(self, master, titolo_finestra="Gestione Problema", problema_esistente=None):
        super().__init__(master)
        self.title(titolo_finestra)
        self.geometry("550x600")
        
        # Blocca il focus sulla finestra popup finché non viene chiusa
        self.grab_set() 
        self.risultato = None

        # --- GESTIONE LOGO FINESTRA POPUP ---
        cartella_views = os.path.dirname(os.path.abspath(__file__))
        cartella_progetto = os.path.dirname(cartella_views)
        percorso_logo = os.path.join(cartella_progetto, "data", "app.png")

        try:
            from tkinter import PhotoImage
            # Salviamo l'immagine nell'istanza (self.) per evitare il Garbage Collector
            self.img_icona = PhotoImage(file=percorso_logo)
            # Applichiamo l'icona un attimo dopo l'avvio del popup
            self.after(200, lambda: self.wm_iconphoto(False, self.img_icona))
        except Exception as e:
            print(f"Impossibile caricare il logo nel popup: {e}")

        # --- CAMPI DI INPUT ---
        ctk.CTkLabel(self, text="Titolo Anomalia:", font=ctk.CTkFont(weight="bold")).pack(padx=20, pady=(20, 2), anchor="w")
        self.ent_titolo = ctk.CTkEntry(self, width=500, height=35)
        self.ent_titolo.pack(padx=20, pady=5)

        ctk.CTkLabel(self, text="Parole Chiave (separate da virgola):", font=ctk.CTkFont(weight="bold")).pack(padx=20, pady=(15, 2), anchor="w")
        self.ent_keys = ctk.CTkEntry(self, width=500, height=35, placeholder_text="es. rete, stampante, errore 500")
        self.ent_keys.pack(padx=20, pady=5)

        ctk.CTkLabel(self, text="Descrizione Errore:", font=ctk.CTkFont(weight="bold")).pack(padx=20, pady=(15, 2), anchor="w")
        self.txt_desc = ctk.CTkTextbox(self, width=500, height=80)
        self.txt_desc.pack(padx=20, pady=5)

        ctk.CTkLabel(self, text="Procedure/Soluzioni (una per riga):", font=ctk.CTkFont(weight="bold")).pack(padx=20, pady=(15, 2), anchor="w")
        self.txt_soluzioni = ctk.CTkTextbox(self, width=500, height=150)
        self.txt_soluzioni.pack(padx=20, pady=5)

        # Se passiamo un problema esistente (MODIFICA), precompiliamo i campi
        if problema_esistente:
            self.ent_titolo.insert(0, problema_esistente.titolo)
            self.ent_keys.insert(0, ", ".join(problema_esistente.parole_chiave))
            self.txt_desc.insert("1.0", problema_esistente.descrizione)
            self.txt_soluzioni.insert("1.0", "\n".join(problema_esistente.soluzioni))

        # --- BOTTONI DI CONFERMA ---
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=25)
        
        self.btn_salva = ctk.CTkButton(btn_frame, text="Salva", fg_color="green", hover_color="darkgreen", width=120, command=self.conferma)
        self.btn_salva.pack(side="right", padx=5)
        
        self.btn_annulla = ctk.CTkButton(btn_frame, text="Annulla", fg_color="gray", width=120, command=self.destroy)
        self.btn_annulla.pack(side="right", padx=5)

    def conferma(self):
        # Elaborazione stringhe per ricostruire liste da testi puliti
        soluzioni_lista = [s.strip() for s in self.txt_soluzioni.get("1.0", "end").split("\n") if s.strip()]
        keys_lista = [k.strip() for k in self.ent_keys.get().split(",") if k.strip()]
        
        # Salviamo il dizionario con i dati inseriti dall'utente
        self.risultato = {
            "titolo": self.ent_titolo.get(),
            "parole_chiave": keys_lista,
            "descrizione": self.txt_desc.get("1.0", "end-1c"),
            "soluzioni": soluzioni_lista
        }
        self.destroy() # Chiude la finestra salvando il risultato