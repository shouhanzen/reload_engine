# Run main.py

import os
import sys
import subprocess
import editor.filewatcher
import asyncio

game = None
respawn_requested = False

async def start_game():
    new_game = await asyncio.create_subprocess_exec(
        sys.executable, 'src/game.py',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    
    return new_game

# Make a filewatcher for the src directory
# This will run the game.py file when any file in the src directory changes
async def on_file_changed(event):
    global game, respawn_requested
    
    respawn_requested = True
    
    print(f'File changed: {event.src_path}')

 
async def main():
    global game, respawn_requested
    await editor.filewatcher.go('src', on_file_changed)
    
    # Wait for the game to finish
    while True: 
        await asyncio.sleep(1)
        
        has_returned = game is not None and game.returncode is not None
        if respawn_requested or game is None or has_returned:
            respawn_requested = False 
            
            try:
                if game is not None:
                    game.kill() 
                game = await start_game()
            except Exception as e:
                print(f'Error: {e}')
                game = None
                continue
                

if __name__ == '__main__':
    asyncio.run(main()) 