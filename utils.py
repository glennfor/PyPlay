
#[SOUNDS]
import pygame
import pygame.locals 

'''
The main pygame modules for playing sound $$ below
pygame.mixer 
pygame.mixer.Sound 
pygame.mixer.music

use pyglet or more dedicated sound module later
'''

#[UI]
import tkinter
import tkinter.ttk as ttk
import tkinter.filedialog
import tkinter.messagebox
import ttkthemes
import tkinter.tix as tix



#[UTILS]

import PIL
from PIL import ImageTk, Image

import random  
import os
import sys
import datetime
import time

import threading  

#constants

SUPPORTED_EXTENSIONS = ['.mp3', '.wav', '.ogg', '.wma'] #'.m4a
PATH_TO_SAMPLE_MUSIC = './assets/sample'
PATH_TO_ICON = './assets/UIicons/icon.ico'
PATH_TO_CANVAS_IMAGE = './assets/UIicons/music_player.ico'


#[tooltips]

class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tip_win = None

    def showtip(self, tip):
        '''display text in a tooltip window'''
        if self.tip_win or not tip:
            return

        x,y,cx,cy = self.widget.bbox(tkinter.INSERT)
        x += self.widget.winfo_rootx() +25
        y += cy + self.widget.winfo_rooty() +25
        self.tip_win = tw = tkinter.Toplevel(self.widget)
        tw.overrideredirect(True)  #remove all WM decorations
        tw.wm_geometry('+%d+%d'%(x, y))
        tkinter.Label(tw, text = tip, justify = tkinter.LEFT, bg = '#FFFFE0', relief = tkinter.SOLID,
              borderwidth = 1, font = ('tahoma', 8, 'normal')).pack(ipadx = 1)

    def hidetip(self):
            tw = self.tip_win
            self.tip_win = None
            if tw:
                tw.destroy()


def create_tool_tip(widget, tip_text):
    tooltip = ToolTip(widget)

    def enter(ev):
        tooltip.showtip(tip_text)

    def leave(ev):
        tooltip.hidetip()
    widget.bind('<Enter>', enter,add='+')
    widget.bind('<Leave>', leave, add='+')