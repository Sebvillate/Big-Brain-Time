# --------------------------------------------------------------------
# Program: Final Project: Big Brain Time
# Author: Alex Hyde
# Date: Jan 21 2020
# Description: Program that allows you to easily keep track of tasks
#   and assignments, implementing study sessions to use when working
#   on said tasks. Also implements a calendar to keep track of due
#   dates and upcoming tasks/events.
# Inputs: Allows for user interaction through button clicks and
#   input boxes.
# --------------------------------------------------------------------


import pygame
import frame
import label
import color as c
import button2 as b
import dynamic_timer as timer
import pygameplus as pgp
import random
import time
from calendar import monthrange
import datetime
"""matplotlib functionality commented out"""
# import matplotlib.pyplot as plt
# plt.style.use('ggplot')


# --------------------Classes--------------------

# set of colour palettes that can be changed to customize look of program
class Palette:
    """class storing colour palettes to be used for the design of the program"""
    def __init__(self):
        self.light2 = (247, 232, 246)
        self.light1 = (241, 198, 231)
        self.dark1 = (229, 176, 234)
        self.dark2 = (189, 131, 206)

    def purple(self):
        self.light2 = (247, 232, 246)
        self.light1 = (241, 198, 231)
        self.dark1 = (229, 176, 234)
        self.dark2 = (189, 131, 206)
        self.set_all_colors()

    def spooky_forest(self):
        self.light2 = (199, 240, 219)
        self.light1 = (139, 186, 187)
        self.dark1 = (108, 123, 149)
        self.dark2 = (70, 65, 89)
        self.set_all_colors()

    def ocean_foam(self):
        self.light2 = (255, 251, 250)
        self.light1 = (139, 215, 210)
        self.dark1 = (0, 189, 157)
        self.dark2 = (73, 198, 229)
        self.set_all_colors()

    def fall(self):
        self.light2 = (245, 240, 227)
        self.light1 = (64, 191, 193)
        self.dark1 = (255, 111, 94)
        self.dark2 = (240, 19, 77)
        self.set_all_colors()

    def grey_scale(self):
        self.light2 = (225, 225, 225)
        self.light1 = (175, 175, 175)
        self.dark1 = (125, 125, 125)
        self.dark2 = (75, 75, 75)
        self.set_all_colors()

    def candy(self):
        self.light2 = (230, 248, 249)
        self.light1 = (177, 232, 237)
        self.dark1 = (237, 181, 245)
        self.dark2 = (232, 110, 208)
        self.set_all_colors()

    def pastel(self):
        self.light2 = (255, 243, 175)
        self.light1 = (195, 245, 132)
        self.dark1 = (255, 210, 113)
        self.dark2 = (246, 92, 120)
        self.set_all_colors()

    # set colour of default drawables when switching colours in settings
    def set_all_colors(self):
        main_component.background_color = self.light1
        tool_bar.background_color = self.dark2
        back_button.set_default_fill_color(self.dark2)
        back_button.set_hover_color(self.dark1)
        back_button.set_hold_color(self.light1)
        back_button.set_border_color(self.dark2)
        side_bar.background_color = self.dark1
        page_component.background_color = self.light1
        sort_button.set_default_fill_color(COLOR.dark2)
        sort_button.set_hover_color(COLOR.dark1)
        sort_button.set_hold_color(COLOR.light1)
        sort_button.set_border_color(COLOR.dark2)
        settings_button.set_default_fill_color(COLOR.dark2)
        settings_button.set_hover_color(COLOR.dark1)
        settings_button.set_hold_color(COLOR.light1)
        settings_button.set_border_color(COLOR.dark2)
        add_button.set_default_fill_color(COLOR.dark2)
        add_button.set_hover_color(COLOR.dark1)
        add_button.set_hold_color(COLOR.light1)
        add_button.set_border_color(c.BLACK)


# class for storing all task data
class Task:
    """stores all task data. can generate task codes"""
    def __init__(self, code, title, description, duedate, priority, parentfolder):
        self.title = title
        self.taskcode = code
        self.description = description
        self.date = duedate
        self.priority = priority
        self.parent = parentfolder
        self.data = [code, title, description, duedate, priority]

    # generating task code for saving the task
    @staticmethod
    def generate_task_code():
        char_code = None
        chars = "1234567890!@#$%^&*()qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDGFHJKLZXCVBNM<>,.;:/?-_+="
        char_list = list(chars)
        # ensures task code is not a duplicate
        while char_code in all_task_codes or char_code is None:
            char_code = ""
            for i in range(10):
                char_code += random.choice(char_list)
        return char_code


# class for storing all folder data
class Folder:
    """stores all folder data, including contents"""
    def __init__(self, title, parent=None):
        self.title = title
        self.contents = []
        self.parent = parent

    def add(self, item):
        self.contents.append(item)

    # add a task to the folder when reading in from file
    def taskadd(self, code, parentfolder):
        global fol
        for i, line in enumerate(fol):
            if line == code:
                all_task_codes.append(code)
                task = Task(fol[i], fol[i + 1], fol[i + 2], fol[i + 3], int(fol[i + 4]), parentfolder)
                self.contents.append(task)
                if task.date in all_task_date_dict:
                    all_task_date_dict[task.date].append(task)
                else:
                    all_task_date_dict[task.date] = [task]
                return


