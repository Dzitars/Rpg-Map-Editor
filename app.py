from tkinter import filedialog
import ttkbootstrap as ttk
import tkinter.messagebox as mb
from ttkbootstrap.constants import *
from pathlib import Path
from map_editor import MapEditor
from map_helper import load_map, save_map

class App(ttk.Window):
    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        style = ttk.Style("superhero")
        style.configure("TButton", font=("Helvetica", 26, "bold"))
        style.configure("browse.TButton", font=("Helvetica", 12, "bold"))

        self.validation = self.register(self.only_numbers)
        self.is_new_map = True

        self.frame1 = ttk.Frame(self)
        self.frame1.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=0.8)
        self.frame2 = ttk.Frame(self)

        self.back_button = ttk.Button(self, text="Back", bootstyle=SECONDARY, command=self.show_initial_frame)

        ttk.Label(self.frame2, text="Map File").pack(anchor=W)
        self.map_file_frame = ttk.Frame(self.frame2)
        self.map_file_frame.pack(fill=X, expand=True)
        self.map_file_entry = ttk.Entry(self.map_file_frame)
        self.map_file_entry.pack(side=LEFT, fill=X, expand=True)
        self.map_file_button = ttk.Button(self.map_file_frame, text="Browse", command=self.choose_map_file, style="browse.TButton")
        self.map_file_button.pack(side=LEFT)

        ttk.Label(self.frame2, text="Tile Size").pack(anchor=W)
        self.tile_size_entry = ttk.Entry(self.frame2, validate="key", validatecommand=(self.validation, '%S'))
        self.tile_size_entry.pack(fill=X, expand=True)

        ttk.Label(self.frame2, text="Map Width").pack(anchor=W)
        self.map_width_entry = ttk.Entry(self.frame2, validate="key", validatecommand=(self.validation, '%S'))
        self.map_width_entry.pack(fill=X, expand=True)

        ttk.Label(self.frame2, text="Map Height").pack(anchor=W)
        self.map_height_entry = ttk.Entry(self.frame2, validate="key", validatecommand=(self.validation, '%S'))
        self.map_height_entry.pack(fill=X, expand=True)

        ttk.Label(self.frame2, text="Ground Tileset").pack(anchor=W)
        self.ground_tileset_frame = ttk.Frame(self.frame2)
        self.ground_tileset_frame.pack(fill=X, expand=True)
        self.ground_tileset_entry = ttk.Entry(self.ground_tileset_frame)
        self.ground_tileset_entry.pack(side=LEFT, fill=X, expand=True)
        self.ground_tileset_button = ttk.Button(self.ground_tileset_frame, text="Browse", command=self.choose_ground_tileset, style="browse.TButton")
        self.ground_tileset_button.pack(side=LEFT)

        ttk.Label(self.frame2, text="Overlay Tileset").pack(anchor=W)
        self.overlay_tileset_frame = ttk.Frame(self.frame2)
        self.overlay_tileset_frame.pack(fill=X, expand=True)
        self.overlay_tileset_entry = ttk.Entry(self.overlay_tileset_frame)
        self.overlay_tileset_entry.pack(side=LEFT, fill=X, expand=True)
        self.overlay_tileset_button = ttk.Button(self.overlay_tileset_frame, text="Browse", command=self.choose_overlay_tileset, style="browse.TButton")
        self.overlay_tileset_button.pack(side=LEFT)

        self.load_editor_button = ttk.Button(self.frame2, text="Load Editor", command=self.load_editor)
        self.load_editor_button.pack(pady=10)

        ttk.Label(self.frame1, text="Simple Map Editor", font=("Helvetica", 40, "bold")).pack(pady=30)

        self.new_button = ttk.Button(self.frame1, text="New Map", command=self.show_data_frame, padding=20)
        self.new_button.pack(padx=10, pady=10)

        self.load_button = ttk.Button(self.frame1, text="Load Map", command=self.load_map, padding=20)
        self.load_button.pack(padx=10, pady=10)

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
        self.frame1.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5)

    def show_data_frame(self, e=None):
        self.frame1.place_forget()
        self.frame2.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.5)

        self.back_button.place(x=25, y=25, anchor=NW)

    def choose_map_file(self):
        file = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json")])
        self.map_file_entry.delete(0, "")
        self.map_file_entry.insert(0, file)

    def choose_ground_tileset(self):
        folder = filedialog.askopenfilename(title="Select Tileset (png)")
        self.ground_tileset_entry.delete(0, "")
        self.ground_tileset_entry.insert(0, folder)

    def choose_overlay_tileset(self):
        folder = filedialog.askopenfilename(title="Select Tileset (png)")
        self.overlay_tileset_entry.delete(0, "")
        self.overlay_tileset_entry.insert(0, folder)

    def populate_data_frame(self, map_data: dict, map_path: str):
        self.map_file_entry.insert(0, map_path)
        self.tile_size_entry.insert(0, map_data["tile_size"])
        self.map_width_entry.insert(0, map_data["map_width"])
        self.map_height_entry.insert(0, map_data["map_height"])
        self.ground_tileset_entry.insert(0, map_data["ground_tileset"])
        self.overlay_tileset_entry.insert(0, map_data["overlay_tileset"])

        for widget in self.frame2.winfo_children():
            if widget.winfo_class() == "TEntry":
                widget.configure(state="disabled")
            if widget.winfo_class() == "TFrame":
                for inner_widget in widget.winfo_children():
                    if inner_widget.winfo_class() == "TEntry" or inner_widget.winfo_class() == "TButton":
                        inner_widget.configure(state="disabled")

    def only_numbers(self, char):
        return char.isdigit()

    def validate_fields(self):
        validation_rules = [
            self.map_file_entry.get() != "",
            self.tile_size_entry.get() != "",
            self.map_width_entry.get() != "",
            self.map_height_entry.get() != "",
            self.ground_tileset_entry.get() != "",
            self.overlay_tileset_entry.get() != ""
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
            self.map_data = {
                "tile_size":  int(self.tile_size_entry.get()),
                "map_width":   int(self.map_width_entry.get()),
                "map_height":  int(self.map_height_entry.get()),
                "ground_tileset":     self.ground_tileset_entry.get(),
                "overlay_tileset":    self.overlay_tileset_entry.get(),
                "ground_data":  [],
                "overlay_data": [],
            }

        save_map(path, self.map_data["ground_data"], self.map_data["overlay_data"], self.map_data["map_width"], self.map_data["map_height"], self.map_data["tile_size"], self.map_data["ground_tileset"],
                 self.map_data["overlay_tileset"])

        self.withdraw()

        editor = MapEditor(map_data=self.map_data, map_file=path)
        editor.run()

        # Close tkinter application after editor is closed
        self.quit()