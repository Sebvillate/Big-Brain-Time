# --------------------------------------------------------------------
# Program: Button Classes
# Author: Alex Hyde
# Date: Oct 25 2019
# Description: Button classes for creating buttons and processing
#   button clicks. Fully customizable with custom on click and release
#   functions.
# Input: Allows easy processing of user clicks.
# --------------------------------------------------------------------


import pygame
import label
import color as c
import vector
import frame

pygame.init()

# alignment constants
LEFT = 0
RIGHT = 1
TOP = 0
BOTTOM = 1
CENTER = 0.5
MATCH = 0
UP = 1
DOWN = 0


# expandable button class
class Button(frame.Drawable):
    """basic button class
    can be expanded into more complex buttons"""
    def __init__(self):
        super().__init__()
        self.round_edges = 0
        self.rect.x, self.rect.y = 0, 0
        self.rect.w = 100
        self.rect.h = 50
        self.border = 2
        self.rounded_strength = 0
        self.text_font = "lucida bright"

        # modifiable draw function
        self.draw = self.draw_as_rect

        # colour attributes
        self.default_fill_color = c.WHITE
        self.border_color = c.BLACK
        self.text_color = c.BLACK
        self.on_hover_color = c.LIGHT_GREY
        self.on_hold_color = c.GREY
        self.current_fill_color = self.default_fill_color

        # button text
        self.text = ""
        self.text_size = 18
        self.tAlignX = CENTER
        self.tAlignY = CENTER
        # rendering text drawable
        self.rendered_text = None
        self.render_text()

        # rendering attributes
        self.visible = True

        # processing attributes
        self.is_clicked = False
        self.active = True
        self.on_click = self.blank_func
        self.on_release = self.blank_func
        self.on_hover = self.blank_func

        # for storing data custom to button
        self.data = dict()

    # default function when button if clicked (change color)
    def on_click_default(self):
        self.current_fill_color = self.on_hold_color
        self.is_clicked = True

    # default function when button if released (change color)
    def on_release_default(self):
        self.current_fill_color = self.default_fill_color
        self.is_clicked = False

    # default function when button if hovered (change color)
    def on_hover_default(self):
        if not self.is_clicked:
            self.current_fill_color = self.on_hover_color

    # return boolean if the mouse position collides with the button
    def is_hovered(self, mouse_pos):
        x, y = mouse_pos
        return self.rect.x < x < self.rect.x + self.rect.w and self.rect.y < y < self.rect.y + self.rect.h

    # renders text drawable
    def render_text(self):
        self.rendered_text = label.Label(self.text, color=self.text_color, size=self.text_size, font=self.text_font)
        self.reset_text_pos()

    # sets text drawable position (based on alignment)
    def reset_text_pos(self):
        self.rendered_text.set_x(self.rect.x + (self.rect.w-self.rendered_text.get_width())*self.tAlignX)
        self.rendered_text.set_y(self.rect.y + (self.rect.h-self.rendered_text.get_height())*self.tAlignY)

    # sets position if using a relative layout
    def set_pos_for_draw(self):
        if self.layout_type == frame.RELATIVE:
            self.set_relative_rect()
            self.reset_text_pos()

    def draw_as_rect(self, win):
        if self.visible:
            self.set_pos_for_draw()
            pygame.draw.rect(win, self.current_fill_color, self.get_rect())

            # draw border
            if self.border != 0:
                x, y, w, h = self.rect.get()
                pygame.draw.rect(win, self.border_color, (x, y, w, self.border))
                pygame.draw.rect(win, self.border_color, (x, y + self.border, self.border, h - self.border))
                pygame.draw.rect(win, self.border_color, (x + self.border, y + h - self.border, w - self.border, self.border))
                pygame.draw.rect(win, self.border_color, (x + w - self.border, y + self.border, self.border, h - self.border))

            self.rendered_text.draw(win)

    def draw_with_rounded_edges(self, win):
        if self.visible:
            self.set_pos_for_draw()
            corner_coordinates = [(self.rect.x + self.rounded_strength, self.rect.y + self.rounded_strength),
                                  (self.rect.x + self.rect.w - self.rounded_strength-1, self.rect.y + self.rounded_strength),
                                  (self.rect.x + self.rect.w - self.rounded_strength-1, self.rect.y + self.rect.h - self.rounded_strength),
                                  (self.rect.x + self.rounded_strength, self.rect.y + self.rect.h - self.rounded_strength)]

            # border of edges
            if self.border != 0:
                for corner in corner_coordinates:
                    pygame.draw.circle(win, self.border_color, corner, self.rounded_strength, self.border)

            # fill of edges
            for corner in corner_coordinates:
                pygame.draw.circle(win, self.current_fill_color, corner, self.rounded_strength-self.border)

            # fill of middle
            pygame.draw.rect(win, self.current_fill_color, (self.rect.x + self.rounded_strength, self.rect.y,
                                                            self.rect.w - 2 * self.rounded_strength, self.rect.h))
            pygame.draw.rect(win, self.current_fill_color, (self.rect.x, self.rect.y + self.rounded_strength,
                                                            self.rect.w, self.rect.h - 2 * self.rounded_strength))

            # border of middle
            if self.border != 0:
                x, y, w, h = self.rect.get()
                pygame.draw.rect(win, self.border_color, (x + self.rounded_strength, y, w - 2 * self.rounded_strength, self.border))
                pygame.draw.rect(win, self.border_color, (x, y + self.rounded_strength, self.border, h - 2 * self.rounded_strength))
                pygame.draw.rect(win, self.border_color, (x + self.rounded_strength, y + h - self.border, w - 2 * self.rounded_strength, self.border))
                pygame.draw.rect(win, self.border_color, (x + w - self.border, y + self.rounded_strength, self.border, h - 2 * self.rounded_strength))

            self.rendered_text.draw(win)

    # function to process button events
    def process(self, click_bool, release_bool, mouse_pos, used_process):
        if (self.is_hovered(mouse_pos) or self.is_clicked) and self.active and used_process is None:
            if click_bool:
                self.on_click_default()
                self.on_click(self)
            elif release_bool and self.is_clicked:
                self.on_release_default()
                self.on_release(self)
            else:
                self.on_hover_default()
                self.on_hover(self)
            return True
        else:
            self.reset_color()
            return used_process

    # reset colour to default color
    def reset_color(self):
        self.current_fill_color = self.default_fill_color

    # empty function (to be replaced by custom functions in instantiated button objects)
    def blank_func(self, blank):
        pass

    # --------------------SETTER AND GETTER METHODS--------------------

    def set_x(self, value):
        self.rect.x = value
        self.reset_text_pos()

    def set_y(self, value):
        self.rect.y = value
        self.reset_text_pos()

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = x, y
        self.reset_text_pos()

    def set_width(self, value):
        self.rect.w = value
        self.reset_text_pos()

    def set_height(self, value):
        self.rect.h = value
        self.reset_text_pos()

    def set_text(self, text):
        self.text = text
        self.render_text()

    def set_font(self, font):
        self.text_font = font
        self.render_text()

    def set_text_size(self, size):
        self.text_size = size
        self.render_text()

    def set_visibility(self, b):
        self.visible = b

    def set_active(self, b):
        self.active = b

    def set_border(self, value):
        self.border = value

    def set_default_fill_color(self, color):
        self.default_fill_color = color

    def set_border_color(self, color):
        self.border_color = color

    def set_hold_color(self, color):
        self.on_hold_color = color

    def set_hover_color(self, color):
        self.on_hover_color = color

    def set_relative(self, parent):
        super().set_relative(parent)
        self.reset_text_pos()

    def set_text_alignment(self, x=None, y=None):
        if x is not None:
            self.tAlignX = x
        if y is not None:
            self.tAlignY = y
        self.reset_text_pos()

    def set_round_edges(self, value):
        if value > 1 or value < 0:
            raise Exception("Edge rounding value cannot be between than 0 and 1")
        rounded_strength = int(min(self.rect.w, self.rect.h) * value / 2)
        if rounded_strength >= self.border:
            self.round_edges = value
            self.rounded_strength = int(min(self.rect.w, self.rect.h) * self.round_edges / 2)
            if value == 0:
                self.draw = self.draw_as_rect
            else:
                self.draw = self.draw_with_rounded_edges


