# SDFont micropython module for M5Stack

This repository defines a means of using CJK (Chinese, Japanese, and Korean) fonts on M5Stack with UiFlow, especially focusing on Japanese fonts.

日本語説明は[こちら](./README_jp.md)

# 1. Introduction
UiFlow is a good programing environement for youth and light coders, but it hadn't supported CJK (Chinese, Japanese, and Korean) fonts. From UiFlow v1.8.x, it has provided unicode font, but it is limited for the UI label, and 24px is the only available size. There are some solutions to use CJK fonts for Arduino Library, but it is not an easy solutions for beginners and very young programmers. I tried some hacks to find out how to use Japanese fonts on UiFlow, but it seems impossible so far, so I decided to make my own micropython module to support it. 

# 2. Features
SDFont module is a micropython module that provides the basic and some advanced functions for drawing text using CJK fonts. The major features are as follows:

 1. Loading fonts from SD-card
 2. Horizontal / vertical text drawing
 3. Wipe / typewriter effect
 4. Mult-line text drawing in rectangle
 5. Multi-page text drawing in rectangle
 6. Adjustable drawing speed
 7. Adjustable pause time between lines / pages
 8. UiFlow custom blocks for SDFont module

SDFont uses a special font data written as a micropython code. You can place a font file in SD card.


# 3. How to prepare CJK Fonts
First of all, you need to prepare a CJK font for SDFont module. An easy solution is to convert your favorite TrueType fonts or OpenType fonts to a font data for SD card. There is a very handy python script [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py) to do it for you. This script is originally created by peterhinch, and I modified it to properly handle large number of characters for CJK fonts. Here is a brief instruction to download this tool on Windows and Linux.

## 3.1 How to prepare a font converter

### Windows 10

 1. Download python3 (for now the latest is python 3.9) from Microsoft Store
 2. Download [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py) to your computer (assume it is on C:\App\font-to-py)
 3. Launch Command Prompt or Windows PowerShell.
 4. Install free-type python module by the following command
   `pip3 install freetype-py`
 5. install mpy-cross, a cross compiler for python
   `pip3 install mpy-cross`
 6. copy font-to-py.py file to "tools" folder of the local copy of this repository

### Linux (Ububtu)

The following commands will install python and freetype python module.
 `apt install python3`
 `pip3 install freetype-py`
 `pip3 install mpy-cross`
 `git clone https://github.com/tatnish/SDFont.git
 `cd tools`
 `git clone https://github.com/tatnish/micropython-font-to-py.git`
 `cp micropython-font-to-py-master/*.py .`
 
