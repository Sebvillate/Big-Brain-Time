# --------------------------------------------------------------------
# Program: Dynamic Timer
# Author: Alex Hyde
# Date: Jan 10 2020
# Description: Displayable timer with a dynamic loading bar.
# --------------------------------------------------------------------

import pygame
import pygameplus as pgp
import frame
import time
import color as c
import vector
import label


# dynamic timer that can draw itself
class DynamicTimer(frame.Drawable):
    """circular timer that can loop through intervals"""
    def __init__(self, time_list):
        super().__init__()
        self.time_interval_list = time_list
        self.current_interval = 0
        self.start_time = time.time()
        self.visible = True
        self.rect.w = 300
        self.rect.h = 300
        self.current_angle = 0
        self.last_angle = 0
        self.background_surface = None
        self.generate_background()
        self.rendered_text = None
        self.center_color = c.RED
        self.bar_color = c.BLUE

    # method to generate background of timer
    def generate_background(self):
        surf = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        surf = surf.convert_alpha()
        self.background_surface = surf

    @staticmethod
    def create_text(time_remaining):
        minutes = str(int(time_remaining // 60))
        seconds = str(int(time_remaining % 60))
        if len(seconds) < 2:
            seconds = "0" + seconds
        return minutes + ":" + seconds

    def draw(self, win):
        if self.visible:
            if self.layout_type == frame.RELATIVE:
                self.set_relative_rect()
            x, y = self.get_center()
            center = vector.Vec2(x, y)
            time_passed = time.time() - self.start_time
            fraction_gained = time_passed / self.time_interval_list[self.current_interval]
            angle_gained = int(fraction_gained * 360)

            for i in range(self.last_angle, angle_gained):
                pygame.draw.line(self.background_surface, self.bar_color, (x, y), center.get_point_on_line(i-90, self.rect.w//2-2).get(), 2)
                pygame.draw.line(self.background_surface, self.bar_color, (x, y), center.get_point_on_line(i-89.5, self.rect.w//2-2).get(), 2)

            self.last_angle = angle_gained

            pygame.draw.circle(self.background_surface, c.BLACK, (self.rect.w // 2, self.rect.h // 2), int(self.rect.w // 2 - 1), 3)
            pygame.draw.circle(self.background_surface, self.center_color, (self.rect.w // 2, self.rect.h // 2), int(self.rect.w // 2.7))

            self.render_text(self.create_text(self.time_interval_list[self.current_interval] - time_passed))
            self.rendered_text.draw(self.background_surface)

            win.blit(self.background_surface, (self.rect.x, self.rect.y))

            if fraction_gained >= 1:
                self.current_interval = (self.current_interval + 1) % len(self.time_interval_list)
                self.start_time = time.time()
                self.generate_background()

    # renders text drawable
    def render_text(self, text):
        self.rendered_text = label.Label(text, color=c.BLACK, size=40)
        self.reset_text_pos()

    # sets text drawable position (based on alignment)
    def reset_text_pos(self):
        self.rendered_text.set_x((self.rect.w - self.rendered_text.get_width()) // 2)
        self.rendered_text.set_y((self.rect.h - self.rendered_text.get_height()) // 2)

    def get_center(self):
        return self.get_w()//2, self.get_h()//2
