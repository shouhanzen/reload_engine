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

class UI(BaseModel):
    
    def onUpdate(self, ds: DataStore, screen: pygame.Surface):
        # Game over button
        if ds.game_state == GAME_OVER:
            font = pygame.font.Font(None, 36)
            text = font.render("Game Over", True, (255, 255, 255))
            text_rect = text.get_rect(center=(ds.WIDTH//2, ds.HEIGHT//2))
            screen.blit(text, text_rect)
            
            # Restart button
            font = pygame.font.Font(None, 36)
            text = font.render("Restart", True, (255, 255, 255))
            text_rect = text.get_rect(center=(ds.WIDTH//2, ds.HEIGHT//2 + 50))
            screen.blit(text, text_rect)