class NegozioController:
    def __init__(self, model, view, main_controller=None):
        self.model = model
        self.view = view
        self.main_controller = main_controller

        # Collega questo controller alla View
        self.view.imposta_controller(self)

        # Collega l'azione del pulsante Cerca tradizionale
        self.view.search_btn.configure(command=self.esegui_ricerca)
        
        # Carica la lista iniziale dei negozi
        self.mostra_tutti_i_negozi()

    def mostra_tutti_i_negozi(self):
        """Prende tutti i negozi dal modello e li passa alla vista."""
        negozi = self.model.ottieni_tutti()
        self.view.mostra_negozi(negozi)

    def esegui_ricerca(self):
        """Legge il testo della barra di ricerca e filtra i risultati."""
        testo_ricerca = self.view.ottieni_testo_ricerca()
        risultati = self.model.cerca_negozi(testo_ricerca)
        self.view.mostra_negozi(risultati)

    def aggiungi_nuovo_negozio(self, codice_breve, nome, coordinatore, codclifor, descrizione_conto):
        """Richiamato quando l'utente preme 'Aggiungi Negozio' compilando il form."""
        # 1. Salva nel database tramite Modello
        self.model.aggiungi_negozio(codice_breve, nome, coordinatore, codclifor, descrizione_conto)
        
        # 2. Rinfresca la lista a schermo (mostra le schede aggiornate)
        self.esegui_ricerca()
        
        # 3. Notifica il MainController per aggiornare l'OptionMenu del Registro Task
        self._notifica_aggiornamento_tasks()

    def modifica_negozio_esistente(self, codice_breve_target, nuovo_nome, nuovo_coordinatore, nuovo_codclifor, nuova_descrizione):
        """Richiamato quando l'utente salva le modifiche di una scheda negozio."""
        
        # 1. Applica le modifiche nel file JSON tramite il DAO
        self.model.modifica_negozio(
            codice_breve_target=codice_breve_target, 
            nuovo_nome=nuovo_nome, 
            nuovo_coordinatore=nuovo_coordinatore, 
            nuovo_codclifor=nuovo_codclifor, 
            nuova_descrizione=nuova_descrizione
        )
        
        # 2. Aggiorna la grafica della tabella dei negozi
        self.esegui_ricerca()
        
        # 3. Notifica le modifiche al modulo Task per aggiornare i menu a tendina dei negozi
        self._notifica_aggiornamento_tasks()

    def elimina_negozio_esistente(self, codice_breve_target):
        """Richiamato quando l'utente preme il pulsante rosso 'Elimina Negozio'."""
        if hasattr(self.model, "negozi"):
            # Filtra la lista rimuovendo l'oggetto con il codice target
            self.model.negozi = [n for n in self.model.negozi if n.codice_breve != codice_breve_target]
            
            # Forza il salvataggio sul file JSON
            self.model._salva_su_file()
            
            # Aggiorna la UI dei negozi e notifica il registro task
            self.esegui_ricerca()
            self._notifica_aggiornamento_tasks()

    def _notifica_aggiornamento_tasks(self):
        """Se il MainController e la TaskView sono attivi, aggiorna il menu a tendina dei negozi."""
        if self.main_controller:
            # Se la vista delle task possiede il metodo per rigenerare l'OptionMenu dei negozi, lo invochiamo
            if hasattr(self.main_controller, "view_task") and hasattr(self.main_controller.view_task, "aggiorna_opzioni_negozi"):
                self.main_controller.view_task.aggiorna_opzioni_negozi()