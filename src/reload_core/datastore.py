from pydantic import BaseModel
from pygame import Surface

class DataStore(BaseModel):
    data: dict = {}
    WIDTH: int = 800
    HEIGHT: int = 600
    
    def init(self):
        pass
    
    def save(self):
        with open('artifacts/datastore.json', 'w') as f:
            f.write(self.model_dump_json())
    
    def load(cls, path: str):
        with open(path, 'r') as f:
            return cls.parse_raw(f.read())