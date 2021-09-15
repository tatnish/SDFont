#@micropython.native

#_DEBUG = True

import sys
from m5stack import lcd
import uiflow

sys.path.append("/sd/fonts")

# module private variables (Do not access from outside)
_font = None
_name = ""
_transparency = False
_height = 0
_hmap = False
_reverse = False
_screensize = lcd.screensize()
_baseline = 0
_descent = 0
_cjk_height = 0
_max_width = 0

# These values may be set by blockly (due to limitation of mpy-cross)
_wipe_delay = 0
_line_delay = 5
_page_delay = 1500


# CONSTANT
EFFECT_NONE=0
EFFECT_WIPE=1
EFFECT_TYPEWRITER=2

#
# load font module
# 
def load(font_module):
    global _font, _height, _hmap, _reverse, _baseline, _descent, _cjk_height, _max_width, _name
    try:
        _font = __import__(font_module) # import font module 
    except Exception as e: 
        print(e)
        print("Font load error: " + font_module)
    else:
        _name = font_module
        _height = _font.height()
        _hmap = _font.hmap()
        _reverse = _font.reverse()
        _baseline = _font.baseline()
        _descent = _height - _baseline
        _cjk_height = _height - int(_descent * 0.65)
        _max_width = _font.max_width()

# horizontally render a character dots ony by one
# FIXME: is there any effective means of drawing a char like framebuffer?
def render_char(x, y, color, bg, ch, effect=EFFECT_WIPE):
    global _wipe_delay, _font, _height
    data, _, width = _font.get_ch(ch)

    if (effect == EFFECT_TYPEWRITER):
        target_x = x
        target_y = y
        lcd.sprite_create(width, _height, lcd.SPRITE_16BIT)
        lcd.sprite_select()
        x = 0
        y = 0

    bytes_per_col = (_height - 1) // 8 + 1
    for col in range(width):
        _x = x + col
        offset = col * bytes_per_col
        for row in range(_height):
            byte = data[offset + row // 8]
            if (_reverse):
                bit = (byte & (1 << (7-(row % 8)))) > 0
            else:
                bit = (byte & (1 << (row % 8))) > 0
            if (bit):
                lcd.pixel(_x, y+row, color)
            elif (not _transparency):
                lcd.pixel(_x, y+row, bg)
        if (effect != EFFECT_NONE and _wipe_delay > 0):
            uiflow.wait_ms(_wipe_delay)

    if (effect == EFFECT_TYPEWRITER):
        lcd.sprite_deselect()
        lcd.sprite_show(target_x, target_y)
        lcd.sprite_delete()

    return width

# vertically render a character dots ony by one
# FIXME: is there any effective means of drawing a char like framebuffer?
def render_char_vertical(x, y, color, bg, ch, effect=EFFECT_WIPE):
    global _wipe_delay, _max_width
    data, _, width = _font.get_ch(ch)

    if (effect == EFFECT_TYPEWRITER):
        target_x = x
        target_y = y
        lcd.sprite_create(width, _height, lcd.SPRITE_16BIT)
        lcd.sprite_select()
        x = 0
        y = 0

    bytes_per_col = (_height - 1) // 8 + 1
    for row in range(_height):
        for col in range(width):
            _x = x + col
            offset = col * bytes_per_col
            byte = data[offset + row // 8]
            if (_reverse):
                bit = (byte & (1 << (7-(row % 8)))) > 0
            else:
                bit = (byte & (1 << (row % 8))) > 0
            if (bit):
                    lcd.pixel(_x, y+row, color)
            elif (not _transparency):
                lcd.pixel(_x, y+row, bg)
        if (effect != EFFECT_NONE and _wipe_delay > 0):
            uiflow.wait_ms(_wipe_delay)

    if (effect == EFFECT_TYPEWRITER):
        lcd.sprite_deselect()
        lcd.sprite_show(target_x, target_y)
        lcd.sprite_delete()
    return getLetterHeight(ch)


# get a width of a character
def getLetterWidth(ch):
    data, _, width = _font.get_ch(ch)
    return width

# get a actual letter height for vertical layout
def getLetterHeight(ch):
    if (not ch in "fjgpqyｆｊｇｐｑｙ{|}[]/\;" and _descent >= 3):
        return _cjk_height
    else:
        return _height

# determine the width of the string for Horizontal Layout
def getTextWidth(string):
    width = 0
    for ch in string:
        width += getLetterWidth(ch)
    return width

# determine the height of the string for Vertical Layout
def getTextHeight(string):
    height = 0
    for ch in string:
        height += getLetterHeight(ch)
    return height

# returns the x starting position for aligning string to the horizontal center
def getX4Center(string):
    return (_screensize[0] - getTextWidth(string)) // 2

# returns the Y starting position for aligning string to the vertical center
def getY4Center(string):
    return (_screensize[1] - _height) // 2

# draw text using a loaded font
# It draws each letter graphics dot by dot. 
# it looks like a rolling text news on a train
def draw_text(x, y, string, color=None, effect=EFFECT_WIPE):
    global _wipe_delay
    bg = lcd.get_bg()
    if (color == None): 
	    color = lcd.get_fg()
    width = getTextWidth(string)
    if (x == lcd.CENTER):
        _x = getX4Center(string)
    else:
        _x = x
    if (y == lcd.CENTER):
        _y = getY4Center(string)
    else:
        _y = y

    if (effect == EFFECT_NONE):  # use sprite to draw text without wipe effect
        lcd.sprite_create(width, _height, lcd.SPRITE_16BIT)
        lcd.sprite_select()
        target_x = _x
        target_y = _y
        _x = 0
        _y = 0

    for ch in string:
       _x += render_char(_x, _y, color, bg, ch, effect)

    if (effect == EFFECT_NONE): 
        lcd.sprite_deselect()
        lcd.sprite_show(target_x, target_y)
        lcd.sprite_delete()

# draw text vertically using a loaded font
# It draws each letter graphics dot by dot. 
# it looks like a rolling text news on a train
def draw_vtext(x, y, string, color=None, effect=EFFECT_WIPE):
    global _max_width
    bg = lcd.get_bg()
    if (color == None): 
	    color = lcd.get_fg()
    height = getTextHeight(string)
    if (x == lcd.CENTER):
        _x = (_screensize[0] - _max_width) // 2
    else:
        _x = x
    if (y == lcd.CENTER):
        _y = (_screensize[1] - height) // 2
    else:
        _y = y

    if (effect == EFFECT_NONE):  # use sprite to draw text without wipe effect
        lcd.sprite_create(_max_width, height, lcd.SPRITE_16BIT)
        lcd.sprite_select()
        target_x = _x
        target_y = _y
        _x = 0
        _y = 0

    for ch in string:
        _y += render_char_vertical(_x, _y, color, bg, ch, effect)

    if (effect == EFFECT_NONE): 
        lcd.sprite_deselect()
        lcd.sprite_show(target_x, target_y)
        lcd.sprite_delete()

# print text using sprite buffer
# this doesn't have a rolling effect but it takes longer before it is shown on screen
# since it all draws 
#def draw_text_buf(x,y, string, color=None):
#    global _wipe_delay
#    width = getTextWidth(string)
#    height = _height
#    last_delay = _wipe_delay
#    _wipe_delay = 0
#
#    lcd.sprite_create(width, height, lcd.SPRITE_16BIT) # Create buffer for string area
#    lcd.sprite_select() # draing to lcd will be written to sprite buffer while selected
#
#    draw_text(0,0, string, color) # draw text to sprite buffer
#    lcd.sprite_deselect() # deselecting sprite will make lcd back to normal
#
#    if (x == lcd.CENTER):
#        x = getX4Center(string)
#    if (y == lcd.CENTER):
#        y = getY4Center(string)
#
#    lcd.sprite_show(x, y) # draw sprite on lcd
#    lcd.sprite_delete()
#    _wipe_delay = last_delay

# draw multi-line text horizontally in a given rect
def draw_text_in_rect(rect_x, rect_y, rect_width, rect_height, string, color, bg, effect=EFFECT_WIPE):
    global _line_delay, _page_delay
    y = rect_y
    lcd.fillRect(rect_x, rect_y, rect_width, rect_height, bg)
    buf = ""
    width = 0
    for ch in string:
        dx = getLetterWidth(ch)
        buf += ch
        width += dx
        if (width > rect_width - _max_width or ch == "。" ):
            draw_text(rect_x, y, buf, color, effect)
            y+= _height
            buf=""
            width=0
            if (_line_delay > 0):
                uiflow.wait_ms(_line_delay)
        if (y > rect_y + rect_height - _height):
            y = rect_y
            uiflow.wait_ms(_page_delay)
            lcd.fillRect(rect_x, rect_y, rect_width, rect_height, bg)
    if (buf != ""):
        draw_text(rect_x, y, buf, color, effect)
        
    

# draw multi-line text vertically in a given rect
def draw_vtext_in_rect(rect_x, rect_y, rect_width, rect_height, string, color, bg, effect=EFFECT_WIPE):
    global _line_delay, _page_delay
    max_width = _max_width + 2
    x = rect_x + rect_width - max_width
    lcd.fillRect(rect_x, rect_y, rect_width, rect_height, bg)
    buf = ""
    height = 0
    for ch in string:
        dy = getLetterHeight(ch)
        buf += ch
        height += dy
        if (height > rect_height - dy or ch == "。"):
            draw_vtext(x, rect_y, buf, color, effect)
            x-= max_width
            buf=""
            height=0
            if (_line_delay > 0):
                uiflow.wait_ms(_line_delay)
        if (x < rect_x):
            x = rect_x + rect_width - max_width
            uiflow.wait_ms(_page_delay)
            lcd.fillRect(rect_x, rect_y, rect_width, rect_height, bg)
    if (buf != ""):
        draw_vtext(x, rect_y, buf, color, effect)

# set delay msec between drawing a font line
#def set_delay(msec):
#    global _wipe_delay
#    _wipe_delay = msec
