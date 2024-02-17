import pygame
import sys
import os
import json
from reload_core.datastore import DataStore, EditorDataStore
from reload_core.config import *
import reload_core.network as network

class ReloadCore():
    def __init__(self, onUpdate, dataStoreClass):
        self.onUpdate = onUpdate
        self.dataStoreClass = dataStoreClass
        self.frame_history = []
        self.frames_passed = 0
        self.editor = None
        self.datastore = None

    def go(self):
        # Initialize Pygame
        pygame.init()
        
        try:
            with open(os.path.join(ARTIFACTS_DIR, 'frame_history.json'), 'r') as f:
                self.frame_history = json.load(f)
            
            with open(os.path.join(ARTIFACTS_DIR, 'editor_state.json'), 'r') as f:
                self.editor = EditorDataStore.parse_raw(f.read())
            
            last_frame = self.frame_history[-1]
            
            # Load the last frame
            self.datastore = DataStore.load(self.dataStoreClass, os.path.join(DATASTORE_DIR, last_frame["name"]))
            
            # Get the number of frames 
            self.frames_passed = last_frame["frame_num"] + 1
            
        except Exception as e:
            print("Error loading datastore")
            print(e)
            
            self.init_clean()
            self.editor = EditorDataStore()
            

        # Set up the display
        screen = pygame.display.set_mode((self.datastore.WIDTH, self.datastore.HEIGHT))

        # Set up the clock
        clock = pygame.time.Clock()
        
        dev_socket = None
        if DEV_MODE:
            dev_socket = network.start_dev_server()
        
        def resume_game(calling_socket):
            self.editor.paused = False
            print("Resuming game")
            print(f"Called from socket {calling_socket.getpeername()}")
            calling_socket.send("Done".encode())

        def cmd_get_frame(calling_socket):
            print("Sending current frame")
            calling_socket.send(str(self.frames_passed).encode())
        
        def cmd_reset_frame(calling_socket):
            print("Resetting frame")
            
            # Delete every frame in frame history
            for i in range(len(self.frame_history)):
                delete_frame(self.frame_history, -1) 
            
            self.init_clean()
            
            calling_socket.send("Done".encode())
        
        cmds = {
            "go": resume_game,
            "frame": cmd_get_frame,
            "reset": cmd_reset_frame,
        }
        
        # Game loop
        while True:
            
            # If we're in dev mode, check for messages from the dev socket
            if DEV_MODE and dev_socket:
                network.update_socket(dev_socket, cmds)
                
            # Set cursor status
            if self.datastore.config.show_cursor:
                pygame.mouse.set_visible(True)
            else:
                pygame.mouse.set_visible(False)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Ctrl D pauses game
                if pygame.key.get_mods() and pygame.KMOD_CTRL and event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                    self.editor.paused = not self.editor.paused
                    print(f"Paused: {self.editor.paused}")
            
            # Core game logic
            self.onUpdate(self.datastore, screen, clock)
            pygame.display.flip()
            clock.tick(FPS) # FPS cap
            
            # FPS counter
            pygame.display.set_caption(f"FPS: {int(clock.get_fps())}")
            keys = pygame.key.get_pressed()

            if pygame.key.get_mods() and pygame.KMOD_CTRL and keys[pygame.K_s]:
                self.datastore.save(os.path.join(ARTIFACTS_DIR, "manual_save.json"))
                print("Manual save")
                
            # Rewind time
            if pygame.key.get_mods() and pygame.KMOD_CTRL and len(self.frame_history) > 1 and keys[pygame.K_z]:
                
                try:
                    self.frames_passed -= 1
                    
                    if self.frames_passed % FRAMES_PER_SAVE == 0:
                        generation = self.frames_passed // FRAMES_PER_SAVE
                        
                        last_frame_name= f"frame_{generation}.json"
                        self.datastore = DataStore.load(self.dataStoreClass, os.path.join(DATASTORE_DIR, last_frame_name))
                        
                        # Delete off the end instead
                        delete_frame(self.frame_history, -1)
                        log_frame_history(self.frame_history, self.frames_passed, last_frame_name)
                        
                        print(f"Reversing to frame {generation}")
                    
                    
                except Exception as e:
                    print("Error rewinding")
                    print(e)
            
            # Store the updated datastore to /artifacts (but only if we're not rewinding!)
            elif not self.editor.paused:
                # Save the frame to /artifacts
                if self.frames_passed % FRAMES_PER_SAVE == 0:
                    # Create frame name
                    self.append_frame()
                
                self.frames_passed += 1
            
            else: 
                # Not moving in either direction, reload the last frame
                generation = self.frames_passed // FRAMES_PER_SAVE - 1
                last_frame_name= f"frame_{generation}.json"
                
                self.datastore = DataStore.load(self.dataStoreClass, os.path.join(DATASTORE_DIR, last_frame_name))
            
            
            # Store editor state to /artifacts
            with open(os.path.join(ARTIFACTS_DIR, 'editor_state.json'), 'w') as f:
                json.dump(self.editor.model_dump(), f)

    def append_frame(self):
        generation = self.frames_passed // FRAMES_PER_SAVE
        frame_name = f"frame_{generation}.json"
        self.datastore.save(os.path.join(DATASTORE_DIR, frame_name))
                    
        self.frame_history.append({
                                "name": frame_name,
                                "frame_num": self.frames_passed 
                            })
                    
        if len(self.frame_history) > FRAME_HISTORY_LIMIT:
            delete_frame(self.frame_history, 0)
        log_frame_history(self.frame_history, self.frames_passed, frame_name)

    def init_clean(self):
        self.datastore = self.dataStoreClass()
        self.datastore.init()
        self.frame_history = []
        self.frames_passed = 0
        
        # Push on a clean frame
        self.append_frame()
        self.frames_passed += 1

            


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
        

            
            
        
        