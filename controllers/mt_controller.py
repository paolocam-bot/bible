import time
from models.problema import Problema
from views.dialogs import ProblemaDialog

class MTController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.problema_corrente = None

        # Setup Eventi
        self.view.search_btn.configure(command=self.gestisci_ricerca)
        self.view.btn_add.configure(command=self.aggiungi_nuovo)
        self.view.btn_edit.configure(command=self.modifica_selezionato)
        self.view.btn_delete.configure(command=self.elimina_selezionato)
        
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
            self.problema_corrente = None
            self.view.aggiorna_dettagli(
                "Nessun Risultato in MT",
                f"Nessuna corrispondenza per la chiave: '{testo_cercato}'.",
                ["Verifica i termini cercati.", "Crea un nuovo ticket se l'errore è inedito."]
            )

    def aggiungi_nuovo(self):
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Aggiungi Errore App MT")
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
            self.model.aggiungi_problema(nuovo_prob)
            self.inizializza_interfaccia()

    def modifica_selezionato(self):
        if not self.problema_corrente:
            return
            
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Modifica Segnalazione MT", self.problema_corrente)
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            self.model.modifica_problema(self.problema_corrente.id, dialog.risultato)
            self.view.aggiorna_dettagli(dialog.risultato["titolo"], dialog.risultato["descrizione"], dialog.risultato["soluzioni"])
            self.inizializza_interfaccia()

    def elimina_selezionato(self):
        if not self.problema_corrente:
            return
        self.model.elimina_problema(self.problema_corrente.id)
        self.problema_corrente = None
        self.view.aggiorna_dettagli("Seleziona una segnalazione MT", "Usa l'indice o la barra di ricerca per visualizzare le soluzioni di MT.", [])
        self.inizializza_interfaccia()