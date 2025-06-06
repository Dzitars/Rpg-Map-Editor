from collections import deque
from map_helper import *
from typing import List

# ─────────────────────────────────────────────────
# CONFIGURATION CONSTANTS
# ─────────────────────────────────────────────
APP_TITLE        = "Tile Map Editor"
PALETTE_ROWS     = 3
SCREEN_BG        = (30, 30, 30)
GRID_COLOR       = (80, 80, 80)
HIGHLIGHT_COL    = (255, 255, 0)
PALETTE_BG       = (50, 50, 50)
FONT_COLOR       = (255,255,255)
EDITOR_SIZE      = (1280, 720)
LEGEND_FONT      = "consolas"
LEGEND_FONT_SIZE = 16

KEY_SWITCH_LAYER = pygame.K_TAB
KEY_TOGGLE_GRID  = pygame.K_g
KEY_SAVE_MAP     = pygame.K_s
KEY_TOGGLE_HELP  = pygame.K_h
KEY_FILL         = pygame.K_f
KEY_CLEAR        = pygame.K_c
KEY_EDIT_META    = pygame.K_m
KEY_NUM_UP       = [pygame.K_KP_PLUS, pygame.K_PLUS]
KEY_NUM_DOWN     = [pygame.K_KP_PLUS, pygame.K_MINUS]

