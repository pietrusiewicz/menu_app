import curses
import time
import sys
import json
import os

from modules.todolist import Todolist
from modules.snake import Snake
from modules.snapshot_ls import Snapshot
from modules.move import Move



class Menu(Move):
    def __init__(self):
        Move.__init__(self)
        
        # content
        self.content = { 
                "start": [
                    {"assier"},
                    {'illaramendi'},
                    {'mattias'},
                    {'johanson'}
                ],
                "todolist": [
                    {},
                    {},
                    {'ale nie'},
                    {}
                ],
                "snake": [
                    {},
                    {},
                    {},
                    {}
                ],
                "snapshot_ls": [
                    {},
                    {},
                    {},
                    {}
                ]
            }


    # menu what displayes menu
    def main(self, scr): 
        while True:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
            self.display_menu(scr) 
            # press a key (execute func in 87 line)
            l = [self.y>0,self.y<2, self.x>0,self.x<len(self.content)-1]
            self.key = self.press_key(scr, l)
            if self.key:
                self.pressed_a_key(scr)


    # display menu
    def display_menu(self,scr):
        self.clear_board(scr)

        # display topbar
        menu_str = "/0) start      /1) todolist   /2) snake      /3) snapshot_ls"
        scr.addstr(0,0,menu_str, curses.color_pair(1))

        # mark selected option
        if self.y == 0:
            start_index = menu_str.find(str(self.x))-1
            end_index = menu_str.find(str(self.x+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2))

            key = list(self.content)[self.x]

            self.display_tiles(scr, 
                    t1=self.content[key][0],
                    t2=self.content[key][1],
                    t3=self.content[key][2],
                    t4=self.content[key][3],
            )

        if self.y > 0:
            self.tiles_for_app(scr)




    def tiles_for_app(self, scr):
        beg = self.x
        key = list(self.content)[self.x]
        self.x = 0 
        while True:
            self.display_tiles(scr, 
                    t1=self.content[key][0],
                    t2=self.content[key][1],
                    t3=self.content[key][2],
                    t4=self.content[key][3],
            )

            self.press_key(scr, cnds=[self.y>0,self.y<2, self.x>0,self.x<3])
            if self.y==0:
                break
        self.x = beg
        self.display_menu(scr)


    # press a key
    def pressed_a_key(self,scr):

        # ESCAPE key
        if ord(self.key) == 27:
            sys.exit()
        
        # ENTER key
        elif ord(self.key) == 10:
            if self.x == 1:
                t = Todolist(Move())
                t.main(scr)

            if self.x == 2:
                s = Snake(Move())
                s.main(scr)

            if self.x == 3:
                if 'modules/config.json' not in os.listdir('modules'):
                    json.dump({},open('config.json', 'w'))
                d = json.load(open('config.json'))
                if 'snapshot_ls' not in d:
                    d['snapshot_ls'] = []
                s = Snapshot(d['snapshot_ls'])
                s.config_app(scr)


if __name__ == '__main__':
    m = Menu()
    curses.wrapper(m.main)
    #m.main()