# class for storing all user data for analytics
class UserData:
    """stores all user data for analytics
    can display the data using matplotlib module"""
    def __init__(self):
        self.studysessions = []
        self.taskscompleted = []
        self.tasks_being_completed = 0

    # add time spent doing a task
    def Add_Time(self, time):
        newtime = round(int(time) / 60, 1)
        today = datetime.datetime.now()
        date = str(today.day) + "/" + str(today.month)
        for item in self.studysessions:
            if item[0] == date:
                item[1] += newtime
                return
        if len(self.studysessions) > 7:  # delete data older than 7 days
            del (self.studysessions[0])
        self.studysessions.append([date, time])

    # add number of tasks completed
    def Add_Tasks(self, taskcount):
        today = datetime.datetime.now()
        date = str(today.day) + "/" + str(today.month)
        for item in self.taskscompleted:
            if item[0] == date:
                item[1] += taskcount#Adds task to current day count if current day already exists
                return
        if len(self.taskscompleted) > 7:  # delete data older than 7 days
            del (self.taskcompleted[0])
        self.taskscompleted.append([date, int(taskcount)])

    # display bar graph with time spend studying
    def DisplayStudyHours(self):
        x = [pair[0] for pair in self.studysessions]
        x_pos = [i for i in range(len(self.studysessions))]
        y_pos = [pair[1] for pair in self.studysessions]
        plt.bar(x_pos, y_pos, color='pink')
        plt.xlabel("Date")
        plt.ylabel("Study Hours")
        plt.title("Study hours per day")
        plt.xticks(x_pos, x)
        plt.show()

    # display bar graph with tasks completed
    def DisplayTasksCompleted(self):
        x = [pair[0] for pair in self.taskscompleted]
        x_pos = [i for i in range(len(self.taskscompleted))]
        y_pos = [pair[1] for pair in self.taskscompleted]
        plt.bar(x_pos, y_pos, color='pink')
        plt.xlabel("Date")
        plt.ylabel("Tasks Completed")
        plt.title("Day")
        plt.xticks(x_pos, x)
        plt.show()

    # save data to text file
    def SaveData(self):
        fi = open("UserData.txt", 'w')
        for item in self.studysessions:
            fi.write(item[0] + "," + str(item[1]) + "\n")
        fi.write("Tasks Completed\n")
        for item in self.taskscompleted:
            fi.write(item[0] + "," + str(item[1]) + "\n")
        fi.close()

    # read data in from text file
    def ReadInData(self):
        fi = open("UserData.txt", 'r')
        alllines = fi.read().splitlines()
        for i in range(len(alllines)):
            if alllines[i] != "Tasks Completed":
                line = alllines[i].split(",")
                self.studysessions.append([line[0], float(line[1])])
            else:
                alllines = alllines[i + 1:]
                for j in range(len(alllines)):
                    line = alllines[j].split(",")
                    self.taskscompleted.append([line[0], float(line[1])])
                break


# --------------------Functions--------------------

