import time                                # Per generare gli ID univoci con time.time()
from models.problema import Problema       # Per istanziare il nuovo problema
from views.dialogs import ProblemaDialog  # Per aprire la finestra di input

class AppController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
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
        # FONDAMENTALE: Salva il riferimento al problema cliccato per Modifica/Elimina!
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
                "Nessuna corrispondenza software",
                f"Nessuna procedura censita per la chiave: '{testo_cercato}'.",
                [
                    "Verifica la sintassi (es. database, rete, crash).",
                    "Scorri manualmente l'elenco dei ticket applicativi a sinistra."
                ]
            )

    def aggiungi_nuovo(self):
        # winfo_toplevel() trova la finestra principale a cui agganciare il popup modale
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Aggiungi Nuovo Problema Applicativo")
        self.view.wait_window(dialog) # Ferma l'esecuzione finché il popup non si chiude
        
        if dialog.risultato:
            # Generiamo un ID univoco usando il timestamp attuale
            nuovo_id = int(time.time())
            
            nuovo_prob = Problema(
                id=nuovo_id,
                titolo=dialog.risultato["titolo"],
                parole_chiave=dialog.risultato["parole_chiave"],
                descrizione=dialog.risultato["descrizione"],
                soluzioni=dialog.risultato["soluzioni"]
            )
            
            # Salva nel JSON tramite modello e rinfresca la sidebar
            self.model.aggiungi_problema(nuovo_prob)
            self.inizializza_interfaccia()

    def modifica_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un problema da modificare!")
            return
            
        # Passiamo il problema_corrente al popup per precompilare le caselle di testo
        dialog = ProblemaDialog(self.view.winfo_toplevel(), "Modifica Problema Esistente", self.problema_corrente)
        self.view.wait_window(dialog)
        
        if dialog.risultato:
            # Mandiamo i dati aggiornati al modello
            self.model.modifica_problema(self.problema_corrente.id, dialog.risultato)
            
            # Aggiorniamo la vista di dettaglio centrale e la sidebar
            self.view.aggiorna_dettagli(dialog.risultato["titolo"], dialog.risultato["descrizione"], dialog.risultato["soluzioni"])
            self.inizializza_interfaccia()

    def elimina_selezionato(self):
        if not self.problema_corrente:
            print("Seleziona prima un problema da eliminare!")
            return
            
        self.model.elimina_problema(self.problema_corrente.id)
        self.problema_corrente = None
        
        # Reset interfaccia
        self.view.aggiorna_dettagli("Seleziona una problematica", "Usa la barra di ricerca o seleziona un ticket dall'indice software.", [])
        self.inizializza_interfaccia()