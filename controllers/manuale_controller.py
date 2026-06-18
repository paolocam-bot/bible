import time                                # Per generare gli ID univoci con time.time()
from models.problema import Problema       # Per istanziare il nuovo problema
from views.dialogs import ProblemaDialog  # Per aprire la finestra di input

class ManualeController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # FONDAMENTALE: Traccia il problema attualmente selezionato per Modifica/Elimina
        self.problema_corrente = None

        # Assegnazione del comando al widget della barra di ricerca
        self.view.search_btn.configure(command=self.gestisci_ricerca)
        
        # Registrazione eventi sui pulsanti CRUD del manuale
        self.view.btn_add.configure(command=self.aggiungi_nuovo)
        self.view.btn_edit.configure(command=self.modifica_selezionato)
        self.view.btn_delete.configure(command=self.elimina_selezionato)
        
        # Inizializzazione dati grafici
        self.inizializza_interfaccia()

    def inizializza_interfaccia(self):
        problemi = self.model.ottieni_tutti()
        self.view.popola_sidebar(problemi, self.mostra_problema_selezionato)

    def mostra_problema_selezionato(self, problema):
        # Memorizza il riferimento al problema cliccato
        self.problema_corrente = problema 
        self.view.aggiorna_dettagli(
            problema.titolo, 
            problema.descrizione, 
            problema.soluzioni
        )

    def gestisci_ricerca(self):
        testo_cercato = self.view.ottieni_testo_ricerca()
        risultato = self.model.cerca_problema(testo_cercato)

        if risultato:
            self.mostra_problema_selezionato(risultato)
        else:
            self.problema_corrente = None
            self.view.aggiorna_dettagli(
                "Nessuna corrispondenza",
                f"Nessuna soluzione trovata nel manuale per: '{testo_cercato}'.",
                [
                    "Riformula la ricerca (es. 'calibrazione', 'led rosso').",
                    "Naviga l'indice a sinistra per trovare l'argomento correlato."
                ]
            )

    # Gestione apertura popup per nuovo inserimento
    def aggiungi_nuovo(self):
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Aggiungi Nuovo Argomento Manuale")
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            nuovo_id = int(time.time())
            nuovo_prob = Problema(
                id=nuovo_id,
                titolo=dialog.risultato["titolo"],
                parole_chiave=dialog.risultato["parole_chiave"],
                descrizione=dialog.risultato["descrizione"],
                soluzioni=dialog.risultato["soluzioni"]
            )
            self.model.aggiungi_problema(nuovo_prob)
            self.inizializza_interfaccia()

    # Gestione apertura popup per modifica
    def modifica_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un argomento da modificare!")
            return
            
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Modifica Argomento Manuale", self.problema_corrente)
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            self.model.modifica_problema(self.problema_corrente.id, dialog.risultato)
            self.view.aggiorna_dettagli(dialog.risultato["titolo"], dialog.risultato["descrizione"], dialog.risultato["soluzioni"])
            self.inizializza_interfaccia()

    # Gestione cancellazione argomenti
    def elimina_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un argomento da eliminare!")
            return
            
        self.model.elimina_problema(self.problema_corrente.id)
        self.problema_corrente = None
        
        # Reset dei dettagli visivi
        self.view.aggiorna_dettagli("Seleziona un argomento", "Usa la barra superiore o seleziona una voce dall'indice.", [])
        self.inizializza_interfaccia()