# FF7/Kernel/Low level libraries {#ff7kernellow_level_libraries}

- [FF7/Kernel/Low level libraries](#ff7kernellow_level_libraries){#toc-ff7kernellow_level_libraries}
  - [PC to PSX comparison](#pc_to_psx_comparison){#toc-pc_to_psx_comparison}
  - [Data Archives](#data_archives){#toc-data_archives}


## PC to PSX comparison {#pc_to_psx_comparison}

The files and data formats used in the PSX version of FF7 and it\'s PC port are conceptually the same thing, and accomplish the same tasks. That being said, they both have wildly different formats, both of which were derived from a third original format that is also somewhat different to the first two.

The original PSX FF7 was created in part using Sony\'s Psy-Q development library. This library uses common formats that are \"native\" to the PSX. Often, a toolkit was used to convert common development-based formats, such as a TGA bitmap or a palleted GIF file, to something a little more suited to Psy-Q, which would be a [TIM file](PSX/TIM_format "TIM file"){.wikilink}.

During the porting process to the PC, some of the original artwork (and artists for that matter) were no longer available. This resulted in the port team having to use the Psy-Q versions of many files, which were ill suited for the PC architecture. In our example, the [TIM file](PSX/TIM_format "TIM file"){.wikilink} was converted to a TEX file, which would be manipulated in the PC\'s video memory a little more efficiently. Sometimes the original artwork was available, such as the pictures of the characters within the menu, or the original MIDI files. Most often times it was not.

To make things a little more confusing, both systems also archive their data files in different ways, making the extraction and rendering of each file a bit of a bear. For the most part the data within each file is the same thing, just a little switched around. Here, we will cover the more generic files first, and then common files used in each module.

## Data Archives {#data_archives}

To save space, quicken access time, and to obfuscate the file structure a little, most of the data files are stored in some kind of archive format. The archives remove such useful items as subdirectories and logical data placement. There is no real \"native\" format these are based on.

### BIN archive data format {#bin_archive_data_format}

The BIN format comes as two different types. They both have the same extension, so one must open the file to see which format is which. They are best described as BIN Types and BIN-GZIP types.

#### BIN Type Archives {#bin_type_archives}

These are uncompressed archives. The header is 4 bytes long and gives the length of the file without the header and then the data beyond that.

#### BIN-GZIP Type Archives {#bin_gzip_type_archives}

Unless otherwise noted, these have a 6 byte header. After this are many gziped sections concatenated together.

<table>
<thead>
<tr>
<th><p>Offset</p></th>
<th><p>Length</p></th>
<th><p>Description</p></th>
</tr>
</thead>
<tbody>
<tr>
<td><p>0x0000</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of gzipped section 1</p></td>
</tr>
<tr>
<td><p>0x0002</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of ungzipped section 1</p></td>
</tr>
<tr>
<td><p>0x0004</p></td>
<td><p>2 bytes</p></td>
<td><p>File type*</p></td>
</tr>
<tr>
<td><p>0x0006</p></td>
<td><p>Varies</p></td>
<td><p>[0x1F8B080000000000...] - Gzip header 1 and data</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of gzipped section 2</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>Length of ungzipped section 2</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>2 bytes</p></td>
<td><p>File type*</p></td>
</tr>
<tr>
<td><p>Varies</p></td>
<td><p>Varies</p></td>
<td><p>[0x1F8B080000000000...] - Gzip header 2 and data</p></td>
</tr>
<tr>
<td colspan="3" style="text-align: center;"><p>...</p></td>
</tr>
</tbody>
</table>

\
*\** This particular value might be ignored by the whatever method is decompressing these archive types. Within archives it declares that the compressed file is a particular type. These values seem to be unique to the particular archive that is being opened and is not consistent between archives.

Example 1: Within the [KERNEL.BIN](FF7/Kernel/Kernel.bin "KERNEL.BIN"){.wikilink} the first nine files are all different data sets so are numbered sequentially 0-8. All remaining files are text types and get labeled as type 9.\
Example 2: Within the WINDOW.BIN file there are three files. The first two are type \"0\" and are textures. The third file is type \"1\" and not a texture.

### LZS Archives {#lzs_archives}

The [LZS format](FF7/LZS_format "LZS format"){.wikilink} is used throughout the PSX version of Final Fantasy 7, often ending with the .lzs extension. LZS itself stands for Lempel-Ziv-Shannon-Fano, Statistical plus Arithmetic. It was originally developed by [Professor Haruhiko Okumura](http://oku.edu.mie-u.ac.jp/~okumura/index-e.html) based on the work of [Abraham Lempel](http://www.hpl.hp.com/about/bios/abraham_lempel.html) and [Jacob Ziv](http://www.marconifoundation.org/pages/dynamic/fellows/fellow_details.php?roster_id=23).

<!-- EXTRACTED FROM MAJOR SECTION: 03_KERNEL.md lines 592-665 -->

#### LZS Archive Format

The LZS archive has a very small header at 0x00 that has the length of the decompressed file as an unsigned 32 bit integer. After that is the compressed data.

#### LZS Compression

FF7 uses LZS compression on some of their files - more properly, a slightly modified version of LZSS compression as devised by Professor Haruhiko Okumura.

LZS data works on a control byte scheme. So each block in the file begins with a single byte indicating how much of the block is uncompressed ('literal data'), and how much is compressed ('references'). You read the byte right-to-left, with 1=literal, 0=reference.

Literal data means just that: read one byte in from the source (compressed) data, and write it straight to the output.

References take up two bytes, and are essentially a pointer to a piece of data that's been written out (i.e. is part of the data you've already decompressed). LZSS uses a 4K buffer, so it can only reference data in the last 4K of data.

#### Reference format

A reference takes up two bytes, and has two pieces of information in it: offset (where to find the data, or which piece of data is going to be repeated), and length (how long the piece of data is going to be). The two reference bytes look like this:

OOOO OOOO OOOO LLLL (O=Offset, L=Length).

So you get a 12-bit offset and a 4-bit length, but both of these values need modifying to work on directly. The length is easy to work with: just add 3 to it. Why? Well, if a piece of repeated data was less than 3 bytes long, you wouldn't bother repeating it - it'd take up no more space to actually just put literal data in. So all references are at least 3 in length. So a length of 0 means 3 bytes repeated, 1 means 4 bytes repeated, so on. Since we have 4 bits available, that gives us a final length ranging from 3-18 bytes long. (That also means the absolute maximum compression we can ever get using LZSS is a touch under 9:1, since the best possible is to replace 18 bytes of data with two bytes of reference, and then you have to add control bytes as well.)

Offset needs a bit work doing on it, depending on how you're actually holding your data. If all you have is an input buffer and an output buffer, what you really need is an output position in your buffer to start reading data from. In other words, if you've already written 10,000 bytes to your output, you want to know where to retrieve the repeated data from - it could fall anywhere in the past 4K of data, (i.e. from 5904 through to 9999 bytes.)

Here's how you get it:

```
real_offset = tail - ((tail - 18 - raw_offset) mod 4096)
```

Here, 'tail' is your current output position (eg. 10,000), 'raw_offset' is the 12-bit data value you've retrieved from the compressed reference, and 'real_offset' is the position in your output buffer you can begin reading from. This is a bit complex because it's not exactly the way LZSS traditionally does (de) compression; it uses a 4K circular buffer; if you do that, the offset is more or less usable directly.

Once you've got to the start position for your reference, you just copy the appropriate length of data over to your output, and you've dealt with that piece of data.

#### Example

If we're at position 1000 in our output, and we need to read in a new control byte because we've finished with the last one. The next data to look it is:

0x03, 0x53, 0x12 .....

We read in a control byte: $03. In binary, that's 00000011. That informs us that the current block of data has two compressed offsets (@ 2 bytes each), followed by 6 literal data bytes. Once we'd read in the next 10 bytes (the compressed data plus the literal data), we'd be ready to read in our next control byte and start again.

Looking at the first compressed reference, we read in $53 $12. That gives us a base offset of $153 (the 53 from the first byte, and the '1' from the second byte makes up the higher nybble). The base length is $2 (we just take the low nybble of the second byte).

Our final length is obviously just 5. Our position in output is still 1000. So our final offset is:

=1000 - ((1000 - 18 - 339) and $FFF)

The 339 is just $153 in decimal.

The (and $FFF) is a quick way to do modulus 4096.

```
=1000 - (643 and 0xFFF)
=1000 - 643
=357
```

So our final offset is 357. We go to position 357 in our output data, read in 5 bytes (remember the length?), then write those 5 bytes out to our output. Now we're ready to read in the next bit of data (another compressed reference), and do the procedure again...

## Complications

Unfortunately, that doesn't quite cover everything - there's two more things to be aware of when decompressing data that *will* ruin you when using FF7 files, since they do use these features. First, if you end up with an negative offset, i.e. reading data from 'before the beginning of the file', write out nulls (zero bytes). That's because the compression buffer is, by default, initialized to zeros; so it's possible, if the start of the file contains a run of zeros, that the file may reference a block you haven't written...

EG: If you're at position 50 in your output, it's possible you may get an offset indicating to go back 60 bytes to offset -10! If you have to read 5 bytes from there, it's simple: you just write out 5 nulls. However, you *could* have to read 15 bytes from there. In that case, you write out 10 nulls (the part of the data 'before' the file start), then the 5 bytes from the beginning of the file.

Secondly, you can have a repeated run. This is almost the opposite problem: when you go off the end of your output. Say you're at offset 100 in your output, and you have to go to offset 95 to read in a reference. That's OK ... but what if the reference length is >5? In that case, you loop the output. So if you had to write out 15 bytes, you'd write out the five bytes that *were* available ... and then write them out again ... then again, to make up the 15 bytes you needed.

The FF7 files use both of these 'tricks', so you can't ignore them!

<!-- END EXTRACTION -->

### LGP Archives {#lgp_archives}

The LGP file format is only used for the PC port of Final Fantasy 7. These are large \"volume\" type archives that hold most of the game\'s data. These archives can hold thousands of files. Unlike the BIN or LZS type files, this archive does reference the data within it by filename. Its file format is explained [here](FF7/LGP_format "here"){.wikilink}.

## Textures

A texture is just a picture that is placed into video memory. It is later manipulated by the engine and displayed on the screen. The native format of a texture was the Psy-Q [TIM](PSX/TIM_format "TIM"){.wikilink} (Texture Image Map). This is used as the native format for the PSX version as well, with a few caveats explained below. The file can hold multiple color look up tables. This was one of the reasons why a video card on the PC that could do palleted data at high color depths was needed.

### TIM texture data format for PSX {#tim_texture_data_format_for_psx}

The [TIM files](PSX/TIM_format "TIM files"){.wikilink} are found both on raw format and also within several archives, including [BIN](FF7/Kernel/Low_level_libraries#BIN_archive_data_format "BIN"){.wikilink}, [LZS](FF7/Kernel/Low_level_libraries#LZS_Archives "LZS"){.wikilink}, or even MNU. The format proper has the ability to contain 24 bit bitmaps, but is not used in FF7. The format was created because the PSX does not have direct access to it\'s VRAM, and must go through the [GPU](PSX/GPU "GPU"){.wikilink} for any graphic access. [A TIM file](PSX/TIM_format "A TIM file"){.wikilink} is a clean way to load a texture and color look up table into VRAM.

### TEX texture data format for the PC {#tex_texture_data_format_for_the_pc}

TEX files are texture files for the PC. The format for these files are located [here](FF7/TEX_format "here"){.wikilink}.

## File formats for 3D models {#file_formats_for_3d_models}

During the development process, 3D models contain a good deal of information needed by the artist every time they save or load the model. When the model is finished, it is often exported and broken up into smaller files with many unneeded attributes stripped from them. When the models for FF7 were created, they were exported into Psy-Q\'s 3D library formats. These include [resource data (.RSD)](PSX/RSD "resource data (.RSD)"){.wikilink}, polygon data (.PLY), polygon groups (.GRP), materials (.MAT), [textures (.TIM)](PSX/TIM_file "textures (.TIM)"){.wikilink}, [skeletal hierarchy (.HRC)](PSX/HRC "skeletal hierarchy (.HRC)"){.wikilink}, and animation (.ANM).

The models are handled differently between modules. The models in the \"battle\" modules have a different animation system than the field models. When the models were converted to the PC version, they were taken from the Psy-Q formats to a more PC-friendly one. Some are even the original, uncompiled, Psy-Q files.

### Model formats for PSX {#model_formats_for_psx}

The Playstation models are stored in the following directories, \\ENEMY1 \\ENEMY2 \\ENEMY3 \\ENEMY4 \\ENEMY5 \\ENEMY6 (battle models), \\FIELD (field models and field character models), \\MAGIC (Summon magic), and \\STAGE1 \\STAGE2 (battle scenes). Battle model names for special characters and party characters are stored in \\ENEMY6, all models of this type end in an .LZS extension. The same goes with summon magic used they are stored with there animations etc. in \\MAGIC with a .LZS extension. The only exception to this extension is the FIELD models, which use the extensions BSX and BCX for scene models and character models respectively. The [Playstation battle model format](FF7/Playstation_Battle_Model_Format "Playstation battle model format"){.wikilink}, is different than the [Playstation field model format](FF7/Field/BSX "Playstation field model format"){.wikilink}, also the [FF7/Playstation battle scene format](FF7/Playstation_battle_scene_format "FF7/Playstation battle scene format"){.wikilink}, is similiar but not identical to the [Playstation battle model format](FF7/Playstation_Battle_Model_Format "Playstation battle model format"){.wikilink}. The [Playstation magic model](FF7/Playstation_magic_model "Playstation magic model"){.wikilink} format is a work in progress.

### Model Formats for PC {#model_formats_for_pc}

The PC models are stored in the LGP files in the /DATA directory. The names for the models were obfuscated a little. The data can be found in the [Hierarchy files (.HRC)](PSX/HRC "Hierarchy files (.HRC)"){.wikilink}, [Resource data files (.RSD)](PSX/RSD "Resource data files (.RSD)"){.wikilink}, and [Polygon files (.P)](FF7/P "Polygon files (.P)"){.wikilink}.
