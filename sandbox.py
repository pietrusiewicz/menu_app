import curses
import time
import sys


class Menu:
    def __init__(self,scr):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.xy = [0,0]
        self.content = {"start": [f"{time.time()}", f"{time.strftime('%D %H:%M:%S')}"]}
        self.main(scr)

    def main(self, scr):
        while True:
            self.display_menu(scr)

    # display menu
    def display_menu(self,scr): # {{{
        self.clear_board(scr)
        menu_str = "/0) start /1) snake /2) todolist"
        scr.addstr(0,0,menu_str, curses.color_pair(1))
        if self.xy[1] == 0:
            start_index = menu_str.find(str(self.xy[0]))-1
            end_index = menu_str.find(str(self.xy[0]+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2))
        self.display_tiles(scr)
        #scr.addstr(0,0,f"{ord(self.key)}")
        #scr.addstr(0,0,str(type(self.key)))
        self.key = scr.getkey()
        self.pressed_a_key() # }}}

    # display tiles
    def display_tiles(self, scr):
        h,w = scr.getmaxyx()
        # background
        for i in range(2, int(h//2)-2):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))

        scr.addstr(3, 3, self.content["start"][0], curses.color_pair(2))
        scr.addstr(3, w//2+5, self.content["start"][1], curses.color_pair(2))

        for i in range(int(h//2)+2, h-3):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))
    # press a key
    def pressed_a_key(self): # {{{
        arrows = ('KEY_UP', 'KEY_DOWN', "KEY_RIGHT", "KEY_LEFT")
        if self.key in arrows:

            choice = arrows.index(self.key)
            # UP
            if choice == 0:
                self.xy[1] -= 1

            # DOWN
            if choice == 1:
                self.xy[1] += 1

            # RIGHT
            if choice == 2:
                self.xy[0] += 1

            # LEFT
            if choice == 3:
                self.xy[0] -= 1

        # ESCAPE key
        elif ord(self.key) == 27:
            sys.exit() # }}}

    # clear board
    def clear_board(self, scr): #{{{
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}") # }}}

curses.wrapper(Menu)