class MapEditor:
    def __init__(self, map_data, map_file: Path):
        pygame.init()
        self.screen = pygame.display.set_mode(EDITOR_SIZE)
        pygame.display.set_caption(APP_TITLE)

        self.clock = pygame.time.Clock()
        self.legend_font = pygame.font.SysFont(LEGEND_FONT, LEGEND_FONT_SIZE)
        self.tile_size = map_data["tile_size"]
        self.map_w = map_data["map_width"]
        self.map_h = map_data["map_height"]

        self.layer_data = map_data["layers"]

        self.tilesets: List[List[pygame.Surface]] = []
        self.tileset_tpr: List[int] = []
        for val in map_data["tilesets"]:
            tileset, tpr = load_tileset(val, self.tile_size)
            self.tilesets.append(tileset)
            self.tileset_tpr.append(tpr)

        self.layers = map_data["layers"]
        self.current_file = map_file
        self.brush_size = 1

        self.show_grid = True
        self.show_help = False
        self.active_layer = 0
        self.selected = 0
        self.palette_off = 0

        self.offset_x = 0
        self.offset_y = 0
        self.panning = False
        self.pan_start = (0,0)
        self.view_start = (0,0)

        self.screen_w, self.screen_h = EDITOR_SIZE

        self.palette_y = self.screen_h - (PALETTE_ROWS * self.tile_size)

        self.undo_stack = deque(maxlen=50)
        self.redo_stack = deque(maxlen=50)
        self._last_snapshot = None
        self._snapshot_taken_this_drag = False

        self.metadata_fields = ["solid", "damage", "interactable"]
        self.current_metadata_field = 0  # index into metadata_fields

        self.tile_metadata = {}  # tile_index -> dict
        self.metadata_path = None
        self.editing_metadata = False


        meta_path = Path(map_data["tilesets"][0]).with_suffix(".json")
        if meta_path.exists():
            self.load_tile_metadata(meta_path)
        else:
            self.metadata_path = meta_path

        self.tileset_names = map_data["tilesets"]

    def load_tile_metadata(self, path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.tile_metadata = data.get("tiles", {})
            self.metadata_path = Path(path)

    def save_tile_metadata(self):
        if not self.metadata_path:
            return
        data = {
            "tile_size": self.tile_size,
            "tiles_per_row": self.tileset_tpr[0],
            "tiles": self.tile_metadata
        }
        with open(self.metadata_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def toggle_metadata(self, index):
        field = self.metadata_fields[self.current_metadata_field]
        if field not in ["solid", "interactable"]:
            return
        meta = self.tile_metadata.get(str(index), {})
        meta[field] = not meta.get(field, False)
        self.tile_metadata[str(index)] = meta
        self.save_tile_metadata()

    def clear_metadata(self, index):
        field = self.metadata_fields[self.current_metadata_field]
        if str(index) in self.tile_metadata:
            self.tile_metadata[str(index)].pop(field, None)
            if not self.tile_metadata[str(index)]:
                del self.tile_metadata[str(index)]
            self.save_tile_metadata()

    def modify_metadata(self, index, delta):
        field = self.metadata_fields[self.current_metadata_field]
        if field not in ["damage", "cost"]:
            return
        meta = self.tile_metadata.get(str(index), {})
        current = meta.get(field, 0)
        meta[field] = max(0, current + delta)
        self.tile_metadata[str(index)] = meta
        self.save_tile_metadata()

    def draw_current_layer(self):
        lines = [
            f"Layer - {self.active_layer}",
            f"Brush Size - {self.brush_size}"
        ]
        for i, line in enumerate(lines):
            text = self.legend_font.render(line, True, FONT_COLOR)
            self.screen.blit(text, (self.screen_w - text.get_width() - 10, 10 + i*18))

    def draw_edit_mode(self):
        line = f"Editing: Metadata[{self.metadata_fields[self.current_metadata_field]}]" if self.editing_metadata else f"Editing: Map"
        text = self.legend_font.render(line, True, FONT_COLOR)
        palette_width = self.tile_size * max(self.tileset_tpr)
        self.screen.blit(text, (palette_width - text.get_width(), self.palette_y - 25))

    def draw_metadata_info(self):
        tile_id = str(self.selected)
        meta = self.tile_metadata.get(tile_id, {})

        x, y = 10, self.palette_y - 25
        spacing = 22

        if not meta:
            text = self.legend_font.render("[No metadata set]", True, (200, 200, 200))
            self.screen.blit(text, (x, y))
            return

        for i, field in enumerate(self.metadata_fields):
            value = meta.get(field, None)
            if value is not None:
                is_current = (i == self.current_metadata_field)
                color = (255, 255, 0) if is_current else FONT_COLOR
                label = f"{field}: {value}"
                text = self.legend_font.render(label, True, color)
                self.screen.blit(text, (x, y))
                y -= spacing

    def draw_legend(self):
        if not self.show_help:
            text = self.legend_font.render("H - Toggle Help", True, FONT_COLOR)
            self.screen.blit(text, (10, 10))
            return
        lines = [
            "H - Toggle Help",
            "TAB - Switch Layer",
            "G - Toggle Grid",
            "S - Save Map",
            "1-6 - Brush Size",
            "F - Fill Layer",
            "C - Clear Layer",
            "Ctrl + Z - Undo",
            "Ctrl + Y - Redo",
            "Mouse Left - Paint",
            "Mouse Right - Erase",
            "Scroll - Palette Scroll"
        ]
        for i, line in enumerate(lines):
            text = self.legend_font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (10, 10 + i * 18))

    def get_active_tileset(self) -> Tuple[List[pygame.Surface], int]:
        return self.tilesets[self.active_layer], self.tileset_tpr[self.active_layer]
        # return (self.overlay_tileset, self.overlay_tpr) if self.active_layer else (self.ground_tileset, self.ground_tpr)

    def scroll_palette(self, direction: int):
        tileset, _ = self.get_active_tileset()
        tiles_per_col = len(tileset) // self.get_active_tpr()
        max_offset = max(0, tiles_per_col - PALETTE_ROWS)
        self.palette_off = max(0, min(max_offset, self.palette_off + direction))

    def get_active_tpr(self) -> int:
        return self.tileset_tpr[self.active_layer]
        # return self.overlay_tpr if self.active_layer else self.ground_tpr

    def draw_map(self):
        for y in range(self.map_h):
            for x in range(self.map_w):
                gx = x * self.tile_size + self.offset_x
                gy = y * self.tile_size + self.offset_y

                # Skip tiles outside view
                if x + self.tile_size < 0 or x > self.screen.get_width():
                    continue
                if y + self.tile_size < 0 or y > self.screen.get_height():
                    continue


                for idx, layer in enumerate(self.layers):
                    id = layer[y][x]
                    if id >= 0:
                        self.screen.blit(self.tilesets[idx][id], (gx, gy))



                # if gid >= 0:
                #     self.screen.blit(self.ground_tileset[gid], (gx, gy))
                # oid = self.overlay_data[y][x]
                # if oid >= 0:
                #     self.screen.blit(self.overlay_tileset[oid], (gx, gy))
                if self.show_grid:
                    pygame.draw.rect(self.screen, GRID_COLOR, (gx, gy, self.tile_size, self.tile_size), 1)

    def draw_palette(self):
        tileset, tpr = self.get_active_tileset()
        pw = self.tile_size
        ph = self.tile_size

        palette_height = ph * PALETTE_ROWS + 4
        palette_width = pw * tpr

        palette_y = self.screen_h - palette_height

        pygame.draw.rect(self.screen, PALETTE_BG, (0, palette_y, palette_width, palette_height))

        for i, tile in enumerate(tileset):
            row = (i // tpr) - self.palette_off
            if 0 <= row < PALETTE_ROWS:
                col = i % tpr
                x = col * pw
                y = row * ph + palette_y + 4
                self.screen.blit(tile, (x, y))
                if i == self.selected:
                    pygame.draw.rect(self.screen, HIGHLIGHT_COL, (x, y, pw, ph), 2)
                if str(i) in self.tile_metadata:
                    meta = self.tile_metadata[str(i)]
                    if meta.get("solid"):
                        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, pw, ph), 1)
                    elif meta.get("interactable"):
                        pygame.draw.rect(self.screen, (0, 255, 255), (x, y, pw, ph), 1)
                    elif "damage" in meta:
                        pygame.draw.rect(self.screen, (255, 128, 0), (x, y, pw, ph), 1)

    def palette_click(self, mx, my) -> bool:
        palette_y_offset = self.screen_h - self.tile_size * PALETTE_ROWS  # Same logic as palette draw
        if my < palette_y_offset:
            return False  # Click is not in the palette area

        rel_y = my - palette_y_offset
        row = rel_y // self.tile_size
        col = mx // self.tile_size

        index = (row + self.palette_off) * self.get_active_tileset()[1] + col

        if 0 <= index < len(self.get_active_tileset()[0]):
            self.selected = index
            if self.editing_metadata:
                self.toggle_metadata(index)
                self.save_tile_metadata()
            return True

        return False

    def paint_tile(self, mx, my, erase=False):
        if not self._snapshot_taken_this_drag:
            self.undo_stack.append(self.snapshot())
            self.redo_stack.clear()
            self._snapshot_taken_this_drag = True

        # Adjust mouse coordinates for the map offset
        mx_adj = mx - self.offset_x
        my_adj = my - self.offset_y

        # Convert adjusted pixel coordinates to tile coordinates
        col = mx_adj // self.tile_size
        row = my_adj // self.tile_size

        # Make sure the position is within the bounds of the map
        if 0 <= col < self.screen_w and 0 <= row < self.screen_h:
            for dy in range(self.brush_size):
                for dx in range(self.brush_size):
                    r = row + dy
                    c = col + dx
                    if 0 <= r < self.screen_h and 0 <= c < self.screen_w:
                        self.layers[self.active_layer][r][c] = -1 if erase else self.selected

    def snapshot(self):
        return {
            "layers": [ [row[:] for row in layer] for layer in self.layers ],
            "layer": self.active_layer,
            "selected": self.selected,
        }

    def apply_snapshot(self, snap):
        self.layers = [ [row[:] for row in layer] for layer in snap["layers"] ]
        self.active_layer = snap["layer"]
        self.selected = snap["selected"]

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.snapshot())
            self.apply_snapshot(self.undo_stack.pop())

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.snapshot())
            self.apply_snapshot(self.redo_stack.pop())

    def run(self):
        """Main editor loop with event listener"""
        running = True
        painting = False
        erase = False
        while running:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    if ev.key == KEY_TOGGLE_HELP:
                        self.show_help = not self.show_help
                    elif ev.key == KEY_EDIT_META:
                        self.editing_metadata = not self.editing_metadata
                        print(f"Metadata edit mode: {self.editing_metadata}")
                    elif self.editing_metadata:
                        if ev.key == pygame.K_TAB:
                            self.current_metadata_field = (self.current_metadata_field + 1) % len(self.metadata_fields)
                        elif ev.key in KEY_NUM_UP:  # + key
                            self.modify_metadata(self.selected, +1)
                        elif ev.key in KEY_NUM_DOWN:
                            self.modify_metadata(self.selected, -1)
                        elif ev.key == pygame.K_SPACE:
                            self.toggle_metadata(self.selected)
                        elif ev.key == pygame.K_BACKSPACE:
                            self.clear_metadata(self.selected)
                    elif ev.key == KEY_SWITCH_LAYER:
                        self.active_layer = (self.active_layer + 1) % len(self.layers)
                        self.selected = 0
                        self.palette_off = 0
                    elif ev.key == KEY_SAVE_MAP:
                            save_map(self.current_file, self.layers, self.map_w, self.map_h, self.tile_size, self.tileset_names)
                    elif ev.key == KEY_TOGGLE_GRID:
                        self.show_grid ^= True
                    elif ev.key == KEY_FILL:
                        if not self.undo_stack or self.snapshot() != self.undo_stack[-1]:
                            self.undo_stack.append(self.snapshot())
                            self.redo_stack.clear()
                        self.layers[self.active_layer] = fill_layer(self.map_w, self.map_h, self.selected)
                    elif ev.key == KEY_CLEAR:
                        if not self.undo_stack or self.snapshot() != self.undo_stack[-1]:
                            self.undo_stack.append(self.snapshot())
                            self.redo_stack.clear()
                        self.layers[self.active_layer] = blank_layer(self.map_w, self.map_h)

                    elif ev.key == pygame.K_DOWN:
                        self.scroll_palette(1)
                    elif ev.key == pygame.K_UP:
                        self.scroll_palette(-1)
                    elif pygame.K_1 <= ev.key <= pygame.K_6:
                        self.brush_size = ev.key - pygame.K_0
                    elif ev.key == pygame.K_z and (ev.mod & pygame.KMOD_CTRL):
                        self.undo()
                    elif ev.key == pygame.K_y and (ev.mod & pygame.KMOD_CTRL):
                        self.redo()

                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if ev.button == 1: # MB1
                        if not self.palette_click(*ev.pos):
                            painting = True
                            erase = False
                            self._snapshot_taken_this_drag = False
                            self.paint_tile(*ev.pos, erase=False)
                    elif ev.button == 2: # Middle mouse
                        self.panning = True
                        self.pan_start = ev.pos
                        self.view_start = (self.offset_x, self.offset_y)
                    elif ev.button == 3: # MB2
                        painting = True
                        erase = True
                        self._snapshot_taken_this_drag = False
                        self.paint_tile(*ev.pos, erase=True)
                    elif ev.button == 4:
                        self.scroll_palette(-1)
                    elif ev.button == 5:
                        self.scroll_palette(1)
                elif ev.type == pygame.MOUSEBUTTONUP:
                    if ev.button in (1, 3):
                        painting = False
                        self._snapshot_taken_this_drag = False
                    elif ev.button == 2:
                        self.panning = False
                elif ev.type == pygame.MOUSEMOTION:
                    if painting:
                        self.paint_tile(*ev.pos, erase=erase)
                    elif self.panning:
                        dx = ev.pos[0] - self.pan_start[0]
                        dy = ev.pos[1] - self.pan_start[1]
                        self.offset_x = self.view_start[0] + dx
                        self.offset_y = self.view_start[1] + dy

            self.screen.fill(SCREEN_BG)
            self.draw_map()
            self.draw_palette()
            self.draw_legend()
            self.draw_metadata_info()
            self.draw_current_layer()
            self.draw_edit_mode()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()