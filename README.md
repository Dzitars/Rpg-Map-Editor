<h1>Instructions for Use:</h1>

<h2>1. New or Load</h2>
<p>Select either new map to start from scratch, or load map to load an existing map.json file</p>

<h2>2. Enter in all required fields, or skip if loading existing:</h2>
<ul>
  <li>Map File: The name and location you want to save your map file to</li>
  <li>Tile Size: The size of the tiles in your supplied tileset images</li>
  <li>Map Width: The width of your desired map, in number of tiles</li>
  <li>Map Height: The height of your desired map, in number of tiles</li>
  <li>Ground Tileset: A png image to use as a tileset for your ground layer</li>
  <li>Ground Tiles Per Row: How many tiles are there per row in your tileset (to be removed and auto generated)</li>
  <li>Overlay Tileset: A png image to use as a tileset for your overlay layer</li>
  <li>Overlay Tiles Per Row: How manby tiles are there per row in your tileset (to be removed and auto generated)</li>
</ul>

<h2>3. Load The Editor</h2>
<p>
  Once load editor is clicked, a pygame window will open to display the map editor<br>
  The editor contains the map data, as well as a palette frame at the bottom.
</p>
<h2>Controls</h2>
<p>While editing map, the M key can be pressed to toggle between editing the map or editing the tileset metadata, <br>
and the control scheme changes slightly between each</p>
<h3>While editing map:</h3>
<ul>
    <li><b>H</b> - Toggle Help</li>
    <li><b>TAB</b> - Switch Layer</li>
    <li><b>G</b> - Toggle Grid</li>
    <li><b>S</b> - Save Map</li>
    <li><b>L</b> - Load Map</li>
    <li><b>N</b> - New Map</li>
    <li><b>1-6</b> - Brush Size</li>
    <li><b>F</b> - Fill Layer</li>
    <li><b>C</b> - Clear Layer</li>
    <li><b>CTRL + Z</b> - Undo</li>
    <li><b>CTRL + Y</b> - Redo</li>
    <li><b>Mouse Left</b> - Paint</li>
    <li><b>Mouse Right</b> - Erase</li>
    <li><b>Mouse Middle</b> - Move Map (drag)</li>
    <li><b>Scroll</b> - Palette Scroll</li>
    <li><b>M</b> - Toggle Edit Mode</li>
</ul>
<h3>While editing metadata:<br></h3>
<ul>
    <li><b>M</b> - Switch back to Map Mode</li>
    <li><b>Mouse Left</b> - toggle boolean metadata</li>
    <li><b>TAB</b> - Switch Metadata Field</li>
    <li><b>+</b> - increase number metadata</li>
    <li><b>-</b> - decrease number metadata</li>
    <li><b>Backspace</b> - remove current metadata</li>
</ul>
<h3>Regarding MetaData</h3>
<p>
Currently supported metadata types are Solid (bool), Damage(int) and Interactable(bool).
boolean metadata can be toggled off and on by simply clicking on the tile, for integer metadata the tile must be selected and then use + or - to change the value.
Tiles will be given borders based on which metadata they have active, metadata values of the currently selected tile are also shown above the palette.
</p>
