# --------------------------------------------------------------------
# Program: Frame Class
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Class for storing and processing all drawable and
#   button of a current screen. Used for storing different screens
#   such as menus and game screens.
# --------------------------------------------------------------------

import pygame
import vector
import color as c

# constants
FIXED = 0
RELATIVE = 1
WRAP = 0
MATCH = 1

top_drawables = []


# frame class for storing and processing current drawables and buttons
class Frame:
    def __init__(self, drawables, button_list=None, fill=(255, 255, 255)):
        self.drawables = drawables
        if button_list is None:
            button_list = []
        self.button_lists = button_list
        self.fill = fill

    def draw(self, win):
        win.fill(self.fill)
        for d in self.drawables:
            d.draw(win)

    # process buttons
    def process_events(self, click_bool, release_bool, mouse_pos):
        for button_list in self.button_lists:
            button_list.process_events(click_bool, release_bool, mouse_pos)

    def add(self, drawable):
        self.drawables.append(drawable)

    # return surface object with the current screen of the frame
    def get_screen(self, w, h):
        surf = pygame.Surface((w, h))
        self.draw(surf)
        return surf

    def __add__(self, other):
        return Frame(self.drawables + other.drawables, self.button_list + other.button_list, self.fill)


# concrete class for storing relative layout attributes
class RelativeLayout:
    """stores all information about relative layout of drawables"""
    def __init__(self):
        self.w = WRAP
        self.h = WRAP
        self.margin_left = 0
        self.margin_right = 0
        self.margin_top = 0
        self.margin_bottom = 0
        self.gravity = ""
        self.align_top = None
        self.align_bottom = None
        self.align_left = None
        self.align_right = None

    def set_margin(self, value):
        self.margin_left = value
        self.margin_right = value
        self.margin_top = value
        self.margin_bottom = value


# abstract drawable class
class Drawable:
    """abstract class for objects that can be displayed using a relative layout"""
    def __init__(self, parent=None, layout_type=FIXED):
        self.parent = parent
        self.get_x = self.get_x_default
        self.get_y = self.get_y_default
        if type(parent) is pygame.Surface:
            self.rect = vector.Rect(0, 0, self.parent.get_width(), self.parent.get_height())
            self.get_w = self.parent.get_width
            self.get_h = self.parent.get_height
        else:
            self.rect = vector.Rect(0, 0, 10, 10)
            self.get_w = self.get_w_default
            self.get_h = self.get_h_default
        self.layout_type = layout_type
        self.layout = RelativeLayout()
        self.draw_top = False
        self.w_fraction = 1
        self.h_fraction = 1

    def set_parent(self, parent):
        self.parent = parent

    def set_layout_type(self, layout_type):
        self.layout_type = layout_type

    def set_relative_rect(self):
        if self.layout_type == RELATIVE:
            if self.layout.align_top is not None:
                drawable = self.parent.find(self.layout.align_top)
                self.rect.y = drawable.get_y() + drawable.get_h() + drawable.layout.margin_bottom + self.layout.margin_top
            elif self.layout.align_bottom is not None:
                drawable = self.parent.find(self.layout.align_bottom)
                self.rect.y = drawable.get_y() - self.get_h() - self.layout.margin_bottom - drawable.layout.margin_top
            elif "top" in self.layout.gravity:
                self.rect.y = self.parent.get_y() + self.layout.margin_top
            elif "bottom" in self.layout.gravity:
                self.rect.y = self.parent.get_y() + self.parent.get_h() - self.layout.margin_bottom - self.get_h()
            elif "centery" in self.layout.gravity:
                self.rect.y = self.parent.get_y() + (self.parent.get_h() - self.get_h())//2
            else:
                self.rect.y = self.parent.get_y()
            self.rect.y += self.layout.margin_top
            if self.layout.align_left is not None:
                drawable = self.parent.find(self.layout.align_left)
                self.rect.x = drawable.get_x() + drawable.get_w() + drawable.layout.margin_right + self.layout.margin_left
            elif self.layout.align_right is not None:
                drawable = self.parent.find(self.layout.align_right)
                self.rect.x = drawable.get_x() - self.get_w() - self.layout.margin_right - drawable.layout.margin_left
            elif "left" in self.layout.gravity:
                self.rect.x = self.parent.get_x() + self.layout.margin_left
            elif "right" in self.layout.gravity:
                self.rect.x = self.parent.get_x() + self.parent.get_w() - self.layout.margin_right - self.get_w()
            elif "centerx" in self.layout.gravity:
                self.rect.x = self.parent.get_x() + (self.parent.get_w() - self.get_w())//2
            else:
                self.rect.x = self.parent.get_x()
            self.rect.x += self.layout.margin_left

            if self.layout.w == MATCH:
                if self.w_fraction is not 1:
                    self.rect.w = int((self.parent.get_w() - self.layout.margin_left - self.layout.margin_right) / self.w_fraction)
                elif self.get_x() != self.parent.get_x():
                    self.rect.w = self.parent.get_w() - self.layout.margin_left - self.layout.margin_right - self.rect.x + self.parent.get_x()
                else:
                    self.rect.w = self.parent.get_w()
            else:
                self.get_w()
            if self.layout.h == MATCH:
                if self.h_fraction is not 1:
                    self.rect.w = int((self.parent.get_h() - self.layout.margin_top - self.layout.margin_bottom + self.parent.get_y()) / self.h_fraction)
                elif self.get_y() != self.parent.get_y():
                    self.rect.h = self.parent.get_h() - self.layout.margin_top - self.layout.margin_bottom - self.rect.y + self.parent.get_y()
                else:
                    self.rect.h = self.parent.get_h()
            else:
                self.rect.h = self.get_h()

    def update_screen(self, new_win):
        self.parent = new_win

    # --------------------SETTER AND GETTER METHODS--------------------

    def get_x_default(self):
        return self.rect.x

    def get_y_default(self):
        return self.rect.y

    def get_w_default(self):
        if self.layout.w == MATCH:
            if self.w_fraction is not 1:
                self.rect.w = int((self.parent.get_w() - self.layout.margin_left - self.layout.margin_right) / self.w_fraction)
            elif self.get_x() != self.parent.get_x():
                self.rect.w = self.parent.get_w() - self.layout.margin_left - self.layout.margin_right - self.rect.x + self.parent.get_x()
            else:
                self.rect.w = int(self.parent.get_w() / self.w_fraction)
        return self.rect.w

    def get_h_default(self):
        if self.layout.h == MATCH:
            if self.h_fraction is not 1:
                self.rect.w = int((self.parent.get_h() - self.layout.margin_top - self.layout.margin_bottom + self.parent.get_y()) / self.h_fraction)
            elif self.get_y() != self.parent.get_y():
                self.rect.h = self.parent.get_h() - self.layout.margin_top - self.layout.margin_bottom - self.rect.y + self.parent.get_y()
            else:
                self.rect.h = self.parent.get_h()
        return self.rect.h

    def get_rect(self):
        return self.get_x(), self.get_y(), self.get_w(), self.get_h()

    def set_relative(self, parent):
        self.layout_type = RELATIVE
        self.rect.x = 0
        self.rect.y = 0
        self.parent = parent
        parent.add(self)


