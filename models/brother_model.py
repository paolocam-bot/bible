from models.manuale_base_model import ManualeBaseModel

class BrotherModel(ManualeBaseModel):
    def __init__(self):
        super().__init__(nome_file_json="database_brother.json")