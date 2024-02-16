import pygame
import sys
from reload_core.datastore import DataStore

def go(onUpdate, dataStoreClass: DataStore):
    # Initialize Pygame
    pygame.init()
    
    # Try to load the datastore from /artifacts
    try:
        datastore = DataStore.load(dataStoreClass, 'artifacts/datastore.json')
    except Exception as e:
        print("Error loading datastore from /artifacts")
        print(e)
        
        datastore = dataStoreClass()
        datastore.init()

    # Set up the display
    screen = pygame.display.set_mode((datastore.WIDTH, datastore.HEIGHT))

    # Set up the clock
    clock = pygame.time.Clock()

    # Game loop
    while True:
        onUpdate(datastore, screen, clock)
        
        # Store the updated datastore to /artifacts
        datastore.save()