# open add task/folder window on click
def add_task_or_folder(but):
    page_component.clear()
    add_button.set_visibility(False)
    add_button.set_active(False)
    start_task_button.set_visibility(False)
    start_task_button.set_active(False)
    back_button.set_visibility(True)
    back_button.set_active(True)
    back_icon.set_visibility(True)
    finish_button.set_visibility(True)
    finish_button.set_active(True)
    sort_button.set_visibility(False)
    sort_button.set_active(False)
    page_component.scrollable = False
    page_component.scroll_y = 0

    folder_button = b.Button()
    folder_button.set_relative(page_component)
    folder_button.set_text("Folder")
    folder_button.layout.gravity = "left top"

    task_button = b.Button()
    task_button.set_relative(page_component)
    task_button.set_text("Task")
    task_button.layout.gravity = "left"
    task_button.layout.align_top = 0

    for button in [folder_button, task_button]:
        button.rect.w = 300
        button.rect.h = 70
        button.set_default_fill_color(COLOR.light2)
        button.set_hover_color(COLOR.light1)
        button.set_hold_color(COLOR.dark1)
        button.set_border_color(COLOR.dark2)
        button.layout.margin_left = 20
        button.layout.margin_top = 5

    input_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    input_component.layout.w = frame.MATCH
    input_component.rect.h = 600
    input_component.layout.gravity = "left"
    input_component.layout.align_top = 1

    blank_button = b.Button()
    blank_button.set_relative(page_component)
    blank_button.layout.gravity = "top left"
    blank_button.set_visibility(False)
    blank_button.set_active(False)

    # display folder input box
    def folder_input(but):
        input_component.clear()
        title = pgp.Input((300, 70), "Title:")
        title.set_relative(input_component)
        title.layout.gravity = "top left"
        title.layout.margin_left = 20
        title.layout.margin_top = 20
        title.fill_color = COLOR.light2
        title.border_color = COLOR.dark2
        title.border = 1

    # display task input boxes
    def task_input(but):
        input_component.clear()
        title = pgp.Input((300, 70), "Title:")
        title.set_relative(input_component)
        title.layout.gravity = "top left"
        title.layout.margin_left = 20
        title.layout.margin_top = 20
        title.fill_color = COLOR.light2
        title.border_color = COLOR.dark2
        title.border = 1

        description = pgp.Input((300, 70), "Description:")
        due_date = pgp.Input((300, 70), "Due Date (dd/mm/yyyy) :")
        due_date.valid_chars = "1234567890/"
        priority = pgp.Input((300, 70), "Priority (0 - 10) :")
        priority.set_numeric(True)

        # button attributes
        for i, button in enumerate([description, due_date, priority]):
            button.set_relative(input_component)
            button.layout.margin_left = 20
            button.layout.margin_top = 5
            button.layout.gravity = "left"
            button.layout.align_top = i
            button.border = 1
            button.fill_color = COLOR.light2
            button.border_color = COLOR.dark2

    folder_button.on_release = folder_input
    task_button.on_release = task_input

    # but parameter to allow function to be used for back button click
    # resets page window when finished creating task
    def reset_page_window(but=None):
        load_folder_page(current_folder)
        add_button.set_visibility(True)
        add_button.set_active(True)
        if selected_tasks:
            start_task_button.set_visibility(True)
            start_task_button.set_active(True)
        finish_button.set_visibility(False)
        finish_button.set_active(False)
        sort_button.set_visibility(True)
        sort_button.set_active(True)
        back_button.on_release = on_back_pressed

    # create task or folder based on inputs, if inputs are valid, and return to main page
    def finish_task_or_folder(but):
        inputs = []
        for item in input_component.contents:  # testing valid inputs
            if type(item) is pgp.Input:
                if item.get_text() == "":
                    return
                elif item.title == "Priority (0 - 10) :" and int(item.get_text()) > 10:
                    return
                elif item.title == "Due Date (dd/mm/yyyy) :" and item.get_text().count("/") != 2:
                    return
                inputs.append(item.get_text())
        if not inputs:  # if folder or task haven't been clicked (no inputs yet)
            return
        elif len(inputs) > 1:  # if more than 1 input box: task
            due_date = inputs[2].split("/")
            for i in range(len(due_date)):
                if due_date[i] == "":
                    due_date[i] = "0"
            due_date = "/".join(due_date)
            new_task = Task(Task.generate_task_code(), inputs[0], inputs[1], due_date, int(inputs[3]), current_folder)
            current_folder.add(new_task)
            # add task to date:task dictionary
            if new_task.date in all_task_date_dict:
                all_task_date_dict[new_task.date].append(new_task)
            else:
                all_task_date_dict[new_task.date] = [new_task]
        else:
            new_folder = Folder(inputs[0], current_folder)
            current_folder.add(new_folder)
        page_component.scrollable = True
        save_work()

        reset_page_window()

    finish_button.on_release = finish_task_or_folder
    back_button.on_release = reset_page_window


# when back button pressed, open previous folder
def on_back_pressed(but):
    load_folder_page(current_folder.parent)


# loads folder off of button click (when clicking on a folder
def load_folder_page_on_click(but):
    load_folder_page(but.data["parent_folder"])


# create page from list of folders and tasks
def load_folder_page(folder):
    # set visible back button if possible to go back
    if folder.parent is None:
        back_button.set_active(False)
        back_button.set_visibility(False)
        back_icon.set_visibility(False)
    else:
        back_button.set_active(True)
        back_button.set_visibility(True)
        back_icon.set_visibility(True)

    add_button.set_visibility(True)
    add_button.set_active(True)
    back_button.on_release = on_back_pressed
    sort_button.set_visibility(True)
    sort_button.set_active(True)

    if sort_button.text == "Date":
        folder.contents = sortbydate(folder.contents)
    else:
        folder.contents = sortbypriority(folder.contents)

    global selected_tasks
    selected_tasks = []
    start_task_button.set_visibility(False)
    start_task_button.set_active(False)

    tool_bar_title.set_text(folder.title)

    page_component.clear()  # remove any previous content
    page_component.scroll_y = 0
    page_component.scrollable = True
    global current_folder
    current_folder = folder  # set new current folder
    ind = -1
    for item in folder.contents:
        if type(item) is Folder:
            box = template_folder_box(page_component, item)
        else:
            box = template_task_box(page_component, item)
        box.layout.margin_bottom = 5
        if ind >= 0:
            box.layout.align_top = ind
        ind += 1


# returns a component for displaying a task containing all of the information from the task
def template_folder_box(parent, folder):
    component = frame.Component(parent, frame.RELATIVE, COLOR.light2)
    component.layout.w = frame.MATCH
    component.rect.h = 70

    full_button = b.Button()
    full_button.set_relative(component)
    full_button.layout.w = frame.MATCH
    full_button.layout.h = frame.MATCH
    full_button.set_default_fill_color(COLOR.light2)
    full_button.set_hover_color(COLOR.dark1)
    full_button.set_hold_color(COLOR.dark2)
    full_button.set_border(0)
    full_button.on_release = load_folder_page_on_click
    full_button.data["parent_folder"] = folder

    folder_icon = pgp.Drawable((60, 60))
    folder_icon.set_relative(component)
    folder_icon.layout.gravity = "left top"
    folder_icon.surface.blit(pygame.image.load("foldericon.png"), (10, 18))

    title = pgp.Label(folder.title)
    title.set_relative(component)
    title.set_size(35)
    title.layout.gravity = "centery"
    title.layout.margin_left = 65

    arrow = pgp.Label(">")
    arrow.set_relative(component)
    arrow.set_size(55)
    arrow.layout.gravity = "right top"
    arrow.layout.margin_right = 30

    return component


