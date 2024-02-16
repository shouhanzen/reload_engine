import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from pydantic import BaseModel
import sys

from reload_core.config import *
from .bullet import Bullet

class Enemy(GameObject):
    pos: Vector2
    x_velocity: float
    y_velocity: float
    
    def update(self, ds: DataStore):
        self.pos.x += self.x_velocity
        self.pos.y += self.y_velocity
        
        # Move towards player
        player = ds.player
        dir = Vector2(x=player.pos.x - self.pos.x, y=player.pos.y - self.pos.y)
        dir = dir.normalize()
        self.x_velocity = dir.x * 1
        self.y_velocity = dir.y * 1
    
    def draw(self, screen: pygame.Surface, color: tuple):
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), 5)
    
    def manage(ds: DataStore, screen: pygame.Surface):
        # Create enemy on right click
        if pygame.mouse.get_pressed()[2]:
            mouse_pos = pygame.mouse.get_pos()
            enemy = Enemy(pos=Vector2(x=mouse_pos[0], y=mouse_pos[1]), x_velocity=0, y_velocity=0)
            ds.enemies.append(enemy)
        
        for enemy in ds.enemies:
            enemy.update(ds)
            enemy.draw(screen, ds.BLACK)