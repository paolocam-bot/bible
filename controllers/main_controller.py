from models.manuale_model import ManualeModel
from models.negozio_model import NegozioModel
from models.app_model import AppModel              # Aggiunto
from views.manuale_view import ManualeView
from views.negozio_view import NegozioView
from views.app_view import AppView                  # Aggiunto
from controllers.manuale_controller import ManualeController
from controllers.negozio_controller import NegozioController
from controllers.app_controller import AppController # Aggiunto

class MainController:
    def __init__(self, view):
        self.view = view

        # 1. Inizializza Modulo Zebra (Modello + Vista inserita nel container + Controller)
        self.model_zebra = ManualeModel()
        self.view_zebra = ManualeView(self.view.container_area)
        self.ctrl_zebra = ManualeController(self.model_zebra, self.view_zebra)

        # 2. Inizializza Modulo Problemi App (QUESTO MANCAVA!)
        self.model_app = AppModel()
        self.view_app = AppView(self.view.container_area)
        self.ctrl_app = AppController(self.model_app, self.view_app)

        # 3. Inizializza Modulo Negozi (Modello + Vista inserita nel container + Controller)
        self.model_negozi = NegozioModel()
        self.view_negozi = NegozioView(self.view.container_area)
        self.ctrl_negozi = NegozioController(self.model_negozi, self.view_negozi)

        # 4. Collega i bottoni del menu alle rispettive funzioni di scambio
        self.view.btn_zebra.configure(command=lambda: self.view.mostra_sezione(self.view_zebra))
        self.view.btn_app.configure(command=lambda: self.view.mostra_sezione(self.view_app)) # Ora self.view_app esiste!
        self.view.btn_negozi.configure(command=lambda: self.view.mostra_sezione(self.view_negozi))

        # Sezione iniziale di default all'avvio
        self.view.mostra_sezione(self.view_zebra)