# returns a component for displaying a task containing all of the information from the task
def template_task_box(parent, task):
    component = frame.Component(parent, frame.RELATIVE, COLOR.light2)
    component.layout.w = frame.MATCH
    component.rect.h = 100

    toggle_button = b.ToggleButton()
    toggle_button.set_relative(component)
    toggle_button.layout.gravity = "left centery"
    toggle_button.layout.margin_left = 15
    toggle_button.layout.margin_right = 20
    toggle_button.set_width(25)
    toggle_button.set_height(25)
    toggle_button.set_round_edges(0.9)
    toggle_button.on_release = select_task
    toggle_button.data["task"] = task

    title = pgp.Label(task.title)
    title.set_size(25)
    title.set_relative(component)
    title.layout.margin_top = 5
    title.layout.align_left = 0

    description = pgp.Label(task.description)
    description.set_relative(component)
    description.set_color(c.GREY)
    description.layout.align_left = 0
    description.layout.align_top = 1

    date = pgp.Label(task.date)
    date.set_relative(component)
    date.layout.align_left = 0
    date.layout.margin_bottom = 5
    date.layout.gravity = "bottom"

    priority_icon = pgp.Drawable((80, 80))
    priority_icon.set_relative(component)
    p_icon = label.Label(str(task.priority))
    p_icon.set_size(int(15+task.priority*2.3))
    p_icon.center((40, 40))
    p_icon.draw(priority_icon.surface)
    if task.priority > 8:
        color = c.RED
    elif task.priority > 4:
        color = c.YELLOW
    else:
        color = c.GREEN
    pygame.draw.circle(priority_icon.surface, color, (40, 40), 38, 4)
    priority_icon.layout.gravity = "right centery"
    priority_icon.layout.margin_right = 20

    return component


# clears all buttons from page component for displaying a new window
# set back button to return to previously visible page
def empty_page_component():
    page_component.clear()
    page_component.scroll_y = 0
    page_component.scrollable = False

    hide_buttons = [start_task_button, sort_button, add_button]
    for but in hide_buttons:
        but.set_visibility(False)
        but.set_active(False)
    back_button.set_visibility(True)
    back_button.set_active(True)
    back_icon.set_visibility(True)

    def end_session(but):
        for hbut in hide_buttons:
            hbut.set_visibility(True)
            hbut.set_active(True)
        page_component.scrollable = True
        back_button.on_release = on_back_pressed
        load_folder_page(current_folder)
        save_work()

    back_button.on_release = end_session


