# Run main.py

import os
import sys
import subprocess
import editor.filewatcher
import asyncio

game = None
respawn_requested = False

async def start_game():
    # Open files for writing stdout and stderr and get their file descriptors
    with open('game_stdout.log', 'wb') as stdout_file, open('game_stderr.log', 'wb') as stderr_file:
        stdout_fd = stdout_file.fileno()
        stderr_fd = stderr_file.fileno()
        
        # Duplicate the file descriptors to keep them open
        stdout_fd = os.dup(stdout_fd)
        stderr_fd = os.dup(stderr_fd)
    
    new_game = await asyncio.create_subprocess_exec(
        sys.executable, '-u', 'src/game.py',
        stdin=subprocess.PIPE,  # Pass the stdin file descriptor
        stdout=stdout_fd,  # Use the file descriptor
        stderr=stderr_fd)  # Use the file descriptor
    
    # It's important to close the duplicated file descriptors to avoid leaks
    os.close(stdout_fd)
    os.close(stderr_fd)
    
    # Send a message to the game
    new_game.stdin.write(b'Hello, game!\n')

    return new_game

# Make a filewatcher for the src directory
# This will run the game.py file when any file in the src directory changes
async def on_file_changed(event):
    global game, respawn_requested
    respawn_requested = True

 
async def main():
    global game, respawn_requested
    await editor.filewatcher.go(['src', 'assets'], on_file_changed)
    
    # Wait for the game to finish
    while True: 
        await asyncio.sleep(1)
        # has_returned = game is not None and game.returncode is not None
        
        if respawn_requested or game is None:
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