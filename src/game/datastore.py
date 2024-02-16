import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from pydantic import BaseModel
import sys

from reload_core.config import *
from game.enemy import Enemy
from game.bullet import Bullet
from game.player import Player
from .constants import *
from .ui import UI


class MyDataStore(DataStore):
    player: Player = None
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    
    WHITE: tuple = (255, 255, 255)
    RED: tuple = (255, 0, 0)
    BLACK: tuple = (0, 0, 0)
    YELLOW: tuple = (255, 255, 0)
    BLUE: tuple = (0, 0, 255)
    
    game_state: int = GAME_PLAYING
    ui: UI = UI()
    
    def init(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.config.show_cursor = False
        
        SQUARE_SIZE = 50
        self.player = Player(pos=Vector2(x=self.WIDTH//2, y=self.HEIGHT//2), width=SQUARE_SIZE, height=SQUARE_SIZE)
        pass