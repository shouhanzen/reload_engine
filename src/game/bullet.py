import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from pydantic import BaseModel
import sys

from reload_core.config import *

class Bullet(GameObject):
    pos: Vector2
    x_velocity: float
    y_velocity: float
    
    def update(self, bounds: tuple=(800, 600)):
        self.pos.x += self.x_velocity
        self.pos.y += self.y_velocity
    
    def draw(self, screen: pygame.Surface, color: tuple):
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), 5)
        
        # Draw bullet trail
        delta=3
        ptr = self.pos + Vector2(x=0, y=0)
        
        for i in range(2):
            pygame.draw.circle(screen, color, (ptr.x, ptr.y), 3)
            ptr.x -= delta * self.x_velocity
            ptr.y -= delta * self.y_velocity
    
    def manage(ds: DataStore, screen: pygame.Surface):
        # Draw the bullets
        to_destroy = []
        for bullet in ds.bullets:
            bullet.update()
            bullet.draw(screen, ds.WHITE)
            
            if bullet.pos.x < 0 or bullet.pos.x > ds.WIDTH or bullet.pos.y < 0 or bullet.pos.y > ds.HEIGHT:
                to_destroy.append(bullet)
        
        for bullet in to_destroy:
            ds.bullets.remove(bullet)