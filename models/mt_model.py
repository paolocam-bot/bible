from models.manuale_base_model import ManualeBaseModel

class MTModel(ManualeBaseModel):
    def __init__(self):
        super().__init__(nome_file_json="database_mt.json")