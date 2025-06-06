from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.scrolled import ScrolledFrame
import tkinter.messagebox as mb
from ttkbootstrap.constants import *
from pathlib import Path
from map_editor import MapEditor
from map_helper import load_map, save_map, blank_layer
from copy import deepcopy

DEFAULT_LAYERS = 2

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        style = ttk.Style("superhero")
        style.configure("TButton", font=("Helvetica", 26, "bold"))
        style.configure("browse.TButton", font=("Helvetica", 12, "bold"))
        style.configure("remove.Link.TButton", font=("Helvetica", 12, "bold"))
        style.map("remove.Link.TButton", foreground=[("active", "red")])

        self.layers: list = []
        self.layer_tilesets: list= []

        self.validation = self.register(self.only_numbers)
        self.is_new_map = True

        self.frame1 = ttk.Frame(self)
        self.frame1.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.8)
        self.frame2 = ttk.Frame(self)

        self.back_button = ttk.Button(self, text="Back", bootstyle=SECONDARY, command=self.show_initial_frame)

        self.data_frame = ttk.Frame(self.frame2)
        self.data_frame.pack(fill=BOTH, expand=True)

        ttk.Label(self.data_frame, text="Map File").pack(anchor=W)
        self.map_file_frame = ttk.Frame(self.data_frame)
        self.map_file_frame.pack(fill=X, expand=True)
        self.map_file_entry = ttk.Entry(self.map_file_frame)
        self.map_file_entry.pack(side=LEFT, fill=X, expand=True)
        self.map_file_button = ttk.Button(self.map_file_frame, text="Browse", command=self.choose_map_file, style="browse.TButton")
        self.map_file_button.pack(side=LEFT)

        ttk.Label(self.data_frame, text="Tile Size").pack(anchor=W)
        self.tile_size_entry = ttk.Entry(self.data_frame, validate="key", validatecommand=(self.validation, '%S'))
        self.tile_size_entry.pack(fill=X, expand=True)

        ttk.Label(self.data_frame, text="Map Width").pack(anchor=W)
        self.map_width_entry = ttk.Entry(self.data_frame, validate="key", validatecommand=(self.validation, '%S'))
        self.map_width_entry.pack(fill=X, expand=True)

        ttk.Label(self.data_frame, text="Map Height").pack(anchor=W)
        self.map_height_entry = ttk.Entry(self.data_frame, validate="key", validatecommand=(self.validation, '%S'))
        self.map_height_entry.pack(fill=X, expand=True)

        self.load_editor_button = ttk.Button(self.frame2, text="Load Editor", command=self.load_editor)
        self.load_editor_button.pack(pady=10)

        self.add_layer_button = ttk.Button(self, text="Add Layer", command=self.add_layer)

        ttk.Label(self.frame1, text="Simple Map Editor", font=("Helvetica", 40, "bold")).pack(pady=30)

        self.new_button = ttk.Button(self.frame1, text="New Map", command=self.show_data_frame, padding=20)
        self.new_button.pack(padx=10, pady=10)

        self.load_button = ttk.Button(self.frame1, text="Load Map", command=self.load_map, padding=20)
        self.load_button.pack(padx=10, pady=10)

    def add_layer(self, e=None, value=None):
        layer_index = len(self.layers)
        layer_frame = ttk.Frame(self.data_frame)
        layer_frame.pack(fill=BOTH, expand=True)

        tileset_value = ttk.StringVar()

        self.layer_tilesets.append(tileset_value)

        ttk.Label(layer_frame, text=f"Tileset - Layer {layer_index}").pack(anchor=W)
        tileset_frame = ttk.Frame(layer_frame)
        tileset_frame.pack(fill=X, expand=True)
        tileset_entry = ttk.Entry(tileset_frame, textvariable=tileset_value)
        tileset_entry.pack(side=LEFT, fill=X, expand=True)
        tileset_button = ttk.Button(tileset_frame, text="Browse", command=lambda: self.choose_tileset(layer_index), style="browse.TButton")
        tileset_button.pack(side=LEFT)
        tileset_remove = ttk.Button(tileset_frame, text="Delete Layer", style="remove.Link.TButton", command=lambda: self.remove_layer(layer_index))
        tileset_remove.pack(side=LEFT)

        if value is not None:
            tileset_value.set(value.get() if hasattr(value, "get") else value)

        self.layers.append(layer_frame)

    def remove_layer(self, layer_index):
        """Whenever removing a layer, regenerate all existing layers to update indexes and labels"""
        for layer in self.layers:
            layer.pack_forget()
        self.layers.pop(layer_index)
        self.layer_tilesets.pop(layer_index)
        layers = len(self.layers)
        layer_tilesets = [val for val in self.layer_tilesets]

        self.layers.clear()
        self.layer_tilesets.clear()

        for idx in range(layers):
            self.add_layer(value=layer_tilesets[idx])

    def load_map(self, event=None):
        path = filedialog.askopenfilename(title="Select Map file (json)")
        path_object = Path(path)
        if path_object and path_object.exists() and path != "":
            self.map_file = path
            self.map_data = load_map(path_object)
            self.populate_data_frame(map_data=self.map_data, map_path=path)
            self.is_new_map = False
            self.show_data_frame()
        else:
            mb.showerror(message="That file does not exist", title="File does not exist")

    def show_initial_frame(self):
        self.frame2.place_forget()
        self.back_button.place_forget()
        self.add_layer_button.place_forget()
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

    def show_data_frame(self, e=None):
        self.frame1.place_forget()
        self.frame2.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.8)

        self.back_button.place(x=25, y=25, anchor=NW)
        self.add_layer_button.place(relx=1, rely=0, anchor=NE)

    def choose_map_file(self):
        file = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        self.map_file_entry.delete(0, "")
        self.map_file_entry.insert(0, file)

    def choose_tileset(self, layer_index):
        folder = filedialog.askopenfilename(title="Select Tileset (png)")
        self.layer_tilesets[layer_index].set(folder)

    def populate_data_frame(self, map_data: dict, map_path: str):
        self.map_file_entry.insert(0, map_path)
        self.tile_size_entry.insert(0, map_data["tile_size"])
        self.map_width_entry.insert(0, map_data["map_width"])
        self.map_height_entry.insert(0, map_data["map_height"])

        if self.layers:
            for layer in self.layers:
                layer.pack_forget()
            self.layers.clear()
        for idx, tileset in enumerate(map_data["tilesets"]):
            self.add_layer(value=tileset)

        # for widget in self.frame2.winfo_children():
        #     if widget.winfo_class() == "TEntry":
        #         widget.configure(state="disabled")
        #
        # for frame in self.layers:
        #     for inner_widget in frame.winfo_children():
        #         if inner_widget.winfo_class() == "TEntry" or inner_widget.winfo_class() == "TButton":
        #             inner_widget.configure(state="disabled")

    def only_numbers(self, char):
        return char.isdigit()

    def validate_fields(self):
        validation_rules = [
            self.map_file_entry.get() != "",
            self.tile_size_entry.get() != "",
            self.map_width_entry.get() != "",
            self.map_height_entry.get() != "",
            *[var.get() != "" for var in self.layer_tilesets]
        ]

        return False in validation_rules

    def load_editor(self):
        # Save map file then load
        if self.validate_fields():
            mb.showerror(message="Please ensure all required fields are entered.")
            return

        if self.map_file_entry.get() == "":
            mb.showerror(message="Please input a file path for your map")
            return
        else:
            path = Path(self.map_file_entry.get())

        if self.is_new_map:
            map_w = int(self.map_width_entry.get())
            map_h = int(self.map_height_entry.get())
            self.map_data = {
                "tile_size":  int(self.tile_size_entry.get()),
                "map_width":  map_w,
                "map_height": map_h,
                "tilesets": [var.get() for var in self.layer_tilesets],
                "layers": [blank_layer(map_w, map_h) for _ in self.layer_tilesets]
            }

        save_map(path, self.map_data["layers"], self.map_data["map_width"], self.map_data["map_height"], self.map_data["tile_size"], self.map_data["tilesets"])

        self.withdraw()

        editor = MapEditor(map_data=self.map_data, map_file=path)
        editor.run()

        # Close tkinter application after editor is closed
        self.quit()