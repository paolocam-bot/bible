from models.manuale_base_model import ManualeBaseModel

class AppModel(ManualeBaseModel):
    def __init__(self):
        super().__init__(nome_file_json="problemi_app.json")