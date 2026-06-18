class Negozio:
    """Rappresenta l'entità anagrafica di un singolo negozio."""
    def __init__(self, codice_breve, nome, coordinatore, codclifor, descrizione_conto):
        self.codice_breve = codice_breve
        self.nome = nome
        self.coordinatore = coordinatore
        self.codclifor = codclifor
        self.descrizione_conto = descrizione_conto