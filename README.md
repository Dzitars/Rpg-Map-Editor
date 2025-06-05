Instructions for Use:

Select new map to start from scratch, or load map to load an existing map.json file
Enter in all required fields:
  Map File: The name and location you want to save your map file to
  Tile Size: The size of the tiles in your supplied tileset images
  Map Width: The width of your desired map, in number of tiles
  Map Height: The height of your desired map, in number of tiles
  Ground Tileset: A png image to use as a tileset for your ground layer
  Ground Tiles Per Row: How many tiles are there per row in your tileset (to be removed and auto generated)
  Overlay Tileset: A png image to use as a tileset for your overlay layer
  Overlay Tiles Per Row: How manby tiles are there per row in your tileset (to be removed and auto generated)

Once load editor is clicked, a pygame window will open to display the map editor
The editor contains the map data, as well as a palette frame at the bottom.
The controls for the editor are as follows:
  While editing map:
    H - Toggle Help
    TAB - Switch Layer
    G - Toggle Grid
    S - Save Map
    L - Load Map
    N - New Map
    1-6 - Brush Size
    F - Fill Layer
    C - Clear Layer
    Ctrl + Z - Undo
    Ctrl + Y - Redo
    Mouse Left - Paint
    Mouse Right - Erase
    Mouse Middle - Move Map (drag)
    Scroll - Palette Scroll
    M - Switch to MetaData Mode
  
  While editing metadata:
    M - Switch back to Map Mode
    Mouse Left - toggle boolean metadata
    Tab - Switch Metadata Field
    + - increase number metadata
    - - decrease number metadata
    Backspace - remove current metadata

Regarding MetaData - Currently supported metadata types are Solid (bool), Damage(int) and Interactable(bool).
boolean metadata can be toggled off and on by simply clicking on the tile, for integer metadata the tile must be selected and then use + or - to change the value.
Tiles will be given borders based on which metadata they have active, metadata values of the currently selected tile are also shown above the palette.

