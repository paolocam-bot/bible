from models.manuale_base_model import ManualeBaseModel

class ManualeModel(ManualeBaseModel):
    def __init__(self):
        super().__init__(nome_file_json=None) # Usa il default "database_manuale.json"