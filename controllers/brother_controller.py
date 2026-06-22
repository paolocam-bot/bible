import time
from models.problema import Problema
from views.dialogs import ProblemaDialog

class BrotherController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.problema_corrente = None

        # Configurazione eventi
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
                "Nessun Risultato Brother",
                f"Nessuna procedura trovata nel database Brother per: '{testo_cercato}'.",
                ["Riprova modificando la chiave di ricerca.", "Aggiungi una nuova scheda tecnica se necessario."]
            )

    def aggiungi_nuovo(self):
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Aggiungi Errore Brother")
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
            # Nota: usiamo il metodo corretto del modello
            self.model.aggiungere_problema(nuovo_prob)
            self.inizializza_interfaccia()

    def modifica_selezionato(self):
        if not self.problema_corrente:
            return
            
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Modifica Guasto Brother", self.problema_corrente)
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
        self.view.aggiorna_dettagli("Seleziona una problematica Brother", "Usa la barra superiore o seleziona un guasto dall'indice a sinistra.", [])
        self.inizializza_interfaccia()