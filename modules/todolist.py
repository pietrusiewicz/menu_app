import curses
import time

class Todolist:
    "docstring of class"


    def __init__(self, scr):
        # declaring program variables
        # {{{
        self.d, self.y={}, 0
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "
        self.colors = lambda x: curses.color_pair(x)
        self.main(scr)
        # }}}--------------------------------------------------------------------------------------

    # main loop
    # {{{
    def main(self, scr):
        "docstring of method"
        # colors in program
        self.program_colors(scr)
        line = ""
    # }}}
        while True:

            # display list of items
            w = (scr.getmaxyx()[1]//9)*2  # {{{
            for i in range(len(self.d)): 
                item = list(self.d)[i]
                # True         or        False
                n = 2 if self.d[item] else 1
                line = f'{i+1}) {item} | {str(self.d[item]):5}'
                self.clrdis_line(scr, line, n=n,h=i)
                scr.addstr(scr.getmaxyx()[0]-1, 16, f"{self.y+1}")
                # display options
                self.clrdis_line(scr, "[d]elete [e]dit", h=len(self.d)+1) # }}}

            # display selected item
            if len(self.d) > self.y: # {{{
                line = f"{str(self.y+1)+ ')' + repr(list(self.d)[self.y])}"
            else:
                line = f"{self.y+1})"
            self.clrdis_line(scr, line, h=self.y, underline=True) # }}}


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
                    # self.y = 1 gdy list(self.d) = [' '] index 0
                    k = list(self.d)[self.y]
                    self.d[k] = not self.d[k] # }}}

            # press a letter
            elif pressed_key in self.a_z: # {{{
                self.press_letter(scr,pressed_key) # }}}
            # }}}----------------------------------------------------------------------------------

    # press a letter
    def press_letter(self, scr, pressed_key): # {{{

        # delete item
        if pressed_key == 'd': # {{{
            oldkey = list(self.d)[self.y-1]
            self.clrdis_line(scr, f"Are you sure to delete {repr(oldkey)} y/n", h=len(self.d)+1)
            while True:
                key = scr.getkey().lower()
                if key == 'y':
                    self.clrdis_line(scr, "", h=len(self.d)+1)
                    self.d.pop(oldkey)
                elif key == 'n':
                    break
            self.clrdis_line(scr, "[d]elete [e]dit", h=len(self.d)+1) # }}}

        # edit new item
        if pressed_key == 'e': # {{{
            self.insert_mode(scr, list(self.d)[self.y]) # }}}

        # add new item
        elif len(self.d) == self.y: # {{{
            # pressed_key is first letter
            self.insert_mode(scr, pressed_key) # }}}
    # }}}

    # clear and display line
    def clrdis_line(self, scr, line, n=1, h=0, underline=False): # {{{
        w = (scr.getmaxyx()[1]//9)*2
        scr.addstr(h, w, f"{'':{scr.getmaxyx()[1]-w}}", self.colors(n))
        if underline:
            statusbar = (curses.A_UNDERLINE | curses.color_pair(n))
            scr.addstr(h, w, line, statusbar)
        scr.addstr(h, w, line, self.colors(n)) # }}}

    # insert mode
    def insert_mode(self, scr, item=''): # {{{
        "docstring of method enter_item"
        
        scr.addstr(scr.getmaxyx()[0]-1, 0, "INSERT")
        while True:
            w = (scr.getmaxyx()[1]//9)*2
            line = f'{self.y+1}) {repr(item)}'
            self.clrdis_line(scr, f'{line}', h=self.y)


            key = scr.getkey()
            # press backspace
            if key in ("KEY_BACKSPACE", '\b', '\x7f'): # {{{
                item = item[:-1] # }}}

            # press enter
            elif key in '\n': # {{{
                if item in list(self.d):
                    scr.addstr(len(self.d)+1, 0, f'{repr(item)} juz istnieje')
                else:
                    scr.addstr(scr.getmaxyx()[0]-1, 0, "SELECT")
                    self.y += 1
                break # }}}
            # press letter
            elif key in self.a_z: # {{{
                item += key # }}}

        # exit insert mode
        # add item to self.d {{{
        if len(self.d) == self.y-1:
            self.d[item] = False
        # replace item
        else:
            oldkey = list(self.d)[self.y-1]
            self.d[item] = self.d.pop(oldkey) # }}}------------------------------------------------
    # }}}------------------------------------------------------------------------------------------

    # press an arrow
    def press_an_arrow(self, key): # {{{
        "docstring press arrow"
        if key == 'KEY_UP':
            if self.y > 0:
                self.y -= 1
        if key == 'KEY_DOWN':
            if self.y < len(self.d):
                self.y += 1
    # }}}------------------------------------------------------------------------------------------

    # colors in program
    # {{{ -----------------------------------------------------------------------------------------
    def program_colors(self, scr):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_WHITE)
        #curses.init_pair(7, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    # }}}------------------------------------------------------------------------------------------

curses.wrapper(Todolist)
print(Todolist.main.__doc__)
