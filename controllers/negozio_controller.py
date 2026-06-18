class NegozioController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Collega l'azione del pulsante Cerca
        self.view.search_btn.configure(command=self.esegui_ricerca)
        
        # Mostra tutti i negozi al primo avvio
        self.mostra_tutti_i_negozi()

    def mostra_tutti_i_negozi(self):
        negozi = self.model.ottieni_tutti()
        self.view.mostra_negozi(negozi)

    def esegui_ricerca(self):
        query = self.view.ottieni_testo_ricerca()
        risultati = self.model.cerca_negozi(query)
        self.view.mostra_negozi(risultati)