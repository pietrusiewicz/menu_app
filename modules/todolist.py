import curses
import os
import time
import sys

class Todolist:
    "Class that makes things to do"


    # declaring program variables 
    def __init__(self, m):
        self.m = m
        self.d, self.y={}, 0
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "

    # main loop
    def main(self, scr):
        "docstring of method"

        # colors in program
        self.program_colors()
        line, self.program = "", True
        while self.program:

            # display list of items
            for i in range(len(self.d)): # {{{
                item = list(self.d)[i]
                # True         or        False
                n = bool(self.d[item])+1
                line = f'{i+1}) {item} | {str(self.d[item]):5}'
                self.m.clear_board(scr)
                self.clrdis_line(scr, line, n=n,h=i)
                scr.addstr(scr.getmaxyx()[0]-1, 16, f"{self.m.y+1}")

            # display last line
            self.clrdis_line(scr, f"+)", h=len(self.d))

            # display options
            if self.m.y == len(self.d):
                self.clrdis_line(scr, "press LETTER KEY to start write", h=len(self.d)+1)
            else:
                self.clrdis_line(scr, "[d]elete [e]dit [c]lear", h=len(self.d)+1) # }}}

            # display selected item
            selected_is_true = False
            if self.m.y in range(len(self.d)):
                line = f"{str(self.m.y+1)+ ')' + list(self.d)[self.m.y]}"
                selected_is_true = self.d[list(self.d)[self.m.y]]
            else:
                line = f"+)"
                #line = f"{self.m.y+1})"
            self.clrdis_line(scr, line, n=5+selected_is_true,h=self.m.y)


            # press a key
# {{{----------------------------------------------------------------------------------
            #pressed_key = scr.getkey()
            key = self.m.press_key(scr, [self.m.y > 0, self.m.y < len(self.d), 1, 0])

            if key:
                # press enter
                if key == '\n': # {{{
                    if len(self.d) == 0:
                        self.insert_mode(scr)
                    elif len(self.d) != self.m.y:
                        k = list(self.d)[self.m.y]
                        self.d[k] = not self.d[k] # }}}

                # press a letter
                elif key.lower() in self.a_z: # {{{
                    self.press_letter(scr,key.lower()) # }}}

                elif key in ("KEY_BACKSPACE", '\b', '\x7f'):
                    self.insert_mode(scr,item=key[:-1]) # }}}


    # press a letter
    def press_letter(self, scr, pressed_key):
        "press a letter"
        # keybinds 
        if self.m.y in range(len(self.d)):
            # delete an item
            if pressed_key == 'd':
                to_remove = list(self.d)[self.m.y]
                self.clrdis_line(scr, f"Are you sure to delete {repr(to_remove)} y/n", h=len(self.d)+1)

                key = scr.getkey().lower()
                if key not in 'yn':
                    self.press_letter(scr, 'd')
                if key == 'y':
                    self.clrdis_line(scr, "", h=len(self.d)+1)
                    self.d.pop(to_remove)
                self.clrdis_line(scr, "[d]elete [e]dit [c]lear", h=len(self.d)+1) # }}}

            # edit an item
            elif pressed_key == 'e':
                self.insert_mode(scr, list(self.d)[self.m.y])

            # clear an item
            elif pressed_key == 'c':
                self.insert_mode(scr)


        # add new item
        elif len(self.d) == self.m.y:
            # pressed_key is first letter
            self.insert_mode(scr, pressed_key)


    # clear and display line
    def clrdis_line(self, scr, line, n=1, h=0): 
        scr.addstr(h, 0, f"{' ':{scr.getmaxyx()[1]}}", curses.color_pair(n))
        #statusbar = (curses.color_pair(n) | curses.A_UNDERLINE)
        scr.addstr(h, 0, f"{line}", curses.color_pair(n)) 


    # insert mode
    def insert_mode(self, scr, item=''):
        "insert like vim"

        scr.addstr(scr.getmaxyx()[0]-1, 0, "INSERT")

        w = (scr.getmaxyx()[1]//9)*2
        line = f'{self.m.y+1}){item}'
        self.clrdis_line(scr, "press ENTER to end edit an item", h=len(self.d)+1)
        self.clrdis_line(scr, f'{line}', h=self.m.y)


        key = scr.getkey()
        # press backspace
        if key in ("KEY_BACKSPACE", '\b', '\x7f'):
            self.insert_mode(scr, item[:-1])

        # press letter
        elif key in self.a_z:
            self.insert_mode(scr, item+key)

        # press enter
        elif key in '\n':
            if item in list(self.d):
                scr.addstr(len(self.d)+1, 0, f'{repr(item)} juz istnieje')

            # exit insert mode 
            else:
                # create item
                if len(self.d) == self.m.y:
                    self.d[item] = False
                # replace item
                else:
                    oldkey = list(self.d)[self.m.y]
                    self.d[item] = self.d.pop(oldkey) 
                self.m.y += 1
                scr.addstr(scr.getmaxyx()[0]-1, 0, "SELECT")


    # press an arrow
    def press_an_arrow(self, key):
        "docstring press arrow"
        if key == 'KEY_UP' and self.m.y > 0:
            self.m.y -= 1

        if key == 'KEY_DOWN' and self.m.y < len(self.d):
            self.m.y += 1

        if key == 'KEY_LEFT':
            self.program=False


    # colors in program
    def program_colors(self):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)

class Todolist2:
    def __init__(self, m):
        self.t1 = {'a':True, 'b':False, 'c':True}
        self.m = m

    def main(self, scr):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
        while True:
            self.m.display_tiles(scr, t1=self.t1)
            k = self.m.press_key(scr, [self.m.y>0,self.m.y<2, self.m.x>0,self.m.x<1])
            if type(k) != bool and ord(k) == 10:
                self.enter_tile(scr)

    def enter_tile(self, scr):
        beg = self.m.xy()
        n = [[0,1], [1,1], [0,2], [1,2]].index(beg)
        self.m.x, self.m.y = 0,0
        win = self.m.wins[n]

        self.m.tile_app(scr, win, d=self.t1)
        self.main(scr)


        self.m.x, self.m.y = beg


if __name__ == '__main__':
    #os.environ.setdefault('ESCDELAY', '25')
    import move
    t = Todolist2(move.Move())
    curses.wrapper(t.main)
#curses.wrapper(Todolist)
#print(Todolist.main.__doc__)