# opens calendar page
def open_calendar(but=None):
    if but is not None:
        global month, year
        dt = datetime.datetime.today()
        year = dt.year
        month = dt.month
    start_day, total_days = monthrange(year, month)
    start_day = (start_day + 1) % 7
    settings_button.open = True
    settings_button.on_release_default()

    empty_page_component()

    # toolbar component of page

    tool_bar_title.set_text("Calendar")

    top_bar_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    top_bar_component.layout.w = frame.MATCH
    top_bar_component.rect.h = 70
    left_button = b.Button()
    left_button.set_relative(top_bar_component)
    left_button.layout.gravity = "left top"
    left_button.layout.h = frame.MATCH
    left_button.rect.w = 70
    left_button.set_default_fill_color(COLOR.light1)
    left_button.set_hover_color(COLOR.dark1)
    left_button.set_hold_color(COLOR.dark2)
    left_button.set_text("<")
    left_button.set_text_size(70)
    left_button.set_border(0)

    def change_month_left(but):
        global month
        month -= 1
        if month < 1:
            global year
            year -= 1
            month = 12
        open_calendar()
    left_button.on_release = change_month_left

    title = pgp.Label(MONTH_NAMES[month-1] + " " + str(year))
    title.set_relative(top_bar_component)
    title.set_size(35)
    title.layout.gravity = "centery"
    title.layout.margin_left = 80

    right_button = b.Button()
    right_button.set_relative(top_bar_component)
    right_button.layout.gravity = "right top"
    right_button.layout.h = frame.MATCH
    right_button.rect.w = 70
    right_button.set_default_fill_color(COLOR.light1)
    right_button.set_hover_color(COLOR.dark1)
    right_button.set_hold_color(COLOR.dark2)
    right_button.set_text(">")
    right_button.set_text_size(70)
    right_button.set_border(0)

    def change_month_right(but):
        global month
        month += 1
        if month > 12:
            global year
            year += 1
            month = 1
        open_calendar()

    right_button.on_release = change_month_right

    # calendar component of page

    calendar_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    calendar_component.layout.w = frame.MATCH
    calendar_component.layout.align_top = 0

    for row in range(6):  # rows of calendar
        row_component = frame.Component(calendar_component, frame.RELATIVE, COLOR.light1)
        if row == 0:
            row_component.layout.gravity = "top centerx"
        else:
            row_component.layout.align_top = row - 1
            row_component.layout.gravity = "centerx"
        row_component.rect.h = 70
        row_component.layout.w = frame.MATCH
        for col in range(7):  # columns of calendar
            day = col + 7 * row - start_day + 1
            if month < 10:
                month_str = "0" + str(month)
            else:
                month_str = str(month)
            if day < 10:
                day_str = "0" + str(day)
            else:
                day_str = str(day)
            date_str = day_str + "/" + month_str + "/" + str(year)
            if date_str in all_task_date_dict:
                tasks = [task.title for task in all_task_date_dict[date_str]]
            else:
                tasks = []
            day_button = b.DropDownButton(tasks)

            if tasks:
                for i in range(len(day_button.drop_buttons)):
                    task = all_task_date_dict[date_str][i]
                    day_button.drop_buttons[i].data["task"] = task
                    day_button.drop_buttons[i].on_release = lambda but: load_folder_page(but.data["task"].parent)

            def change_draw_priority(self):
                self.draw_top = self.open
            day_button.on_release = change_draw_priority
            day_button.set_relative(row_component)
            if col == 0:
                day_button.layout.gravity = "left centery"
            else:
                day_button.layout.align_left = col - 1
                day_button.layout.gravity = "centery"
            day_button.layout.w = frame.MATCH
            day_button.layout.h = frame.MATCH
            day_button.drop_buttons_width = 250
            if col > 3:
                day_button.menu_side = b.RIGHT
            day_button.w_fraction = 7.2
            day_button.set_border(3)
            day_button.layout.set_margin(1)
            if day < DAY and month == MONTH and year == YEAR or month < MONTH and year == YEAR or year < YEAR:
                day_button.set_border_color(c.LIGHT_RED)
            elif day == DAY and month == MONTH and year == YEAR:
                day_button.set_border_color(c.GREEN)
            else:
                day_button.set_border_color(COLOR.dark2)
            day_button.set_hold_color(COLOR.dark2)
            day_button.set_hover_color(COLOR.dark1)
            if tasks:
                day_button.set_default_fill_color(COLOR.light2)
            else:
                day_button.set_default_fill_color(COLOR.light1)
            if day < 1 or day > total_days:
                day_button.set_default_fill_color(COLOR.light1)
                day_button.set_border(0)
                day_button.set_active(False)
            else:
                day_button.set_text(str(day))


# opens settings page
def open_settings(but):
    empty_page_component()
    settings_button.on_release_default()

    tool_bar_title.set_text("Settings")

    # colours settings

    title = pgp.Label("Color Schemes")
    title.layout.w = frame.MATCH
    title.set_relative(page_component)
    title.set_size(35)
    title.layout.gravity = "top left"
    title.layout.margin_top = 10
    title.layout.margin_left = 20

    button_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    button_component.layout.w = frame.MATCH
    button_component.layout.gravity = "top left"
    button_component.layout.align_top = 0

    purple_button = b.Button()
    purple_button.set_relative(button_component)
    purple_button.set_default_fill_color((241, 198, 231))
    purple_button.set_hover_color((229, 176, 234))
    purple_button.set_hold_color((189, 131, 206))
    purple_button.set_border_color((247, 232, 246))
    purple_button.on_release = lambda but: COLOR.purple()
    purple_button.layout.gravity = "top left"

    green_button = b.Button()
    green_button.set_relative(button_component)
    green_button.set_default_fill_color((139, 186, 187))
    green_button.set_hover_color((108, 123, 149))
    green_button.set_hold_color((70, 65, 89))
    green_button.set_border_color((199, 240, 219))
    green_button.on_release = lambda but: COLOR.spooky_forest()

    blue_button = b.Button()
    blue_button.set_relative(button_component)
    blue_button.set_default_fill_color((139, 215, 210))
    blue_button.set_hover_color((0, 189, 157))
    blue_button.set_hold_color((73, 198, 229))
    blue_button.set_border_color((255, 251, 250))
    blue_button.on_release = lambda but: COLOR.ocean_foam()

    red_button = b.Button()
    red_button.set_relative(button_component)
    red_button.set_default_fill_color((255, 111, 94))
    red_button.set_hover_color((64, 191, 193))
    red_button.set_hold_color((240, 19, 77))
    red_button.set_border_color((245, 240, 227))
    red_button.on_release = lambda but: COLOR.fall()

    grey_button = b.Button()
    grey_button.set_relative(button_component)
    grey_button.set_default_fill_color((175, 175, 175))
    grey_button.set_hover_color((125, 125, 125))
    grey_button.set_hold_color((75, 75, 75))
    grey_button.set_border_color((225, 225, 225))
    grey_button.on_release = lambda but: COLOR.grey_scale()

    candy_button = b.Button()
    candy_button.set_relative(button_component)
    candy_button.set_default_fill_color((177, 232, 237))
    candy_button.set_hover_color((237, 181, 245))
    candy_button.set_hold_color((232, 110, 208))
    candy_button.set_border_color((230, 248, 249))
    candy_button.on_release = lambda but: COLOR.candy()

    pastel_button = b.Button()
    pastel_button.set_relative(button_component)
    pastel_button.set_default_fill_color((195, 245, 132))
    pastel_button.set_hover_color((255, 210, 113))
    pastel_button.set_hold_color((246, 92, 120))
    pastel_button.set_border_color((255, 243, 175))
    pastel_button.on_release = lambda but: COLOR.pastel()

    for i, but in enumerate([purple_button, green_button, blue_button, red_button, grey_button, candy_button, pastel_button]):
        if i != 0:
            but.layout.align_left = i-1
        but.layout.w = frame.MATCH
        but.w_fraction = 7
        but.layout.gravity = "top"

    # analytics settings

    title = pgp.Label("Analytics")
    title.layout.w = frame.MATCH
    title.set_relative(page_component)
    title.set_size(35)
    title.layout.align_top = 1
    title.layout.gravity = "top left"
    title.layout.margin_top = 30
    title.layout.margin_left = 20

    button_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    button_component.layout.w = frame.MATCH
    button_component.layout.gravity = "top left"
    button_component.layout.align_top = 2

    task_completed_data = b.Button()
    task_completed_data.set_text("Unavailable")
    task_completed_data.set_relative(button_component)
    task_completed_data.layout.w = frame.MATCH
    task_completed_data.w_fraction = 2
    # task_completed_data.on_release = lambda but: User.DisplayTasksCompleted()
    task_completed_data.layout.gravity = "top left"

    hours_spend_data = b.Button()
    hours_spend_data.set_text("Unavailable")
    hours_spend_data.set_relative(button_component)
    hours_spend_data.layout.w = frame.MATCH
    hours_spend_data.w_fraction = 2
    hours_spend_data.layout.gravity = "top"
    hours_spend_data.layout.align_left = 0
    # hours_spend_data.on_release = lambda but: User.DisplayStudyHours()


