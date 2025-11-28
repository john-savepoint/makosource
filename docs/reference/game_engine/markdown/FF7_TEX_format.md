# FF7/TEX format {#ff7tex_format}

- [FF7/TEX format](#ff7tex_format){#toc-ff7tex_format}
  - [TEX Texture Data Format for PC by Mirex (Edits by Aali)](#tex_texture_data_format_for_pc_by_mirex_edits_by_aali){#toc-tex_texture_data_format_for_pc_by_mirex_edits_by_aali}



## TEX Texture Data Format for PC by [Mirex](User:Mirex "Mirex"){.wikilink} (Edits by [Aali](User:Aali "Aali"){.wikilink}) {#tex_texture_data_format_for_pc_by_mirex_edits_by_aali}

FF7 PC texture consists of header, an optional palette and bitmap data. Usually data are stored like palletized picture, with bitmap pixels referencing to palette. Color 0 (in palette its usually black) is usually used as transparent color.

*Pixel values of 0 may or may not be transparent, depending on the color key status, more on that later. This also applies to non-paletted formats.*

When bit depth is 16 then data are stored as packed RGB in style RGB555, which means 5 bits per color in one 2 byte entry. I\'m not sure if it is used in FF7 at all, its probably used in FF8.

*The tex format is actually very flexible and can take almost any non-paletted format as long as you describe it properly in the header.*

<table>
<thead>
<tr>
<th style="border: 1px grey; vertical-align: middle; width: 51px; height: 26px; background-color: rgb(130, 130, 130)"><p>Offset</p></th>
<th style="border: 1px grey; vertical-align: middle; width: 126px; height: 26px; background-color: rgb(130, 130, 130)"><p>Size</p></th>
<th style="border: 1px grey; vertical-align: middle; width: 222px; height: 26px; background-color: rgb(130, 130, 130)"><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Header</p></td>
</tr>
<tr>
<td><p>0x00</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Version, must be 1, or FF7 won't load the file</p></td>
</tr>
<tr>
<td><p>0x04</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x08</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Color key flag</p></td>
</tr>
<tr>
<td><p>0x0C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x10</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x14</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum bits per color (D3D driver uses these to determine which texture format to convert to on load)</p></td>
</tr>
<tr>
<td><p>0x18</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum bits per color</p></td>
</tr>
<tr>
<td><p>0x1C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum alpha bits</p></td>
</tr>
<tr>
<td><p>0x20</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum alpha bits</p></td>
</tr>
<tr>
<td><p>0x24</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Minimum bits per pixel</p></td>
</tr>
<tr>
<td><p>0x28</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Maximum bits per pixel</p></td>
</tr>
<tr>
<td><p>0x2C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x30</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of palettes</p></td>
</tr>
<tr>
<td><p>0x34</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of colors per palette</p></td>
</tr>
<tr>
<td><p>0x38</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bit depth</p></td>
</tr>
<tr>
<td><p>0x3C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Image Width</p></td>
</tr>
<tr>
<td><p>0x40</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Image Height</p></td>
</tr>
<tr>
<td><p>0x44</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Pitch or bytes per row, usually ignored and assumed to be bytes per pixel * width</p></td>
</tr>
<tr>
<td><p>0x48</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0x4C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette flag (this indicates the presence of a palette)</p></td>
</tr>
<tr>
<td><p>0x50</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bits per index, always 0 for non-paletted images</p></td>
</tr>
<tr>
<td><p>0x54</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Indexed-to-8bit flag, never used in FF7</p></td>
</tr>
<tr>
<td><p>0x58</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette size, always number of palettes * colors per palette</p></td>
</tr>
<tr>
<td><p>0x5C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of colors per palette (again, may be 0 sometimes, the other value will be used anyway)</p></td>
</tr>
<tr>
<td><p>0x60</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data, ignored on load</p></td>
</tr>
<tr>
<td><p>0x64</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bits per pixel</p></td>
</tr>
<tr>
<td><p>0x68</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Bytes per pixel, always use this to determine how much data to read, if this is 1 you read 1 byte per pixel, regardless of bit depth</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: black; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: black; border-width: 1px"><p>Pixel format (all 0 for paletted images)</p></td>
</tr>
<tr>
<td><p>0x6C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of red bits</p></td>
</tr>
<tr>
<td><p>0x70</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of green bits</p></td>
</tr>
<tr>
<td><p>0x74</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of blue bits</p></td>
</tr>
<tr>
<td><p>0x78</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Number of alpha bits</p></td>
</tr>
<tr>
<td><p>0x7C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red bitmask</p></td>
</tr>
<tr>
<td><p>0x80</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green bitmask</p></td>
</tr>
<tr>
<td><p>0x84</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue bitmask</p></td>
</tr>
<tr>
<td><p>0x88</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha bitmask</p></td>
</tr>
<tr>
<td><p>0x8C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red shift</p></td>
</tr>
<tr>
<td><p>0x90</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green shift</p></td>
</tr>
<tr>
<td><p>0x94</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue shift</p></td>
</tr>
<tr>
<td><p>0x98</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha shift</p></td>
</tr>
<tr>
<td><p>0x9C</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Always 8 - Number of red bits (Not sure what the point of these fields is, they're always ignored anyway)</p></td>
</tr>
<tr>
<td><p>0xA0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of green bits</p></td>
</tr>
<tr>
<td><p>0xA4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of blue bits</p></td>
</tr>
<tr>
<td><p>0xA8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>8 - Number of alpha bits</p></td>
</tr>
<tr>
<td><p>0xAC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Red max</p></td>
</tr>
<tr>
<td><p>0xB0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Green max</p></td>
</tr>
<tr>
<td><p>0xB4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Blue max</p></td>
</tr>
<tr>
<td><p>0xB8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Alpha max</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: black; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: black; border-width: 1px"><p>End of pixel format</p></td>
</tr>
<tr>
<td><p>0xBC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Color key array flag (this indicates the presence of a color key array)</p></td>
</tr>
<tr>
<td><p>0xC0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xC4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Reference alpha (more on this later)</p></td>
</tr>
<tr>
<td><p>0xC8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xCC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xD0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Palette index (runtime data)</p></td>
</tr>
<tr>
<td><p>0xD4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xD8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Runtime data</p></td>
</tr>
<tr>
<td><p>0xDC</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE0</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE4</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td><p>0xE8</p></td>
<td><p>4 bytes (long)</p></td>
<td><p>Unknown</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Palette data (ignore this section if palette flag is 0)</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>0xEC</p></td>
<td style="border: 1px grey; vertical-align: top"><p>Palette size * 4</p></td>
<td style="border: 1px grey; vertical-align: top"><p>The raw palette data, always in 32-bit BGRA format</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Pixel data</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>Varies</p></td>
<td colspan="2" style="border: 1px grey; vertical-align: top"><p>Read width * height * "bytes per pixel" bytes of data. If there's a palette, every pixel is an index into that palette, otherwise use the pixel format specification.</p></td>
</tr>
<tr>
<td style="border-style: solid none solid solid; border-color: grey; border-width: 1px; vertical-align: top"></td>
<td colspan="2" style="border-style: solid solid solid none; border-color: grey; border-width: 1px"><p>Color key array</p></td>
</tr>
<tr>
<td style="border: 1px grey; vertical-align: top"><p>Varies</p></td>
<td colspan="2" style="border: 1px grey; vertical-align: top"><p>Number of palettes * 1 bytes.</p></td>
</tr>
</tbody>
</table>

*Color keying: If the color key flag is zero, no color keying is performed and the color key array is ignored. Otherwise, the current palette index is used to retrieve a single byte from the color key array, this is the new color key flag, zero means don\'t do color keying.* If there is no color key array (and the color key flag is not zero), you should always color key.

*Reference alpha: Only applies to paletted images, if the alpha value sampled from the palette is 0xFE, this value should be replaced with the reference alpha.*