# concrete component class to store drawable groups
class Component(Drawable):
    """drawable designed to contain other drawables
    acts as a frame to be used for relative layout of contained drawables"""
    def __init__(self, parent, layout_type=FIXED, background_color=c.WHITE):
        super().__init__(parent, layout_type)
        self.contents = []
        self.background_color = background_color
        self.background = self.blank_background
        self.scrollable = False
        self.scroll_y = 0
        if type(parent) is not pygame.Surface:
            parent.add(self)

    @staticmethod
    def blank_background(self, win):
        pass

    def get_y_default(self):
        return self.rect.y + self.scroll_y

    def scroll(self, events):
        down = 0
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    self.scroll_y += 20
                elif event.button == 5:
                    self.scroll_y -= 20
                    down = 1
        too_low = True
        too_high = True
        lowest = 0
        coord_above = 0
        for item in self.contents:
            coord_above = item.get_y() + item.get_h()
            if coord_above > self.get_y() + self.get_h() - self.scroll_y:
                too_high = False
            elif coord_above < lowest:
                lowest = coord_above
        if too_high:
            self.scroll_y = self.get_y() + self.get_h() - coord_above + 20*down

        if self.scroll_y > 0:
            self.scroll_y = 0

    def clear(self):
        self.contents = []

    def default_background(self, win):
        pygame.draw.rect(win, self.background_color, self.get_rect())

    def process(self, click_bool, release_bool, mouse_pos, used_process):
        global top_drawables
        if type(self.parent) is pygame.Surface:
            for item in top_drawables:
                if hasattr(item, 'process') and callable(getattr(item, 'process')):
                    used_process = item.process(click_bool, release_bool, mouse_pos, used_process)

        for item in self.contents[::-1]:
            if item not in top_drawables:
                if hasattr(item, 'process') and callable(getattr(item, 'process')):
                    used_process = item.process(click_bool, release_bool, mouse_pos, used_process)
        if type(self.parent) is pygame.Surface:
            top_drawables = []
        return used_process

    def is_hovered(self, mouse_pos):
        x, y = mouse_pos
        self.set_relative_rect()
        return self.rect.x < x < self.rect.x + self.rect.w and self.rect.y < y < self.rect.y + self.rect.h

    def process_focus(self, events, keys):
        for d in self.contents:
            if hasattr(d, 'process_focus') and callable(getattr(d, 'process_focus')):
                d.process_focus(events, keys)
        if self.is_hovered(pygame.mouse.get_pos()) and self.scrollable:
            self.scroll(events)

    def add(self, item):
        self.contents.append(item)

    # function to find drawables for relative layout
    def find(self, ind):
        return self.contents[ind]

    # function to draw component and all its content
    def draw(self, win):
        if self.layout_type == RELATIVE:
            self.set_relative_rect()
        self.default_background(win)
        self.background(self, win)
        global top_drawables
        for item in self.contents:
            if item.draw_top:
                top_drawables.append(item)
            else:
                item.draw(win)
        if type(self.parent) is pygame.Surface:
            for d in top_drawables:
                d.draw(win)