# starts studying session from selected tasks
def start_session(b):
    page_component.clear()
    page_component.scroll_y = 0
    page_component.scrollable = False

    hide_buttons = [start_task_button, sort_button, add_button]
    for but in hide_buttons:
        but.set_visibility(False)
        but.set_active(False)
    back_button.set_visibility(True)
    back_button.set_active(True)
    back_icon.set_visibility(True)

    start_time = time.time()

    def end_session(but):
        for hbut in hide_buttons:
            hbut.set_visibility(True)
            hbut.set_active(True)
        page_component.scrollable = True
        back_button.on_release = on_back_pressed
        load_folder_page(current_folder)
        User.Add_Tasks(User.tasks_being_completed)
        User.tasks_being_completed = 0
        User.Add_Time((time.time() - start_time)//60)
        save_work()

    back_button.on_release = end_session
    tool_bar_title.set_text("Study Session")

    timer_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    timer_component.layout.w = frame.MATCH
    timer_component.rect.h = 350
    timer_component.draw_top = True
    active_timer = timer.DynamicTimer([25*60, 5*60])
    active_timer.set_relative(timer_component)
    active_timer.layout.gravity = "centerx centery"
    active_timer.bar_color = COLOR.dark1
    active_timer.center_color = COLOR.dark2

    def display_time(seconds):
        seconds = int(seconds)
        hrs = str(seconds // 3600)
        seconds %= 3600
        mins = str(seconds // 60)
        seconds = str(seconds % 60)
        if len(mins) == 1:
            mins = "0" + mins
        if len(seconds) == 1:
            seconds = "0" + seconds
        return hrs + ":" + mins + ":" + seconds

    total_time = pgp.DynamicLabel(lambda a: display_time(time.time() - start_time + 1))
    total_time.set_relative(timer_component)
    total_time.text_size = 30
    total_time.layout.gravity = "bottom right"

    tasks_component = create_task_component_for_session()


# creates scrollable tasks section below timer when studying
def create_task_component_for_session():
    tasks_component = frame.Component(page_component, frame.RELATIVE, COLOR.light1)
    tasks_component.layout.w = frame.MATCH
    tasks_component.layout.h = frame.MATCH
    tasks_component.layout.align_top = 0
    tasks_component.layout.gravity = "centery"
    tasks_component.scrollable = True
    for i, task in enumerate(selected_tasks):
        task_component = frame.Component(tasks_component, frame.RELATIVE, COLOR.light2)
        task_component.layout.w = frame.MATCH
        task_component.rect.h = 200
        if i > 0:
            task_component.layout.align_top = i-1
            task_component.layout.margin_top = 5

        toggle_button = b.ToggleButton()
        toggle_button.set_relative(task_component)
        toggle_button.set_width(50)
        toggle_button.set_height(50)
        toggle_button.layout.gravity = "centery"
        toggle_button.layout.margin_left = 30
        toggle_button.data["task"] = task.data["task"]
        toggle_button.on_release = complete_task

        title = pgp.Label(task.data["task"].title)
        title.set_relative(task_component)
        title.set_size(50)
        title.layout.gravity = "centery"
        title.layout.align_left = 0
        title.layout.margin_left = 30
    return tasks_component


# when task in studying is toggled, it is deleted
def complete_task(but):
    global current_folder
    if but.toggled:
        current_folder.contents.remove(but.data["task"])
        all_task_date_dict[but.data["task"].date].remove(but.data["task"])
        User.tasks_being_completed += 1
    else:
        current_folder.contents.append(but.data["task"])
        if but.data["task"].date in all_task_date_dict:
            all_task_date_dict[but.data["task"].date].append(but.data["task"])
        else:
            all_task_date_dict[but.data["task"].date] = [but.data["task"]]
        User.tasks_being_completed -= 1


# when task on main screen is toggled, it is appended or removed from selected tasks
# start studying becomes visible if at least one button is selected
def select_task(but):
    global selected_tasks
    if but.toggled:
        selected_tasks.append(but)
    else:
        selected_tasks.remove(but)
    start_task_button.set_visibility(bool(selected_tasks))
    start_task_button.set_active(bool(selected_tasks))


# deletes current folder is it is empty
def delete_current_folder(but):
    settings_button.on_release_default()
    if current_folder.parent is not None and not current_folder.contents:
        current_folder.parent.contents.remove(current_folder)
        load_folder_page(current_folder.parent)
        save_work()


# recursive algorithm creating folders from text file
# creates directory as a tree data structure
def createfolder(parentfolder):
    global fi
    next_line = fi.readline().strip()
    while next_line != "}" and next_line != '':
        if next_line[-1] == "{":
            new_folder = Folder(next_line[:-1], parentfolder)
            createfolder(new_folder)
            parentfolder.add(new_folder)
        else:
            parentfolder.taskadd(next_line, parentfolder)
        next_line = fi.readline().strip()
    return


# saves all tasks, folders, and their paths in the respective text files
def save_contents(item, taskfold, foldfold):
    if type(item) == Folder:
        if item != main_folder:
            foldfold.write(item.title + "{\n")
        for thing in item.contents:
            save_contents(thing, taskfold, foldfold)
        if item != main_folder:
            foldfold.write("}\n")
    elif type(item) == Task:
        foldfold.write(item.taskcode + '\n')
        for attribute in item.data:
            taskfold.write(str(attribute) + "\n")


# sets sorting to by date
def sort_by_date_on_click(b):
    b.data["main"].set_text(b.text)
    load_folder_page(current_folder)


# sorts list of tasks and folders by date, placing folders at the beginning
def sortbydate(tasklist):
    folderlist = []
    for item in tasklist:  # Removes all folders with no due date
        if type(item) is Folder:
            folderlist.append(item)
        else:
            item.date = item.date.split("/")
    for f in folderlist:
        tasklist.remove(f)
    tasklist = sorted(tasklist, key=lambda task: int(task.date[0]))
    tasklist = sorted(tasklist, key=lambda task: int(task.date[1]))
    tasklist = sorted(tasklist, key=lambda task: int(task.date[2]))
    for item in tasklist:
        item.date = "/".join(item.date)
    return folderlist + tasklist


# sets sorting to by priority
def sort_by_priority_on_click(b):
    b.data["main"].set_text(b.text)
    load_folder_page(current_folder)


# sorts list of tasks and folders by priority, placing folders at the beginning
def sortbypriority(tasklist):
    folderlist = []
    for item in tasklist:  # Removes all folders with no priority
        if type(item) is Folder:
            folderlist.append(item)
    for f in folderlist:
        tasklist.remove(f)
    tasklist = sorted(tasklist, key=lambda task: int(task.priority), reverse=True)
    return folderlist + tasklist


# saves all tasks, folders, and their directories, as well as all user data
def save_work():
    fi = open('folder folder.txt', 'w')
    fo = open('Saved Tasks.txt', 'w')
    save_contents(main_folder, fo, fi)
    User.SaveData()
    fi.close()
    fo.close()


# redraws everything in the main_component (main component contains all other drawables on screen)
def redraw():
    win.fill(c.WHITE)
    main_component.draw(win)
    pygame.display.update()


# --------------------Constants--------------------

dt = datetime.datetime.today()  # temporary variable
YEAR = dt.year
MONTH = dt.month
DAY = dt.day
MIN_WIDTH = 600
MIN_HEIGHT = 400
COLOR = Palette()
MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


# --------------------Initialisation--------------------

pygame.init()

win = pygame.display.set_mode((700, 600), pygame.RESIZABLE)
pygame.display.set_icon(pygame.image.load("brainicon.png"))
pygame.display.set_caption("Big Brain Time")

main_component = frame.Component(win, background_color=COLOR.light1)

# initialises variables
year = dt.year
month = dt.month
all_task_codes = []
selected_tasks = []
all_task_date_dict = dict()

# reads in user data
User = UserData()
User.ReadInData()

# reads in folders and tasks
fi = open('folder folder.txt', 'r')
fo = open('Saved Tasks.txt', 'r')
fol = fo.read().splitlines()
main_folder = Folder("Big Brain Time")
createfolder(main_folder)
current_folder = main_folder

# ----------------------------
# initialising all initial drawables, buttons, and components (such as tool bar, side bar, and main page component)
# ----------------------------

tool_bar = frame.Component(main_component, frame.RELATIVE, COLOR.dark2)
tool_bar.layout.w = frame.MATCH
tool_bar.rect.h = 70
tool_bar.draw_top = True

back_button = b.Button()
back_button.set_relative(tool_bar)
back_button.layout.h = frame.MATCH
back_button.rect.w = 70
back_button.set_default_fill_color(COLOR.dark2)
back_button.set_hover_color(COLOR.dark1)
back_button.set_hold_color(COLOR.light1)
back_button.set_border_color(COLOR.dark2)
back_button.border = 0
back_button.on_release = on_back_pressed

back_icon = pgp.Drawable((70, 70))
back_icon.set_relative(tool_bar)
back_icon.layout.gravity = "top left"
back_icon.surface.blit(pygame.image.load("backbutton-2.png"), (0, 0))

tool_bar_title = pgp.Label(current_folder.title)
tool_bar_title.set_relative(tool_bar)
tool_bar_title.layout.align_left = 0
tool_bar_title.set_size(50)
tool_bar_title.layout.gravity = "centery"
tool_bar_title.layout.margin_left = 20

side_bar = frame.Component(main_component, frame.RELATIVE, COLOR.dark1)
side_bar.rect.w = 70
side_bar.layout.h = frame.MATCH

settings_button = b.DropDownButton(["SETTINGS", "DELETE FOLDER", "CALENDAR"])
settings_button.set_relative(side_bar)
settings_button.layout.w = frame.MATCH
settings_button.rect.h = 70
settings_button.spacing = 20
settings_button.layout.gravity = "bottom centerx"
settings_button.drop_buttons_width = 200
settings_button.menu_direction = b.UP
settings_button.draw_top = True
settings_button.set_round_edges(0.3)
settings_button.set_default_fill_color(COLOR.dark2)
settings_button.set_hover_color(COLOR.dark1)
settings_button.set_hold_color(COLOR.light1)
settings_button.set_border_color(COLOR.dark2)
settings_button.drop_buttons[0].on_release = open_settings
settings_button.drop_buttons[1].on_release = delete_current_folder
settings_button.drop_buttons[2].on_release = open_calendar

gear_icon = pgp.Drawable((70, 70))
gear_icon.set_relative(side_bar)
gear_icon.layout.gravity = "bottom left"
gear_icon.surface.blit(pygame.image.load("gearicon.png"), (6, 8))
gear_icon.draw_top = True

page_component = frame.Component(main_component, frame.RELATIVE, COLOR.light1)
page_component.scrollable = True
page_component.layout.align_top = 0
page_component.layout.align_left = 1
page_component.layout.w = frame.MATCH
page_component.layout.h = frame.MATCH

start_task_button = b.Button()
start_task_button.set_relative(main_component)
start_task_button.set_text("START SESSION")
start_task_button.set_width(200)
start_task_button.set_height(60)
start_task_button.set_round_edges(0.7)
start_task_button.layout.gravity = "centerx bottom"
start_task_button.layout.margin_bottom = 20
start_task_button.set_visibility(False)
start_task_button.set_active(False)
start_task_button.on_release = start_session

finish_button = b.Button()
finish_button.set_relative(main_component)
finish_button.set_text("CREATE")
finish_button.set_width(200)
finish_button.set_height(60)
finish_button.set_round_edges(0.7)
finish_button.layout.gravity = "centerx bottom"
finish_button.layout.margin_bottom = 20
finish_button.set_visibility(False)
finish_button.set_active(False)

sort_button = b.SelectorButton(["Priority", "Date"], 0)
sort_button.set_relative(tool_bar)
sort_button.layout.gravity = "right"
sort_button.rect.w = 120
sort_button.layout.h = frame.MATCH
sort_button.set_default_fill_color(COLOR.dark2)
sort_button.set_hover_color(COLOR.dark1)
sort_button.set_hold_color(COLOR.light1)
sort_button.set_border_color(COLOR.dark2)
sort_button.drop_buttons[0].on_release = sort_by_priority_on_click
sort_button.drop_buttons[1].on_release = sort_by_date_on_click

add_button = b.Button()
add_button.set_relative(main_component)
add_button.set_width(70)
add_button.set_height(70)
add_button.layout.gravity = "right bottom"
add_button.set_round_edges(1)
add_button.set_text("+")
add_button.set_text_size(80)
add_button.tAlignY = 0.75
add_button.layout.margin_bottom = 10
add_button.layout.margin_right = 10
add_button.on_release = add_task_or_folder
add_button.set_default_fill_color(COLOR.dark2)
add_button.set_hover_color(COLOR.dark1)
add_button.set_hold_color(COLOR.light1)
add_button.set_border_color(c.BLACK)

# loads main page (main folder)
load_folder_page(current_folder)

program_run = True
clock = pygame.time.Clock()


# --------------------Main Loop--------------------

while program_run:
    dt = clock.tick(120)/1000
    redraw()

    # variables for button processing
    click_bool = False
    release_bool = False
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            program_run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_bool = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                release_bool = True
        elif event.type == pygame.VIDEORESIZE:
            WIN = pygame.display.set_mode((max(event.w, MIN_WIDTH), max(event.h, MIN_HEIGHT)), pygame.RESIZABLE)
            main_component.update_screen(WIN)

    # processes clicks and keypresses
    main_component.process(click_bool, release_bool, pygame.mouse.get_pos(), None)
    main_component.process_focus(events, pygame.key.get_pressed())

pygame.quit()
