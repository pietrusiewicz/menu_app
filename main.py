import curses
import time
import sys
import json
import os

from modules.todolist import Todolist
from modules.snake import Snake
from modules.snapshot_ls import Snapshot
from modules.move import Move

class Menu:
    def __init__(self): #{{{ 
        self.m = Move()
        # content
        self.content = { # {{{
                "start": [f"{time.time()}", 
                 f"{time.strftime('%D %H:%M:%S')}", 
                 time.time.__doc__.split('\n')],
                "todolist": ["I don't know", "what do you have to do", ["press enter", "and check"]],
                "snake": ["Let's play", "Press enter to play", ['snake waits to', 'sssssss']],
                "snapshot_ls": ["snapshots paths","like you want", ["",""]]
            } # }}}
##############################################################################}}}

    # menu what displayes menu
    def main(self, scr): # {{{
        while True:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            self.display_menu(scr) 
############################################################################# }}}

    # display menu
    def display_menu(self,scr): # {{{
        self.m.clear_board(scr)

        # display topbar
        menu_str = "/0) start /1) todolist /2) snake /3) snapshot_ls"
        scr.addstr(0,0,menu_str, curses.color_pair(1))

        # mark selected option
        if self.m.y == 0: # {{{
            start_index = menu_str.find(str(self.m.x))-1
            end_index = menu_str.find(str(self.m.x+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2)) # }}}

        # execute func in 54 line
        self.display_tiles(scr)

        # press a key (execute func in 87 line)
        self.key = self.m.press_key(scr, [0,0,self.m.x>0,self.m.x<len(self.content)-1])
        if self.key:
            self.pressed_a_key(scr)
############################################################################## }}}

    # display tiles
    def display_tiles(self, scr): # {{{
        h,w = scr.getmaxyx()
        key = list(self.content.keys())[self.m.x]
        # render first row of tiles
        for i in range(2, int(h//2)-2):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))

        # first row of tiles
        scr.addstr(3, 3, self.content[key][0], curses.color_pair(2))
        scr.addstr(3, w//2+5, self.content[key][1], curses.color_pair(2))

        # render second row of tiles
        for i in range(int(h//2)+2, h-3):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))

        # second row of tiles
        for i, line in enumerate(self.content[key][2]):
            scr.addstr(h//2+5+i, 3, f"{line:{w//2-6}}", curses.color_pair(2))

        for i, line in enumerate(self.content[key][2]):
            scr.addstr(h//2+5+i, w//2+5, f"{line:{w//2-8}}", curses.color_pair(2)) 
############################################################################### }}}


    # press a key
    def pressed_a_key(self,scr): # {{{

        # ESCAPE key
        if ord(self.key) == 27:
            sys.exit()
        
        # ENTER key
        elif ord(self.key) == 10:
            if self.m.x == 1:
                t = Todolist(Move())
                t.main(scr)

            if self.m.x == 2:
                s = Snake(Move())
                s.main(scr)

            if self.m.x == 3:
                os.chdir('modules')
                if 'config.json' not in os.listdir():
                    json.dump({},open('config.json', 'w'))
                d = json.load(open('config.json'))
                if 'snapshot_ls' not in d:
                    d['snapshot_ls'] = []
                s = Snapshot(d['snapshot_ls'])
                s.config_app(scr)
                os.chdir('..')
######################################################################## }}}



if __name__ == '__main__':
    m = Menu()
    curses.wrapper(m.main)
