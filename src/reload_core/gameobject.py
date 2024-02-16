from pydantic import BaseModel
from typing import Callable

class GameObject(BaseModel):
    data: dict = {}
    onStart: Callable = None
    onUpdate: Callable = None