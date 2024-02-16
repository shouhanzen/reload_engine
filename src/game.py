import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from pydantic import BaseModel
import sys

from reload_core.config import *

class Square(GameObject):
    pos: Vector2
    width: int
    height: int
    
    def move_ip(self, x, y):
        self.pos.x += x
        self.pos.y += y
    
    def draw(self, screen: pygame.Surface, color: tuple):
        pyRect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        # pygame.draw.rect(screen, color, pyRect)
        
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), 25)
        
class Bullet(GameObject):
    pos: Vector2
    x_velocity: float
    y_velocity: float
    
    def update(self, bounds: tuple=(800, 600)):
        self.pos.x += self.x_velocity
        self.pos.y += self.y_velocity
    
    def draw(self, screen: pygame.Surface, color: tuple):
        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), 5)
    
    pass

class MyDataStore(DataStore):
    square: Square = None
    bullets: list[Bullet] = []
    WHITE: tuple = (255, 255, 255)
    RED: tuple = (255, 0, 0)
    BLACK: tuple = (0, 0, 0)
    YELLOW: tuple = (255, 255, 0)
    BLUE: tuple = (0, 0, 255)
    
    def init(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.config.show_cursor = False
        
        SQUARE_SIZE = 50
        self.square = Square(pos=Vector2(x=self.WIDTH//2, y=self.HEIGHT//2), width=SQUARE_SIZE, height=SQUARE_SIZE)
        pass

def onUpdate(datastore: MyDataStore, screen: pygame.Surface, clock: pygame.time.Clock):
    square = datastore.square
    WIDTH = datastore.WIDTH
    HEIGHT = datastore.HEIGHT

    # Fill the screen with white
    # screen.fill(datastore.WHITE)
    screen.fill(datastore.BLUE)

    # Draw the square
    square.draw(screen, datastore.RED)
    
    # Draw the bullets
    to_destroy = []
    for bullet in datastore.bullets:
        bullet.update()
        bullet.draw(screen, datastore.WHITE)
        
        if bullet.pos.x < 0 or bullet.pos.x > WIDTH or bullet.pos.y < 0 or bullet.pos.y > HEIGHT:
            to_destroy.append(bullet)
    
    for bullet in to_destroy:
        datastore.bullets.remove(bullet)
    
    # Draw a cursor at the mouse position
    pygame.draw.circle(screen, datastore.YELLOW, pygame.mouse.get_pos(), 5)

    # Move the square
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square.move_ip(-5, 0)
    if keys[pygame.K_RIGHT]:
        square.move_ip(5, 0)
    if keys[pygame.K_UP]:
        square.move_ip(0, -5)
    if keys[pygame.K_DOWN]:
        square.move_ip(0, 5)
        
    # Create bullet on click
    if pygame.mouse.get_pressed()[0]:
        
        mouse_pos = pygame.mouse.get_pos()
        dir = Vector2(x=mouse_pos[0] - square.pos.x, y=mouse_pos[1] - square.pos.y)
        dir = dir.normalize()
        fireVelo = dir * 5
        
        bullet = Bullet(pos=Vector2(x=square.pos.x, y=square.pos.y), x_velocity=fireVelo.x, y_velocity=fireVelo.y)
        datastore.bullets.append(bullet)
    

reload_core.go(onUpdate=onUpdate,dataStoreClass=MyDataStore)