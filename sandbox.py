import curses
import time
import sys

class Menu:
    def __init__(self,scr):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.key = "a"
        self.main(scr)

    def main(self, scr):
        while True:
            self.clear_board(scr)
            scr.addstr(0,0,"/0) start /1) snake /2) todolist", curses.color_pair(1))
            scr.addstr(0,0,f"{ord(self.key)}")
            #scr.addstr(0,0,str(type(self.key)))
            self.key = scr.getkey()
            if ord(self.key) == 27:
                sys.exit()
            #f = open(self.selected_file)

     # clear board
    def clear_board(self, scr): #{{{
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}") # }}}

curses.wrapper(Menu)
