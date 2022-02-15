from config.select_file import Select
import curses

s = curses.wrapper(Select)
file_name = s.name

class Reader:
    def __init__(self):
        self.last
