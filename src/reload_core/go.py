import pygame
import sys
import os
import json
from reload_core.datastore import DataStore, EditorDataStore
from reload_core.config import *

def go(onUpdate, dataStoreClass: DataStore):
    # Initialize Pygame
    pygame.init()
    
    # Try to load the datastore from /artifacts
    frame_history = []
    frames_passed = 0
    editor = None
    
    try:
        with open(os.path.join(ARTIFACTS_DIR, 'frame_history.json'), 'r') as f:
            frame_history = json.load(f)
        
        with open(os.path.join(ARTIFACTS_DIR, 'editor_state.json'), 'r') as f:
            editor = EditorDataStore.parse_raw(f.read())
        
        last_frame = frame_history[-1]
        
        # Load the last frame
        datastore = DataStore.load(dataStoreClass, os.path.join(DATASTORE_DIR, last_frame["name"]))
        
        # Get the number of frames 
        frames_passed = last_frame["frame_num"] + 1
        
    except Exception as e:
        print("Error loading datastore")
        print(e)
        
        datastore = dataStoreClass()
        datastore.init()
        
        editor = EditorDataStore()
        

    # Set up the display
    screen = pygame.display.set_mode((datastore.WIDTH, datastore.HEIGHT))

    # Set up the clock
    clock = pygame.time.Clock()
    
    # Game loop
    while True:
        
        # Set cursor status
        if datastore.config.show_cursor:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Ctrl D pauses game
            if pygame.key.get_mods() and pygame.KMOD_CTRL and event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                editor.paused = not editor.paused
                print(f"Paused: {editor.paused}")
        
        # Core game logic
        onUpdate(datastore, screen, clock)
        pygame.display.flip()
        clock.tick(FPS) # FPS cap
        
        # FPS counter
        pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
        keys = pygame.key.get_pressed()

        if pygame.key.get_mods() and pygame.KMOD_CTRL and keys[pygame.K_s]:
            datastore.save(os.path.join(ARTIFACTS_DIR, "manual_save.json"))
            print("Manual save")
            
        # Rewind time
        if pygame.key.get_mods() and pygame.KMOD_CTRL and len(frame_history) > 1 and keys[pygame.K_z]:
            
            try:
                frames_passed -= 1
                
                if frames_passed % FRAMES_PER_SAVE == 0:
                    generation = frames_passed // FRAMES_PER_SAVE
                    
                    last_frame_name= f"frame_{generation}.json"
                    datastore = DataStore.load(dataStoreClass, os.path.join(DATASTORE_DIR, last_frame_name))
                    
                    # Delete off the end instead
                    delete_frame(frame_history, -1)
                    log_frame_history(frame_history, frames_passed, last_frame_name)
                    
                    print(f"Reversing to frame {generation}")
                
                
            except Exception as e:
                print("Error rewinding")
                print(e)
        
        # Store the updated datastore to /artifacts (but only if we're not rewinding!)
        elif not editor.paused:
            # Save the frame to /artifacts
            if frames_passed % FRAMES_PER_SAVE == 0:
                # Create frame name
                generation = frames_passed // FRAMES_PER_SAVE
                frame_name = f"frame_{generation}.json"
                datastore.save(os.path.join(DATASTORE_DIR, frame_name))
                
                frame_history.append({
                            "name": frame_name,
                            "frame_num": frames_passed 
                        })
                
                if len(frame_history) > FRAME_HISTORY_LIMIT:
                    delete_frame(frame_history, 0)
                log_frame_history(frame_history, frames_passed, frame_name)
            
            frames_passed += 1
        
        else:
            # Not moving in either direction, reload the last frame
            generation = frames_passed // FRAMES_PER_SAVE - 1
            last_frame_name= f"frame_{generation}.json"
            
            datastore = DataStore.load(dataStoreClass, os.path.join(DATASTORE_DIR, last_frame_name))
        
        
        # Store editor state to /artifacts
        with open(os.path.join(ARTIFACTS_DIR, 'editor_state.json'), 'w') as f:
            json.dump(editor.model_dump(), f)


def delete_frame(frame_history, index):
    try:
        path = os.path.join(DATASTORE_DIR, frame_history[index]["name"])
        os.remove(path)
                    
        frame_history.pop(index)
    except Exception as e:
        print("Error saving frame")
        print(e)

def log_frame_history(frame_history, frames_passed, frame_name):
    with open(os.path.join(ARTIFACTS_DIR, 'frame_history.json'), 'w') as f:
        json.dump(frame_history, f)
        

            
            
        
        