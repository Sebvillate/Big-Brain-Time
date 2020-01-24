import pygame
import color as c
import label
import frame
import time


# Loading screen
class LoadingScreen:
    def __init__(self, width, height):
        self.surface = Surface_Drawable((width, height))
        # loading screen design
        self.surface.fill(c.WHITE)
        l = label.Label("Loading: please wait")
        l.set_x((width - l.get_width()) / 2)
        l.set_y((height - l.get_height()) / 2)
        l.draw(self.surface)
        # loading bar attributes
        self.bar_start = 200
        self.bar_end = width - 200
        self.bar_percent = 0
        self.bar_y = height//2 + 100
        self.bar_h = 30

    def draw(self, win):
        win.blit(self.surface, (0, 0))
        # loading bar outline
        pygame.draw.rect(win, c.BLACK, (self.bar_start, self.bar_y, self.bar_end-self.bar_start, self.bar_h), 1)
        # loading bar fill
        pygame.draw.rect(win, c.RED,
                         (self.bar_start, self.bar_y, (self.bar_end-self.bar_start) * self.bar_percent, self.bar_h))

    def load(self, win, current_task, total_tasks):
        self.bar_percent = current_task / total_tasks  # size of red loading bar
        self.draw(win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # true if the program must be quit from loading screen


# surface extension to make it drawable in a draw loop
class SurfaceDrawable(pygame.Surface):
    def draw(self, win):
        win.blit(self, (0, 0))

    def get_px(self, x, y):
        w, h = self.get_size()
        return self.get_at((int(x * w), int(y * h)))


class Drawable(frame.Drawable):
    """drawable class for displaying custom surfaces (such as images)"""
    def __init__(self, dimensions_or_surface=(10, 10)):
        super().__init__()
        if type(dimensions_or_surface) is pygame.Surface:
            self.surface = surface
            self.rect.w, self.rect.h = dimensions_or_surface.get_width(), dimensions_or_surface.get_height()
        else:
            self.surface = pygame.Surface(dimensions_or_surface, pygame.SRCALPHA)
            self.surface = self.surface.convert_alpha()
            self.rect.w, self.rect.h = dimensions_or_surface
        self.visible = True

    def draw(self, win):
        if self.visible:
            if self.layout_type == frame.RELATIVE:
                self.set_relative_rect()
            win.blit(self.surface, (self.get_x(), self.get_y()))

    def get_w(self):
        return self.surface.get_width()

    def get_h(self):
        return self.surface.get_height()

    def set_visibility(self, b):
        self.visible = b


class Label(frame.Drawable):
    """label that can be used with the relative layout"""
    def __init__(self, text=""):
        super().__init__()
        self.text = text
        self.text_color = c.BLACK
        self.text_size = 18
        self.rendered_text = None
        self.render_text()

    def set_size(self, size):
        self.text_size = size
        self.render_text()

    def set_text(self, text):
        self.text = text
        self.render_text()

    def set_color(self, color):
        self.text_color = color
        self.render_text()

    def draw(self, win):
        if self.layout_type == frame.RELATIVE:
            self.set_relative_rect()
        self.rendered_text.set_x(self.get_x())
        self.rendered_text.set_y(self.get_y())
        self.rendered_text.draw(win)

    # renders text drawable
    def render_text(self):
        self.rendered_text = label.Label("".join(self.text), color=self.text_color, size=self.text_size)
        self.rect.w = self.rendered_text.get_width()
        self.rect.h = self.rendered_text.get_height()


class DynamicLabel(Label):
    def __init__(self, function):
        super().__init__()
        self.text_func = function

    def draw(self, win):
        self.set_text(self.text_func(self))
        super().draw(win)


class Input(frame.Drawable):
    """input box"""
    def __init__(self, wh=(200, 70), title=""):
        super().__init__()
        self.rect.w, self.rect.h = wh
        self.text = []
        self.letter_lengths = []
        self.text_size = 18
        self.text_color = c.BLACK
        self.title_color = c.GREY
        self.fill_color = c.WHITE
        self.border_color = c.BLACK
        self.border = 2
        self.rendered_text = None
        self.render_text()
        self.title = title
        self.rendered_title = None
        self.render_title()
        self.surface = pygame.Surface(wh, pygame.SRCALPHA)
        self.surface.convert_alpha()
        self.text_relative_x = 0
        self.flashing_line_ind = -1
        self.flashing_time = time.time()
        self.focus = False
        self.current_character = None
        self.character_start_time = None
        self.first_click = False
        self.first_delay = False
        self.margin = 20
        self.start_highlight = None
        self.end_highlight = None
        self.highlight_color = c.SKY_BLUE
        self.clicked = False
        self.valid_chars = """qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()-_=+[{]}\\|;:'",<.>/?`~ """

    # renders text drawable
    def render_text(self):
        self.rendered_text = label.Label("".join(self.text), color=self.text_color, size=self.text_size)

    # renders title drawable
    def render_title(self):
        self.rendered_title = label.Label(self.title, color=self.title_color, size=self.text_size)

    def get_at_click(self, mouse_pos):
        relative_click = mouse_pos[0] - self.get_x() - self.text_relative_x
        ind = None
        distance = 0
        i = 0  # if loop does not run
        for i, letter in enumerate(self.letter_lengths + [-1]):
            distance += letter
            if letter == -1:
                ind = len(self.letter_lengths) - 1
            elif relative_click < distance - 5:
                ind = i - 1
                break
        if ind is None:
            ind = i - 1
        return ind

    def process(self, click_bool, release_bool, mouse_pos, used_process):
        if click_bool and not self.collide(mouse_pos):
            self.focus = False
        if self.focus:
            if click_bool:
                if self.collide(mouse_pos):
                    self.start_highlight = self.get_at_click(mouse_pos)
                    self.clicked = True
                self.end_highlight = None
            if release_bool:
                self.clicked = False
            if self.clicked:
                self.end_highlight = self.get_at_click(mouse_pos)
                self.flashing_line_ind = self.end_highlight
        elif release_bool:
            if self.collide(mouse_pos) and not used_process:
                self.focus = True
                self.flashing_line_ind = self.get_at_click(mouse_pos)

    def collide(self, mouse_pos):
        x, y = mouse_pos
        return self.rect.x < x < self.rect.x + self.rect.w and self.rect.y < y < self.rect.y + self.rect.h

    def flash(self):
        if time.time() - self.flashing_time > 0.8:
            self.flashing_time = time.time()
        elif time.time() - self.flashing_time > 0.4:
            return True
        return False

    def is_valid_character(self, char):
        return char.lower() in self.valid_chars and char.lower() != ""

    def draw(self, win):
        self.surface = pygame.Surface((self.get_w(), self.get_h()), pygame.SRCALPHA)
        self.surface.convert_alpha()
        if self.layout_type == frame.RELATIVE:
            self.set_relative_rect()
        self.surface.fill(self.fill_color)

        focus_pos = sum(self.letter_lengths[:self.flashing_line_ind+1]) + self.text_relative_x
        if focus_pos > self.get_w() - self.margin:
            self.text_relative_x -= focus_pos - self.get_w() + self.margin
            focus_pos = self.get_w() - self.margin
        else:
            while focus_pos < self.margin * 2:
                self.text_relative_x += 20
                focus_pos += 20
        if self.text_relative_x > self.margin:
            focus_pos -= self.text_relative_x - self.margin
            self.text_relative_x = self.margin

        if len(self.text) == 0:
            self.rendered_title.set_x(self.text_relative_x)
            self.rendered_title.set_y((self.get_h() - self.rendered_text.get_height()) / 2)
            self.rendered_title.draw(self.surface)
        else:
            self.rendered_text.set_x(self.text_relative_x)
            self.rendered_text.set_y((self.get_h() - self.rendered_text.get_height()) / 2)

            if self.end_highlight != self.start_highlight:
                start_x = sum(self.letter_lengths[:self.start_highlight + 1]) + self.text_relative_x
                end_x = sum(self.letter_lengths[:self.end_highlight + 1]) + self.text_relative_x
                pygame.draw.rect(self.surface, self.highlight_color,
                                 (start_x, self.rendered_text.y, end_x - start_x, self.rendered_text.get_height()))

            self.rendered_text.draw(self.surface)

        pygame.draw.rect(self.surface, self.fill_color, (0, 0, self.margin, self.get_h()))
        pygame.draw.rect(self.surface, self.fill_color, (self.get_w() - self.margin, 0, self.margin, self.get_h()))
        if self.focus and self.flash():
            pygame.draw.line(self.surface, self.text_color, (focus_pos, (self.get_h() - self.rendered_text.get_height())/2),
                             (focus_pos, (self.get_h() + self.rendered_text.get_height())/2))
        if self.border > 0:
            pygame.draw.rect(self.surface, self.border_color, (0, 0, self.get_w(), self.get_h()), self.border)
        win.blit(self.surface, (self.get_x(), self.get_y()))

    def run_event(self):
        current_time = time.time()
        if current_time - self.character_start_time > 0.05 and not self.first_click and not self.first_delay:
            self.character_start_time = time.time()
            return True
        elif self.first_click:
            self.first_click = False
            self.first_delay = True
            return True
        elif current_time - self.character_start_time > 0.5 and self.first_delay:
            self.first_delay = False
        return False

    def process_focus(self, events, keys):
        if self.focus:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    self.current_character = event
                    self.character_start_time = time.time()
                    self.first_click = True
                elif event.type == pygame.KEYUP:
                    self.current_character = None
                    self.first_click = False
                    self.first_delay = False

            if self.current_character is not None and self.run_event():
                if self.current_character.key == pygame.K_BACKSPACE:
                    if self.end_highlight is not None and self.end_highlight != self.start_highlight and not self.clicked:
                        s, e = sorted([self.start_highlight+1, self.end_highlight+1])
                        del self.text[s:e]
                        del self.letter_lengths[s:e]
                        self.start_highlight = None
                        self.end_highlight = None
                        self.render_text()
                        self.flashing_line_ind = s - 1
                    elif self.flashing_line_ind >= 0:
                        del self.text[self.flashing_line_ind]
                        del self.letter_lengths[self.flashing_line_ind]
                        self.flashing_line_ind -= 1
                        self.render_text()
                elif self.current_character.key == pygame.K_LEFT:
                    if self.flashing_line_ind > 0:
                        self.flashing_line_ind -= 1
                elif self.current_character.key == pygame.K_RIGHT:
                    if self.flashing_line_ind < len(self.text)-1:
                        self.flashing_line_ind += 1
                elif self.is_valid_character(self.current_character.unicode):
                    if self.end_highlight is not None and self.end_highlight != self.start_highlight and not self.clicked:
                        s, e = sorted([self.start_highlight+1, self.end_highlight+1])
                        del self.text[s:e]
                        del self.letter_lengths[s:e]
                        self.start_highlight = None
                        self.end_highlight = None
                        self.render_text()
                        self.flashing_line_ind = s - 1

                        self.text = self.text[:self.flashing_line_ind + 1] + [self.current_character.unicode] + self.text[self.flashing_line_ind + 1:]
                        last_width = self.rendered_text.get_width()
                        self.render_text()
                        self.letter_lengths.insert(self.flashing_line_ind + 1, self.rendered_text.get_width() - last_width)

                        self.flashing_line_ind += 1

                    else:
                        self.text = self.text[:self.flashing_line_ind+1] + [self.current_character.unicode] + self.text[self.flashing_line_ind+1:]
                        last_width = self.rendered_text.get_width()
                        self.render_text()
                        self.letter_lengths.insert(self.flashing_line_ind+1, self.rendered_text.get_width() - last_width)
                        self.flashing_line_ind += 1

    def get_text(self):
        return "".join(self.text)

    def set_title(self, text):
        self.title = title
        self.render_title()

    def set_numeric(self, boolean):
        if boolean:
            self.valid_chars = "1234567890"
        else:
            self.valid_chars = """qwertyuiopasdfghjklzxcvbnm1234567890!@#$%^&*()-_=+[{]}\\|;:'",<.>/?`~ """
