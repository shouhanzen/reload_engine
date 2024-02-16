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
from game.datastore import MyDataStore
from game.constants import *

def onUpdate(ds: MyDataStore, screen: pygame.Surface, clock: pygame.time.Clock):
    player = ds.player
    WIDTH = ds.WIDTH
    HEIGHT = ds.HEIGHT

    # Fill the screen with white
    # screen.fill(datastore.WHITE)
    screen.fill(ds.BLUE)

    # Draw the square
    player.draw(screen, ds.YELLOW)
    player.update(ds)
    
    Bullet.manage(ds, screen)
    Enemy.manage(ds, screen)
    
    # Draw a cursor at the mouse position
    pygame.draw.circle(screen, ds.YELLOW, pygame.mouse.get_pos(), 5)
    
    # Draw UI
    ds.ui.onUpdate(ds, screen)
    
    # Calculate physics between bullets and enemies
    for bullet in ds.bullets:
        for enemy in ds.enemies:
            if (bullet.pos.x - enemy.pos.x)**2 + (bullet.pos.y - enemy.pos.y)**2 < 25**2:
                ds.bullets.remove(bullet)
                ds.enemies.remove(enemy)
                break
    
    # If enemies hit player, destroy enemy and hurt player
    for enemy in ds.enemies:
        if (player.pos.x - enemy.pos.x)**2 + (player.pos.y - enemy.pos.y)**2 < 25**2:
            ds.enemies.remove(enemy)
            player.hp -= 10
            break


reload_core.go(onUpdate=onUpdate,dataStoreClass=MyDataStore)