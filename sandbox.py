from select_file import Select
import curses

s = curses.wrapper(Select)
print(s.name)
