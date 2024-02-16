from pydantic import BaseModel
from reload_core.types import Vector2

class Circle2D(BaseModel):
    p: Vector2
    r: float