# button with a drop down menu when clicked
class DropDownButton(Button):
    """button that displays a drop down menu of other buttons when clicked"""
    def __init__(self, drop_down_button_names):
        super().__init__()
        self.drop_buttons_width = MATCH
        self.drop_buttons_names = drop_down_button_names
        self.drop_buttons = self.create_buttons(drop_down_button_names)
        self.menu_side = LEFT  # to which side of the main button is the menu displayed
        self.menu_direction = DOWN
        self.spacing = 0
        self.open = False

    # updated process function to include drop down buttons
    def process(self, click_bool, release_bool, mouse_pos, used_process):
        super().process(click_bool, release_bool, mouse_pos, used_process)
        for b in self.drop_buttons:
            used_process = b.process(click_bool, release_bool, mouse_pos, used_process)
        if click_bool and not used_process and not self.is_hovered(mouse_pos):
            self.open = True
            self.on_release_default()
            self.on_release(self)
        return used_process

    # create invisible and inactive drop down buttons
    def create_buttons(self, button_names):
        b_list = []
        y = self.get_y()
        for b in button_names:
            y += self.get_h()
            new_button = Button()
            new_button.set_text(b)
            new_button.set_visibility(False)
            new_button.set_active(False)
            b_list.append(new_button)
        return b_list

    # open and close drawer
    def on_release_default(self):
        super().on_release_default()
        self.open = not self.open
        for b in self.drop_buttons:
            b.set_active(self.open)
            b.set_visibility(self.open)

    def draw_as_rect(self, win):
        super().draw_as_rect(win)
        y = self.get_y()
        if self.drop_buttons_width == MATCH:
            w = self.get_w()
        else:
            w = self.drop_buttons_width
        if self.menu_side == LEFT:
            x = self.get_x()
        else:
            x = self.get_x() + self.get_w() - w
        for b in self.drop_buttons:
            change = self.get_h() - 1 + self.spacing  # -1 to remove 1 pixel gap between buttons
            if self.menu_direction == DOWN:
                y += change
            else:
                y -= change
            if b.visible:
                b.set_x(x)
                b.set_y(y)
                b.set_width(w)
                b.set_height(self.get_h())
                b.draw_as_rect(win)

    def draw_with_rounded_edges(self, win):
        super().draw_with_rounded_edges(win)
        y = self.get_y()
        if self.drop_buttons_width == MATCH:
            w = self.get_w()
        else:
            w = self.drop_buttons_width
        if self.menu_side == LEFT:
            x = self.get_x()
        else:
            x = self.get_x() + self.get_w() - w
        for b in self.drop_buttons:
            change = self.get_h() - 1 + self.spacing  # -1 to remove 1 pixel gap between buttons
            if self.menu_direction == DOWN:
                y += change
            else:
                y -= change
            if b.visible:
                b.set_x(x)
                b.set_y(y)
                b.set_width(w)
                b.set_height(self.get_h())
                b.set_round_edges(self.round_edges)
                b.rounded_strength = self.rounded_strength
                b.draw_with_rounded_edges(win)

    # --------------------SETTER AND GETTER METHODS--------------------

    def set_default_fill_color(self, color):
        self.default_fill_color = color
        for b in self.drop_buttons:
            b.default_fill_color = color

    def set_border_color(self, color):
        self.border_color = color
        for b in self.drop_buttons:
            b.border_color = color

    def set_hold_color(self, color):
        self.on_hold_color = color
        for b in self.drop_buttons:
            b.on_hold_color = color

    def set_hover_color(self, color):
        self.on_hover_color = color
        for b in self.drop_buttons:
            b.on_hover_color = color


