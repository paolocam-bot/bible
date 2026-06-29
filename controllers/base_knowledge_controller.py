import time
from models.problema import Problema
from views.dialogs import ProblemaDialog

class BaseKnowledgeController:
    def __init__(self, model, view, titolo_modulo="Problema"):
        self.model = model
        self.view = view
        self.titolo_modulo = titolo_modulo
        
        # Variabile per tracciare quale problema è attualmente selezionato
        self.problema_corrente = None

        # Assegnazione del comando al tasto cerca
        self.view.search_btn.configure(command=self.gestisci_ricerca)
        
        # Registrazione eventi pulsanti CRUD
        self.view.btn_add.configure(command=self.aggiungi_nuovo)
        self.view.btn_edit.configure(command=self.modifica_selezionato)
        self.view.btn_delete.configure(command=self.elimina_selezionato)
        
        # Carica i dati nell'interfaccia all'avvio
        self.inizializza_interfaccia()

    def inizializza_interfaccia(self):
        problemi = self.model.ottieni_tutti()
        self.view.popola_sidebar(problemi, self.mostra_problema_selezionato)

    def mostra_problema_selezionato(self, problema):
        self.problema_corrente = problema
        self.view.aggiorna_dettagli(problema.titolo, problema.descrizione, problema.soluzioni)

    def gestisci_ricerca(self):
        testo_cercato = self.view.ottieni_testo_ricerca()
        risultato = self.model.cerca_problema(testo_cercato)

        if risultato:
            self.mostra_problema_selezionato(risultato)
        else:
            # Sfrutta il titolo del modulo per mostrare un feedback preciso in caso di mancata corrispondenza
            self.view.aggiorna_dettagli(
                f"Nessun risultato per: '{testo_cercato}'", 
                f"Non è stato trovato alcun argomento nel manuale {self.titolo_modulo} corrispondente alla ricerca.", 
                []
            )

    def aggiungi_nuovo(self):
        # Usa il titolo dinamico nel popup
        dialog = ProblemaDialog(self.view.winfo_toplevel(), f"Aggiungi Nuovo {self.titolo_modulo}")
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            nuovo_id = int(time.time())
            nuovo_prob = Problema(
                nuovo_id,
                dialog.risultato["titolo"],
                dialog.risultato["parole_chiave"],
                dialog.risultato["descrizione"],
                dialog.risultato["soluzioni"]
            )
            # Uniformato al metodo standard
            self.model.aggiungi_problema(nuovo_prob)
            self.inizializza_interfaccia()

    def modifica_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un elemento da modificare!")
            return
            
        dialog = ProblemaDialog(self.view.winfo_toplevel(), f"Modifica {self.titolo_modulo}", self.problema_corrente)
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            self.model.modifica_problema(self.problema_corrente.id, dialog.risultato)
            self.view.aggiorna_dettagli(dialog.risultato["titolo"], dialog.risultato["descrizione"], dialog.risultato["soluzioni"])
            self.inizializza_interfaccia()

    def elimina_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un elemento da eliminare!")
            return
            
        self.model.elimina_problema(self.problema_corrente.id)
        self.problema_corrente = None
        self.view.aggiorna_dettagli("Argomento Eliminato", "Seleziona un'altra voce dall'indice.", [])
        self.inizializza_interfaccia()