import pytmx
from pytmx.util_pygame import load_pygame

from pydantic import BaseModel
import numpy as np

class TiledRenderer(BaseModel):
    fname: str 
    
    def render_map(self, surface, tmap_store):
        
        # If tiled_map isnt loaded, load it
        tmap = self.get_tmap(tmap_store)
        
        """Render the map to a pygame surface."""
        for layer in tmap.visible_layers:
            
            if isinstance(layer, pytmx.TiledTileLayer):
                self.render_tile_layer(surface, tmap, layer)

    def get_tmap(self, tmap_store):
        if self.fname not in tmap_store:
            tmap_store[self.fname] = load_pygame(self.fname)
        tmap = tmap_store[self.fname]
        return tmap

    def render_layer_by_name(self, surface, tmap_store, layer_name):
        tmap = self.get_tmap(tmap_store)
        
        """Render a layer by name."""
        try:
            layer = tmap.get_layer_by_name(layer_name)
            if layer:
                self.render_tile_layer(surface, tmap, layer)
        except ValueError:
            print(f'Layer {layer_name} not found')
            
            pass

    def render_tile_layer(self, surface, tmap, layer):
        """Render a tile layer."""
        for x, y, gid, in layer:
            tile = tmap.get_tile_image_by_gid(gid)
            if tile:
                surface.blit(tile, (x * tmap.tilewidth, y * tmap.tileheight))
    
    # Returns 2d array of collidable tiles
    def layer_to_coll_map(self, tmap_store, layer_name):
        tmap = self.get_tmap(tmap_store)
        layer = tmap.get_layer_by_name(layer_name)
        
        coll_map = np.zeros((tmap.width, tmap.height))
        
        for x, y, gid, in layer:
            if gid == 0:
                continue
            
            coll_map[x][y] = 1
        
        return coll_map
        
        