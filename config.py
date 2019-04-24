import math

center_label_font = ''
titlefont_sum = ''
keyfont_sum = ''
contentfont_sum = ''
slider_label_font = ''
button_font = ''
multilistbox_font = ''
listbox_font = ''
arrow_font = ''
sun_font = ''

curr_width = 1920
curr_height = 1080
ratio_w = 1
ratio_h = 1

bg_color = 'gray82'
button_color = 'gray27'

big_button_color = 'white'
active_big_button_color = 'gray90'
active_small_button_color = 'gray15'

entry_color = '#eff1e7'
inverted_entry_color = '#0c0c0c'
button_text_color = 'ghost white'
button_color_gen = 'medium blue'

slider_color = '#c0c0c0'
slider_label_fg = 'gray25'
slider_label_bg = '#eff1e7'

title_text_color = "black"
title_key_color = "gray32"
title_text_inverted_color = "gray95"
title_key_inverted_color = "gray90"


def generate_fonts(ratio_w, ratio_h):
    print(ratio_w)
    global center_label_font, titlefont_sum, keyfont_sum, contentfont_sum, slider_label_font, button_font, \
           multilistbox_font, listbox_font, arrow_font, sun_font
    center_label_font = "\"Yu Gothic Demibold\" %d bold" % int(30*ratio_w)

    titlefont_sum = "\"Times New Roman\" %d bold" % int(28*ratio_w)
    keyfont_sum = "\"Yu Gothic UI Light\" %d italic" % int(14*ratio_w)
    contentfont_sum = "\"Palatino Linotype\" %d" % int(18*ratio_w)  # (family="Yu Gothic Medium", size=30)

    slider_label_font = "\"Yu Gothic Demibold\" %d bold" % int(12*ratio_w)
    button_font = "\"Yu Gothic UI\" %d bold" % int(20*ratio_w)
    multilistbox_font = "\"Yu Gothic UI\" %d" % int(14*ratio_w)
    listbox_font = "\"Yu Gothic UI\" %d" % math.ceil(18*ratio_w)
    arrow_font = "\"Yu Gothic UI\" %d bold" % int(24*ratio_w)
    sun_font = "\"Yu Gothic UI\" %d bold" % int(20 * ratio_h)




