from models.manuale_model import ManualeModel
from models.negozio_model import NegozioModel
from models.app_model import AppModel              
from views.manuale_view import ManualeView
from views.negozio_view import NegozioView
from views.app_view import AppView                  
from controllers.manuale_controller import ManualeController
from controllers.negozio_controller import NegozioController
from controllers.app_controller import AppController 

# Import dei moduli MT (Verifica che i file si chiamino esattamente così)
from models.mt_model import MTModel
from views.mt_view import MTView
from controllers.mt_controller import MTController

class MainController:
    def __init__(self, view):
        self.view = view

        # 1. Inizializza Modulo Zebra (Modello + Vista inserita nel container + Controller)
        self.model_zebra = ManualeModel()
        self.view_zebra = ManualeView(self.view.container_area)
        self.ctrl_zebra = ManualeController(self.model_zebra, self.view_zebra)

        # 2. Inizializza Modulo Problemi App
        self.model_app = AppModel()
        self.view_app = AppView(self.view.container_area)
        self.ctrl_app = AppController(self.model_app, self.view_app)

        # 3. Inizializza Modulo Negozi (Modello + Vista inserita nel container + Controller)
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi)

        # 4. Inizializza Modulo MT (NUOVO!)
        self.model_mt = MTModel()
        self.view_mt = MTView(self.view.container_area)
        self.ctrl_mt = MTController(self.model_mt, self.view_mt)

        # 5. Collega i bottoni del menu alle rispettive funzioni di scambio
        self.view.btn_zebra.configure(command=lambda: self.view.mostra_sezione(self.view_zebra))
        self.view.btn_app.configure(command=lambda: self.view.mostra_sezione(self.view_app)) 
        self.view.btn_negozi.configure(command=lambda: self.view.mostra_sezione(self.view_negozi))
        
        # Collega il bottone per l'applicazione MT (Assicurati che self.view.btn_mt esista nella tua Sidebar/Menu principale)
        if hasattr(self.view, 'btn_mt'):
            self.view.btn_mt.configure(command=lambda: self.view.mostra_sezione(self.view_mt))

        self.view.mostra_sezione(self.view_zebra)