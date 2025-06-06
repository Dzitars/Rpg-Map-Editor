from pathlib import Path
from typing import List, Tuple
import pygame
import json

def load_tileset(image_path: Path, tile_size: int) -> Tuple[List[pygame.Surface], int]:
    image = pygame.image.load(str(image_path)).convert_alpha()
    cols  = image.get_width()  // tile_size
    rows  = image.get_height() // tile_size
    tiles: List[pygame.Surface] = []
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            tiles.append(image.subsurface(rect).copy())
    return tiles, cols

def blank_layer(w: int, h: int) -> List[List[int]]:
    return [[-1 for _ in range(w)] for _ in range(h)]

def fill_layer(w: int, h: int, tileid: int) -> List[List[int]]:
    return [[tileid for _ in range(w)] for _ in range(h)]

def save_map(path: Path,
             ground: List[List[int]],
             overlay: List[List[int]],
             map_width: int,
             map_height: int,
             tile_size: int,
             ground_ts: str,
             overlay_ts: str):
    out = {
        "tile_size":  tile_size,
        "map_width":   map_width,
        "map_height":  map_height,
        "ground_tileset":     ground_ts,
        "overlay_tileset":    overlay_ts,
        "ground_data":  ground,
        "overlay_data": overlay,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Saved → {path}")

def load_map(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)