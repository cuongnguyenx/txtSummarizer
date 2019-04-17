import tkinter as tk
import config


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self['background']
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        if self['foreground'] == config.button_text_color:
            self['background'] = config.active_small_button_color
        else:
            self['background'] = config.active_big_button_color

    def on_leave(self, e):
        self['background'] = self.defaultBackground
