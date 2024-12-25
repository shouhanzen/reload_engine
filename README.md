# Reload Engine

A powerful game development engine that features automatic state saving and live code reloading capabilities, making game development faster and more iterative.

## Features

- **Frame-by-Frame State Saving**: Automatically saves game states at configurable intervals
- **Time Control**:
  - `Ctrl + D`: Pause/Unpause the game
  - `Ctrl + Z`: Rewind to previous states
  - `Ctrl + S`: Create manual save states
- **Live Code Reloading**: Modify code while the game is running and see changes instantly
- **Development Mode**: Special dev mode with additional debugging capabilities

## Project Structure

```
reload_engine/
├── src/
│   ├── game.py           # Main game entry point
│   ├── overseer.py       # File watcher for live reloading
│   └── reload_core/      # Core engine components
│       ├── go.py         # Main game loop and time control
│       └── datastore.py  # State management
├── artifacts/
│   └── frames/          # Directory for saved game states
```

## Getting Started

1. Run the game:
   ```bash
   python src/game.py
   ```

2. Start the overseer process for live reloading:
   ```bash
   python overseer.py
   ```

## Controls

- **Game Controls**:
  - `Ctrl + D`: Pause/Unpause
  - `Ctrl + Z`: Rewind time (requires saved frames)
  - `Ctrl + S`: Create manual save

## Development

The engine saves game states every frame (configurable via `FRAMES_PER_SAVE`), allowing you to:
- Rewind to previous states during development
- Make code changes while the game is running
- Instantly see your changes without restarting

The overseer process watches for file changes and automatically triggers reloads while maintaining the current game state.

## Dependencies

- Python 3.x
- Pygame
