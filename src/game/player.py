import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from pydantic import BaseModel
import sys

from reload_core.config import *
from .bullet import Bullet
from .constants import GAME_OVER

class Player(GameObject):
    pos: Vector2
    width: int
    height: int
    hp: int = 100
    max_hp: int = 100
    
    alive: bool = True
    
    def move_ip(self, x, y):
        self.pos.x += x
        self.pos.y += y
    
    def draw(self, screen: pygame.Surface, color: tuple):
        if not self.alive:
            return
        
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), 25)
        
        # Draw image assets/smiley.png
        image = pygame.image.load('assets/smiley.png')
        screen.blit(image, (self.pos.x - 25, self.pos.y - 25))
        
        # Draw health bar
        hp_bar_fill = pygame.Rect(self.pos.x - 25, self.pos.y - 40, 50 * (self.hp / self.max_hp), 5)
        pygame.draw.rect(screen, (255, 0, 0), hp_bar_fill)
    
    def update(self, ds: DataStore):
        if self.hp <= 0:
            self.kill(ds)
        
        if not self.alive:
            return
        
        # Move the square
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_ip(-5, 0)
        if keys[pygame.K_RIGHT]:
            self.move_ip(5, 0)
        if keys[pygame.K_UP]:
            self.move_ip(0, -5)
        if keys[pygame.K_DOWN]:
            self.move_ip(0, 5)
            
        # Create bullet on click
        if pygame.mouse.get_pressed()[0]:
            
            mouse_pos = pygame.mouse.get_pos()
            dir = Vector2(x=mouse_pos[0] - ds.player.pos.x, y=mouse_pos[1] - ds.player.pos.y)
            dir = dir.normalize()
            fireVelo = dir * 5
            
            bullet = Bullet(pos=Vector2(x=ds.player.pos.x, y=ds.player.pos.y), x_velocity=fireVelo.x, y_velocity=fireVelo.y)
            ds.bullets.append(bullet)
        
        pass

    def kill(self, ds: DataStore):
        self.alive = False
        ds.game_state = GAME_OVER
    
    def respawn(self, ds: DataStore):
        self.alive = True
        self.hp = 100
        self.pos.x = ds.WIDTH//2
        self.pos.y = ds.HEIGHT//2