import asyncio
import time
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AsyncHandler(FileSystemEventHandler):
    def __init__(self, loop, on_event):
        self.loop = loop
        self.on_event = on_event

    def on_any_event(self, event):
        if event.is_directory:
            return None

        if event.event_type in ('created', 'modified', 'deleted'):
            asyncio.run_coroutine_threadsafe(self.handle_event(event), self.loop)

    async def handle_event(self, event): 
        await self.on_event(event)

def start_observer(loop, paths_to_watch, on_event):
    observers = []
    for path in paths_to_watch:
        event_handler = AsyncHandler(loop=loop, on_event=on_event)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()
        observers.append(observer)
    
    try:
        while True:
            time.sleep(1)
    finally:
        for observer in observers:
            observer.stop()
            observer.join()

async def go(path_to_watch, on_event):
    loop = asyncio.get_running_loop()
    
    # Run the observer in a separate thread
    observer_thread = Thread(target=start_observer, args=(loop, path_to_watch, on_event), daemon=True)
    observer_thread.start()
    
