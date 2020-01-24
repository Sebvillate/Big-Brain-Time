# --------------------------------------------------------------------
# Program: Label Classes
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Classes for displaying text on a pygame surface.
# --------------------------------------------------------------------

import pygame
pygame.init()

# alignment constants
LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
CENTER = 0.5


# scalable class for easily drawable text
class Label:
    def __init__(self, text, x=0, y=0, font="lucida bright", size=18, color=(0, 0, 0), visible=True):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font = font
        self.size = size
        self.label = self.render_label()
        self.visible = visible

    def draw(self, win):
        if self.visible:
            win.blit(self.label, (self.x, self.y))

    # return rendered label's text as a drawable
    def render_label(self):
        return pygame.font.SysFont(self.font, self.size).render(self.text, True, self.color)

    def center(self, xy):
        self.set_x(xy[0] - self.get_width()//2)
        self.set_y(xy[1] - self.get_height()//2)

    # --------------------SETTER AND GETTER METHODS--------------------

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_size(self, size):
        self.size = size
        self.label = self.render_label()

    def get_width(self):
        return self.label.get_width()

    def get_height(self):
        return self.label.get_height()

    def set_text(self, text):
        self.text = text
        self.label = self.render_label()

    def set_color(self, color):
        self.color = color
        self.label = self.render_label()

    def set_visible(self, b):
        self.visible = b


# sub class of label with a filled rectangular background
class FilledLabel(Label):
    def __init__(self, rect, text, font="lucida bright", size=18, color=(0, 0, 0),
                 fColor=(255, 255, 255), border=0, bColor=(0, 0, 0), thAlign=CENTER, tvAlign=CENTER):
        super().__init__(text, 0, 0, font, size, color)
        self.rectx, self.recty, self.w, self.h = rect
        # text alignment in rectangle
        self.thAlign = thAlign
        self.tvAlign = tvAlign
        self.set_x(self.rectx + (self.w - self.get_width()) * thAlign)
        self.set_y(self.recty + (self.h - self.get_height()) * tvAlign)

        self.fillRect = self.rectx + border, self.recty + border, self.w - 2 * border, self.h - 2 * border
        self.fColor = fColor
        self.border = border  # border width
        self.bColor = bColor

    def draw(self, win):
        if self.visible:
            if self.border != 0:
                pygame.draw.rect(win, self.bColor, self.get_rect())
            pygame.draw.rect(win, self.fColor, self.fillRect)
            super().draw(win)

    # returns rect tuple
    def get_rect(self):
        return self.rectx, self.recty, self.w, self.h

    # updates text position based on alignment (used when changing text size, alignment, etc.)
    def update_text_pos(self):
        self.set_x(self.rectx + (self.w - self.get_width()) * self.thAlign)
        self.set_y(self.recty + (self.h - self.get_height()) * self.tvAlign)
