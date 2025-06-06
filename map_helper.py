from pathlib import Path
from typing import List, Tuple
import pygame
import json
import os

def load_tileset_and_metadata(image_path: Path, tile_size: int) -> Tuple[List[pygame.Surface], dict, int]:
    image = pygame.image.load(str(image_path)).convert_alpha()
    cols  = image.get_width()  // tile_size
    rows  = image.get_height() // tile_size
    tiles: List[pygame.Surface] = []
    for row in range(rows):
        for col in range(cols):
            rect = pygame.Rect(col * tile_size, row * tile_size, tile_size, tile_size)
            tiles.append(image.subsurface(rect).copy())

    # Load metadata if available
    meta_path = Path(image_path).with_suffix(".json")
    metadata = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r") as f:
            metadata = json.load(f)
            metadata = {int(k): v for k, v in metadata.items()}  # Ensure keys are ints
    return tiles, metadata, cols

def blank_layer(w: int, h: int) -> List[List[int]]:
    return [[-1 for _ in range(w)] for _ in range(h)]

def fill_layer(w: int, h: int, tileid: int) -> List[List[int]]:
    return [[tileid for _ in range(w)] for _ in range(h)]

def save_map(path: Path,
             layers: List[List[List[int]]],
             map_width: int,
             map_height: int,
             tile_size: int,
             tilesets: list):
    out = {
        "tile_size":  tile_size,
        "map_width":   map_width,
        "map_height":  map_height,
        "tilesets": tilesets,
        "layers":  layers
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"Saved → {path}")

def load_map(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)