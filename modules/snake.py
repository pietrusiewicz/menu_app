from curses import wrapper
import curses

class Snake:
    def __init__(self, scr):
        #TODO self.x, self.y
        key = scr.getkey()
        scr.addstr(key)
        key = scr.getkey()


wrapper(Snake)
