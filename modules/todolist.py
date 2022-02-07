import curses
import time
import sys

class Todolist:
    "docstring of class"


    # declaring program variables 
    def __init__(self, scr): # {{{
        self.d, self.y={}, 0
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "
        #self.main(scr) # }}}

    # main loop
    def main(self, scr): # {{{
        "docstring of method"
        # colors in program
        self.program_colors(scr)
        line, self.program = "", True
        while self.program:

            # display list of items
            for i in range(len(self.d)): # {{{
                item = list(self.d)[i]
                # True         or        False
                n = 2 if self.d[item] else 1
                line = f'{i+1}) {item} | {str(self.d[item]):5}'
                self.clrdis_line(scr, line, n=n,h=i)
                scr.addstr(scr.getmaxyx()[0]-1, 16, f"{self.y+1}")

            # display last line
            self.clrdis_line(scr, f"+)", h=len(self.d))
            # display options
            if self.y == len(self.d):
                self.clrdis_line(scr, "press LETTER KEY to start write", h=len(self.d)+1)

            else:
                self.clrdis_line(scr, "[d]elete [e]dit [c]lear", h=len(self.d)+1) # }}}

            # display selected item
            selected_is_true = False # {{{
            if self.y in range(len(self.d)):
                line = f"{str(self.y+1)+ ')' + list(self.d)[self.y]}"
                selected_is_true = self.d[list(self.d)[self.y]]
            else:
                line = f"+)"
                #line = f"{self.y+1})"
            self.clrdis_line(scr, line, n=5+selected_is_true,h=self.y) # }}}


            # press a key
            # {{{----------------------------------------------------------------------------------
            pressed_key = scr.getkey()

            # press arrow 
            if pressed_key in ('KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'): # {{{
                # line 88
                self.press_an_arrow(pressed_key) # }}}

            # press enter
            elif pressed_key == '\n': # {{{
                if len(self.d) == 0:
                    self.insert_mode(scr)
                elif len(self.d) != self.y:
                    k = list(self.d)[self.y]
                    self.d[k] = not self.d[k] # }}}

            # press a letter
            elif pressed_key.lower() in self.a_z: # {{{
                self.press_letter(scr,pressed_key.lower()) # }}}
            # }}}----------------------------------------------------------------------------------

        # }}} 

    # press a letter
    def press_letter(self, scr, pressed_key): # {{{

        # press an letter
        # keybinds {{{-----------------------------------------------------------------------------
        if self.y in range(len(self.d)):
            # delete an item
            if pressed_key == 'd': # {{{
                to_remove = list(self.d)[self.y]
                self.clrdis_line(scr, f"Are you sure to delete {repr(to_remove)} y/n", h=len(self.d)+1)
                key = scr.getkey().lower()
                if key not in 'yn':
                    self.press_letter(scr, 'd')
                if key == 'y':
                    self.clrdis_line(scr, "", h=len(self.d)+1)
                    self.d.pop(to_remove)
                self.clrdis_line(scr, "[d]elete [e]dit [c]lear", h=len(self.d)+1) # }}}

            # edit an item
            elif pressed_key == 'e': # {{{
                self.insert_mode(scr, list(self.d)[self.y]) # }}}

            # clear an item
            elif pressed_key == 'c': # {{{
                self.insert_mode(scr) # }}}

        # }}}--------------------------------------------------------------------------------------

        # add new item
        elif len(self.d) == self.y: # {{{
            # pressed_key is first letter
            self.insert_mode(scr, pressed_key) # }}}
    # }}}

    # clear and display line
    def clrdis_line(self, scr, line, n=1, h=0): # {{{
        w = (scr.getmaxyx()[1]//9)*2
        scr.addstr(h, w, f"{'':{scr.getmaxyx()[1]-w}}", curses.color_pair(n))
        #statusbar = (curses.color_pair(n) | curses.A_UNDERLINE)
        scr.addstr(h, w, f"{line}", curses.color_pair(n)) # }}}

    # insert mode
    def insert_mode(self, scr, item=''): # {{{
        "docstring of method enter_item"
        
        scr.addstr(scr.getmaxyx()[0]-1, 0, "INSERT")

        w = (scr.getmaxyx()[1]//9)*2
        line = f'{self.y+1}){item}'
        self.clrdis_line(scr, "press ENTER to end edit an item", h=len(self.d)+1)
        self.clrdis_line(scr, f'{line}', h=self.y)


        key = scr.getkey()
        # press backspace
        if key in ("KEY_BACKSPACE", '\b', '\x7f'): # {{{
            self.insert_mode(scr, item[:-1]) # }}}

        # press letter
        elif key in self.a_z: # {{{
            self.insert_mode(scr, item+key) # }}}
        # press enter
        elif key in '\n': # {{{
            if item in list(self.d):
                scr.addstr(len(self.d)+1, 0, f'{repr(item)} juz istnieje')

            # exit insert mode 
            else:
                # create item
                if len(self.d) == self.y:
                    self.d[item] = False
                # replace item
                else:
                    oldkey = list(self.d)[self.y]
                    self.d[item] = self.d.pop(oldkey) 
                self.y += 1
                scr.addstr(scr.getmaxyx()[0]-1, 0, "SELECT")
        # }}}
    # }}}------------------------------------------------------------------------------------------

    # press an arrow
    def press_an_arrow(self, key): # {{{
        "docstring press arrow"
        if key == 'KEY_UP' and self.y > 0:
            self.y -= 1
        if key == 'KEY_DOWN' and self.y < len(self.d):
            self.y += 1
        if key == 'KEY_LEFT':
            self.program=False
    # }}}------------------------------------------------------------------------------------------

    # colors in program
    # {{{ -----------------------------------------------------------------------------------------
    def program_colors(self, scr):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(7, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # }}}------------------------------------------------------------------------------------------

curses.wrapper(Todolist)
print(Todolist.main.__doc__)
