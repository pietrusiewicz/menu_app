import os
import curses
import json

from config.select_file import Select
#s = curses.wrapper(Select)
#file_name = s.name

class Reader:
    def __init__(self,scr):
        self.config_pwd = os.getcwd()+'/config/config.json'
        self.y = 0
        self.check_files(scr)
        self.main(scr)

    def main(self, scr):
        while True:
            self.clear_board(scr)

            # display items
            scr.addstr(0, 0, f"Select text file what you want read:") # {{{
            for i in range(len(self.files)):
                scr.addstr(i+1, 0, f"{i+1}) {self.files[i]}")
            if len(self.files) == self.y:
                scr.addstr(self.y+1, 0, f"+)Add text file", curses.A_UNDERLINE)
            else:
                scr.addstr(self.y+1, 0, f"{self.y+1}) {self.files[self.y]}", curses.A_UNDERLINE)
                scr.addstr(len(self.files)+1, 0, f"+) Add text file") # }}}
            self.press_an_arrow(scr.getkey())

    # press an arrow
    def press_an_arrow(self, key): # {{{
        if key == 'KEY_UP' and self.y>0:
            self.y-=1
        if key == 'KEY_DOWN' and self.y<len(self.files):
            self.y+=1 # }}}

    def clear_board(self, scr):
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}")

    def check_files(self, scr):
        try:
            self.files = json.load(open(self.config_pwd))['files']
        except:
            Select(scr)
            self.check_files(scr)


curses.wrapper(Reader)
