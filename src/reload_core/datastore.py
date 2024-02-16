from pydantic import BaseModel
from pygame import Surface

class Config(BaseModel):
    show_cursor: bool = True

class DataStore(BaseModel):
    data: dict = {}
    WIDTH: int = 800
    HEIGHT: int = 600
    config: Config = Config()
    
    def init(self):
        pass
    
    def save(self, path: str):
        with open(path, 'w') as f:
            f.write(self.model_dump_json())
    
    def load(cls, path: str):
        with open(path, 'r') as f:
            return cls.parse_raw(f.read())
        
class EditorDataStore(BaseModel):
    paused: bool = False