# button for selecting from a set of options
class SelectorButton(DropDownButton):
    """expanded drop down menu
    buttons clicked from drop down menu become the text of the main button"""
    def __init__(self, drop_down_button_names, default_ind=None):
        super().__init__(drop_down_button_names)
        for b in self.drop_buttons:
            b.data["main"] = self  # used to reference main button from drop down buttons
            b.on_release = self.selection  # used to set main button's text when clicking (releasing) drop down buttons)
        if default_ind is not None:
            self.set_text(self.drop_buttons[default_ind].text)

    # function to set selection when drop down button is clicked
    @staticmethod
    def selection(b):
        b.data["main"].set_text(b.text)


# button for toggling
class ToggleButton(Button):
    """expanded on basic button: toggles when clicked"""
    def __init__(self):
        super().__init__()
        self.toggled = False
        self.toggled_color = c.LIGHT_BLUE
        self.toggled_hover_color = c.BLUE
        self.toggled_hold_color = c.DARK_BLUE

    def on_release_default(self):
        if self.current_fill_color is self.toggled_color:
            self.current_fill_color = self.default_fill_color
        else:
            self.current_fill_color = self.toggled_color
        self.is_clicked = False
        self.toggled = not self.toggled

    def on_click_default(self):
        if self.toggled:
            self.current_fill_color = self.toggled_hold_color
        else:
            self.current_fill_color = self.on_hold_color
        self.is_clicked = True

    def on_hover_default(self):
        if not self.is_clicked:
            if self.toggled:
                self.current_fill_color = self.toggled_hover_color
            else:
                self.current_fill_color = self.on_hover_color

    def reset_color(self):
        if self.toggled:
            self.current_fill_color = self.toggled_color
        else:
            self.current_fill_color = self.default_fill_color

    # --------------------SETTER AND GETTER METHODS--------------------

    def set_toggle_color(self, color):
        self.toggled_color = color

    def set_toggle_hold_color(self, color):
        self.toggled_hold_color = color

    def set_toggle_hover_color(self, color):
        self.toggled_hover_color = color


pygame.quit()
