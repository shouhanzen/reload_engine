import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.gameobject import GameObject
from pydantic import BaseModel
import sys

class Square(BaseModel):
    x: int
    y: int
    width: int
    height: int
    
    def move_ip(self, x, y):
        self.x += x
        self.y += y

class MyDataStore(DataStore):
    square: Square = None
    WHITE: tuple = (255, 255, 255)
    RED: tuple = (255, 0, 0)
    BLACK: tuple = (0, 0, 0)
    
    def init(self):
        self.WIDTH, self.HEIGHT = 800, 600
        
        SQUARE_SIZE = 50
        self.square = Square(x=self.WIDTH // 2, y=self.HEIGHT // 2, width=SQUARE_SIZE, height=SQUARE_SIZE)
        pass

def onUpdate(datastore: MyDataStore, screen: pygame.Surface, clock: pygame.time.Clock):
    square = datastore.square
    WIDTH = datastore.WIDTH
    HEIGHT = datastore.HEIGHT
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with white
    # screen.fill(datastore.WHITE)
    screen.fill(datastore.BLACK)

    pyRect = pygame.Rect(square.x, square.y, square.width, square.height)
    pygame.draw.rect(screen, datastore.RED, pyRect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

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
    
    

reload_core.go(onUpdate=onUpdate,dataStoreClass=MyDataStore)