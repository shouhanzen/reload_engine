from pydantic import BaseModel
from typing import Callable

class GameObject(BaseModel):
    pass

class Vector2i(BaseModel):
    x: int
    y: int

class Vector2(BaseModel):
    x: float
    y: float
    
    def __add__(self, other):
        return Vector2(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other):
        return Vector2(x=self.x - other.x, y=self.y - other.y)
    
    def __mul__(self, factor):
        return Vector2(x=self.x*factor, y=self.y*factor)
    
    def normalize(self):
        x = self.x
        y = self.y
        
        magnitude = (x**2 + y**2)**0.5
        if magnitude == 0:
            return Vector2(x=0, y=0)
        else:
            return Vector2(x=x/magnitude, y=y/magnitude)
    
    def assign(self, other):
        self.x = other.x
        self.y = other.y
    
    def dot(self, other):
        return self.x*other.x + self.y*other.y