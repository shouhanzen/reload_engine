import reload_core
import pygame
from reload_core.datastore import DataStore
from reload_core.types import GameObject, Vector2
from reload_core.go import ReloadCore
from pydantic import BaseModel
import sys
import numpy as np

from reload_core.config import *
from game.enemy import Enemy
from game.bullet import Bullet
from game.player import Player
from game.datastore import MyDataStore
from game.constants import *

tmap_store = {
}

def onUpdate(ds: MyDataStore, screen: pygame.Surface, clock: pygame.time.Clock):
    player = ds.player
    WIDTH = ds.WIDTH
    HEIGHT = ds.HEIGHT

    # Fill the screen with white
    # screen.fill(datastore.WHITE)
    screen.fill(ds.ORANGE)
    
    # Draw ground
    ds.level_tmap.render_layer_by_name(screen, tmap_store, 'ground')

    # Draw the square
    player.draw(screen, ds.YELLOW)
    player.update(ds, screen=screen, tmap_store=tmap_store)
    
    Bullet.manage(ds, screen)
    Enemy.manage(ds, screen)
    
    # Draw overlay
    ds.level_tmap.render_layer_by_name(screen, tmap_store, 'trees')
    ds.level_tmap.render_layer_by_name(screen, tmap_store, 'coll')
    
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
        

    


reloader = ReloadCore(onUpdate=onUpdate,dataStoreClass=MyDataStore)
reloader.go()