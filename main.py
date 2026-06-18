import os
import sys

# Mantiene i percorsi corretti per Windows
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from views.main_view import MainView
from controllers.main_controller import MainController

def main():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Avvia la finestra contenitore principale
    root_view = MainView()
    
    # Il controllore centrale unisce e attiva le sezioni
    app_controller = MainController(root_view)
    
    root_view.mainloop()

if __name__ == "__main__":
    main()