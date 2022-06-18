import curses
import time
import sys
#import inspect

from modules.todolist import Todolist
from modules.snake import Snake

class Menu:
    def __init__(self,scr):
        #self.key="a"
        self.xy = [0,0]
        self.content = {
                "start": [f"{time.time()}", 
                 f"{time.strftime('%D %H:%M:%S')}", 
                 time.time.__doc__.split('\n')],
                "todolist": ["I don't know", "what do you have to do", ["press enter", "and check"]],
                "snake": ["Let's play", "Press enter to play", ['snake waits to', 'sssssss']]
            }
        self.main(scr)

    # menu what displayes menu
    def main(self, scr): # {{{
        while True:
            curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
            self.display_menu(scr) # }}}

    # display menu
    def display_menu(self,scr): # {{{
        self.clear_board(scr)

        # display topbar
        menu_str = "/0) start /1) todolist /2) snake"
        scr.addstr(0,0,menu_str, curses.color_pair(1))

        # moving in topbar
        if self.xy[1] == 0: # {{{
            start_index = menu_str.find(str(self.xy[0]))-1
            end_index = menu_str.find(str(self.xy[0]+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2)) # }}}

        # execute func in 54 line
        self.display_tiles(scr)
        #scr.addstr(0,0,f"{ord(self.key)}")
        #scr.addstr(0,0,str(type(self.key)))

        # press a key (execute func in 79 line)
        self.key = scr.getkey()
        self.pressed_a_key(scr) # }}}

    # display tiles
    def display_tiles(self, scr): #{{{
        h,w = scr.getmaxyx()
        key = list(self.content.keys())[self.xy[0]]
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
            scr.addstr(h//2+5+i, w//2+5, f"{line:{w//2-8}}", curses.color_pair(2)) #}}}

    # press a key
    def pressed_a_key(self,scr): # {{{
        arrows = ('KEY_UP', 'KEY_DOWN', "KEY_RIGHT", "KEY_LEFT")
        if self.key in arrows:

            choice = arrows.index(self.key)
            """
            # UP
            if choice == 0:
                self.xy[1] -= 1

            # DOWN
            if choice == 1:
                self.xy[1] += 1
            """

            # RIGHT
            if choice == 2 and self.xy[0] < 4:
                self.xy[0] += 1

            # LEFT
            if choice == 3 and self.xy[0] > 0:
                self.xy[0] -= 1

        # ESCAPE key
        elif ord(self.key) == 27:
            sys.exit()
        
        # ENTER key
        elif ord(self.key) == 10:
            if self.xy[0] == 1:
                Todolist(scr)

            if self.xy[0] == 2:
                Snake(scr) # }}}

    # clear board
    def clear_board(self, scr): #{{{
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}") # }}}

curses.wrapper(Menu)