## 3.2 How to convert fonts (horizontal layout)

 1. Prepare a text file that contains characters to convert
 You can use [tools/jisx0208.py](./tools/jisx0208.py) to create ASCII & Japanese characters
   `python3 jisx0208.py > chars.txt`
 2. Download your favorite TrueType/OpenType font file
 3. Convert font file to python file using  [micropython-font-to-py](https://github.com/tatnish/micropython-font-to-py). The following command will create 24px font data for somefont.ttf
   `python3 font_to_py.py -k chars.txt somefont.ttf 24 somefont24.py`
  4. compile .py file to mpy using mpy-cross
    `mpy-cross -O3 somefont24.py -march=xtensawin -X emit=native -somefont24.py -X heapsize=8000000`
  
  Now you have somefont24.mpy. 
  Note: Increase value for heapsize=xxxxxxxx when you get memory allocation error

## 3.3 How to convert fonts (vertical layout)

You need to make a subset font file of a TrueType/OpenType font file for vertical layout using [サブセットフォントメーカー (subset font maker)](https://opentype.jp/subsetfontmk.htm) first. The following steps will create one for you.

1. Download [subset font maker](https://opentype.jp/bin/subsetfont320.msi)
2. Select a font file to convert into by selecting "参照" button
3. Name output font path into "作成後のフォントファイル(D)"
4. Copy & Pase all the characters in chars.txt into "フォントに格納するファイル(C)" textbox on subset font maker window.
	- You can create chars.txt using [tools/jisx0208.py](./tools/jisx0208.py)
5. Select 縦書き(V) (vertical layout) at 文字組方向(A) checkbox.
6.  Uncheck "書体名を変更する(G)" (=Change font name) 
7. Click "作成開始 (Start Creation)" button
8. Follow "3.2 How to convert fonts (horizontal layout)" using a file made with subset font maker.
 
# 4. How to install SDFont modules and fonts

1. compile [sdfont.py](./tools/sdfont.py) by the following command 
  `mpy-cross -O3 sdfont.py -march=xtensawin -X emit=native -X heapsize=8000000` 
2. copy sdfont.mpy and your font's .mpy files into "fonts" folder on your SD-card

Note: The **fonts** folder must be created under the root folder of the SD-card

# 5. How to use fonts in UiFlow (Demo)

You can use [UiFlow](http://flow.m5stack.com) to create some M5Stack app. 
Here is a easy step to run a demo program here.

 - Insert the SD card to M5Stack. The SD card contains the following files in /fonts/ folder 
     - sdfont.mpy
     - font files (*.mpy)
         - [Klee One](./examples/demo/KleeOne24jp.mpy)
         - [Pixel-M-PLUS12R](./examples/demo/Pixel-M-PLUS12R-24jp.mpy)
         - [Stick B](./examples/demo/Stick40jp.mpy)
     - [title.jpg](./examples/demo/title.jpg)
     - [RPGMap.jpg](./examples/demo/RPGMap.jpg)
  2. Open [UiFlow]((http://flow.m5stack.com) on your browser
  3. choose API Key for your M5Stack core2.
  4. Add the following 2 custom blocks for SDFont module to UiFlow
	 - [Graphics.m5b](./uiflow/Graphics.m5b)
	 - [SDFont.m5b](./uiflow/SDFont.m5b)
  5. Open a demo app [SDFontDemo.m5f](./examples/demo/SDFontDemo.m5f)(./examples/demo/SDFontDemo.m5f) 
  6. Press "▶(Play)" button on the menu bar to go.

You can learn how to use fonts by seeing the blocks in this demo. You can also refer the block reference in section 6.

# 6. How to use Custom Blocks for SDFont

### loadFont

sdfont.load("yourfont").

You can add a text block to specify your font file. you must place the fonts in /fonts folder in an SD-card. You must specify the base file name for the font.
e.g. somefont24 for somefont24.mpy file.

### print

This block draws a text on the LCD horizontally. The following arguments are to be filled.

- text: **string**: text to draw
- x: **number**: x position of the left-top point  
- y: **number**: y position of the left-top point
- effect: **number**: use one of the following blocks
	- None: no effect. each line of text will be drawn in turn. 
	- Wipe Effect: Each character will be drawn line by line
	- Typewriter Effect: Each character will be shown one by one

### vprint

This block draws a text on the LCD horizontally. The following arguments are to be filled.

- text: **string**: text to draw
- x: **number**: x position of the left-top point  
- y: **number**: y position of the left-top point
- effect: **number**: use one of the following blocks
	- None: no effect. each line of text will be drawn in turn. 
	- Wipe Effect: Each character will be drawn line by line
	- Typewriter Effect: Each character will be shown one by one

### printInRect

This block draws a long text horizontally in a give rectangle. This block will automatically change page for long text.

- text: **string**: long text to draw. you can specify entire book story here.  
- x: **number**: x position of the left-top point  
- y: **number**: y position of the left-top point
- width: **number**: width of a rectangle
- height: **number**: height of a rectangle
- color: **number**: color valur (e.g. 0xffffff for white)
	- You can use one of color blocks (like WHITE color) in Graphics custom block.
- effect: **number**: use one of the following blocks
	- **No Effect**: no effect. each line of text will be drawn in turn. 
	- **Wipe Effect**: Each character will be drawn line by line
	- **Typewriter Effect**: Each character will be shown one by one

### vprintInRect

This block draws text vertically in a given rectangle. 
parameters are the same as printInRect.

You should use .mpy font file that is made for vertical layout, You can make one using the steps in section 3.3

### setWipeDelay

This block specifies the delay (msec) for Wipe Effect. specifying 1 or 2 will make a good pause for showing the effect. specifying 5 will make a drawing very slow. The delay value is used by print, vprint, printInRect, and vprintInRect blocks.

- Parameter: **number** delay amount in milliseconds

### setLineDelay

This block specifies the the delay (msec) between lines.
This delay value is used by printInRect and vprintInRect block.

- Parameter: ** number** delay amount in milliseconds

### setPageDelay

This block specifies the delay (msec) between pages. This delay value is used by printInRect.

- Parameter: **number**: delay amount in milliseconds

### 

### Wipe Effect, Typewritter Effect, and No Effect

These blocks are used to specify an effect parameter for print, vprint, printInRect, vprintInRect blocks.

- **No Effect**: no effect. each line of text will be drawn in turn. 
- **Wipe Effect**: Each character will be drawn line by line
- **Typewriter Effect**: Each character will be shown one by one

### CENTER

This block specifies that the text will be drawn at the center of the LCD. This can be used for both x, and y parameters for **print**, **vprint**, **printInRect**, and **vprintInRect**  blocks.

This block is equivalent to `lcd.block` in micropython.

### textWidth

This block returns a length of a given text in pixel when using a font loaded by **loadFont** block.

- Parameter: **string**: a text

# Limitation

This module is written in micorpython and thus the speed is very slow.
The text drawing takes some milliseconds, and the font loading takes about a few seconds to 10 seconds
depending on the size of the font.

The font data in .mpy is not frozen since it is not included in the firmware, the memory usage is very high.
Therefore loading multiple fonts or a large size font may cause memory allocation error.
When the allocation error occurs, either last loaded file is used or an error "get_ch is not defined" happens.

