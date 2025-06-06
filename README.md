<h1>Instructions for Use:</h1>

<h2>1. New or Load</h2>
<p>Select either new map to start from scratch, or load map to load an existing map.json file</p>

<h2>2. Enter in all required fields, or skip if loading existing:</h2>
<table>
<tr>
    <th>Field</th><th>Description</th>
</tr>
<tr>
    <td>Map File</td><td>The name and location you want to save your map file to</td>
</tr>
<tr>
    <td>Tile Size</td><td>The size of the tiles in your supplied tileset images</td>
</tr>
<tr>
    <td>Map Width</td><td>The width of your desired map, in number of tiles</td>
</tr>
<tr>
    <td>Map Height</td><td>The height of your desired map, in number of tiles</td>
</tr>
<tr>
    <td>Ground Tileset</td><td>A png image to use as a tileset for your ground layer</td>
</tr>
<tr>
    <td>Overlay Tileset</td><td>A png image to use as a tileset for your overlay layer</td>
</tr>
</table>

<h2>3. Load The Editor</h2>
<p>
  Once load editor is clicked, a pygame window will open to display the map editor<br>
  The editor contains the map data, as well as a palette frame at the bottom.
</p>
<h2>Controls</h2>
<p>While editing map, the M key can be pressed to toggle between editing the map or editing the tileset metadata, <br>
and the control scheme changes slightly between each</p>

<table>
  <tr>
    <td valign="top">
        <h3>While editing map:</h3>
        <table>
        <tr><th>Key</th><th>Action</th></tr>
        <tr><td>H</td><td>Toggle Help</td></tr>
        <tr><td>TAB</td><td>Switch Layer</td></tr>
        <tr><td>G</td><td>Toggle Grid</td></tr>
        <tr><td>S</td><td>Save Map</td></tr>
        <tr><td>1-6</td><td>Brush Size</td></tr>
        <tr><td>F</td><td>Fill Layer</td></tr>
        <tr><td>C</td><td>Clear Layer</td></tr>
        <tr><td>CTRL + Z</td><td>Undo</td></tr>
        <tr><td>CTRL + Y</td><td>Redo</td></tr>
        <tr><td>Mouse Left</td><td>Paint</td></tr>
        <tr><td>Mouse Right</td><td>Erase</td></tr>
        <tr><td>Mouse Middle</td><td>Move Map (drag)</td></tr>
        <tr><td>Scroll</td><td>Palette Scroll</td></tr>
        <tr><td>M</td><td>Toggle Edit Mode</td></tr>
        </table>
    </td>
    <td style="width: 40px;"></td>
    <td valign="top">
        <h3>While editing metadata:</h3>
        <table>
        <tr><th>Key</th><th>Action</th></tr>
        <tr><td>M</td><td>Switch back to Map Mode</td></tr>
        <tr><td>Mouse Left</td><td>Toggle boolean metadata</td></tr>
        <tr><td>TAB</td><td>Switch Metadata Field</td></tr>
        <tr><td>+</td><td>Increase number metadata</td></tr>
        <tr><td>-</td><td>Decrease number metadata</td></tr>
        <tr><td>Backspace</td><td>Remove current metadata</td></tr>
        </table>
    </td>
  </tr>
</table>

<div>
    <h2>Regarding MetaData</h2>
    <p>
    Currently supported metadata types are Solid (bool), Damage(int) and Interactable(bool).<br>
    Boolean metadata can be toggled off and on by simply clicking on the tile, for integer metadata the tile must be selected and then use + or - to change the value.
    Tiles will be given borders based on which metadata they have active, metadata values of the currently selected tile are also shown above the palette.
    </p>
</div>

