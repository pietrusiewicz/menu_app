import curses
import time

class Todolist:
    "docstring of class"
    def __init__(self, scr):
        # declaring program variables
        #{{{
        self.d,self.y={},[0,0]
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "
        self.colors = lambda x: curses.color_pair(x)
        self.main(scr)
        #}}}

    def main(self, scr):
        "docstring of method"

        self.program_colors(scr)
        # program colors
        #{{{
        #curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        #curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        #curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        #curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        #curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)
        #}}}
        while True:

            # display list of items
            #{{{
            for i, item in enumerate(self.d.keys()):
                # self.d[item] is not 0
                if not self.d[item]:
                    if i == self.y[0]:
                        color = self.colors(2)
                    else:
                        color = self.colors(1)
                    scr.addstr(i, 0, f'{i+1}) {item} | {str(self.d[item]):5}', color)
                else:
                    color = self.colors(4) if i == self.y[0] else self.colors(3)
                    scr.addstr(i, 0, f'{i+1}) {item} | {str(self.d[item]):5}', color)
            scr.addstr(len(self.d), 0, f'{len(self.d)+1})', self.colors(1))

            #}}}

            # when pressed a key
            #{{{
            pressed_key = scr.getkey()
            if pressed_key in ('KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'):
                # line 88
                self.press_arrow(pressed_key)

            # reverse bool
            elif pressed_key == '\n':
                try:
                    k = list(self.d.keys())[self.y[0]]
                    self.d[k] = not self.d[k]
                except IndexError:
                    self.insert_mode(scr)

            # enter letter
            elif pressed_key in self.a_z:
                self.insert_mode(scr, pressed_key)
            #scr.addstr(scr.getmaxyx()[0]-1,16, f"{pressed_key}")
            #}}}


    def insert_mode(self, scr, item=''):
        "docstring of method enter_item"
        scr.addstr(scr.getmaxyx()[0]-1,0, "INSERT")
        scr.addstr(scr.getmaxyx()[0]-1,16, f"{self.y[0]}")
        while True:
            scr.addstr(len(self.d), 0, f'{self.y[0]+1}) {item}', self.colors(1))
            key = scr.getkey()
            if key in ("KEY_BACKSPACE",'\b', '\x7f'):
                item = item[:-1]
            elif key in '\n':
                if item in list(self.d.keys()):
                    scr.addstr(len(self.d)+1, 0, f'{repr(item)} juz istnieje')
                else:
                    scr.addstr(scr.getmaxyx()[0]-1,0, "SELECT")
                    self.y[0] += 1
                break
            elif key in self.a_z:
                item += key
        self.d[item] = False

    def press_arrow(self, key):
        "docstring press arrow"
        if key == 'KEY_UP':
            if self.y[0] > 0:
                self.y[0] -= 1
        if key == 'KEY_DOWN':
            if self.y[0] < len(self.d)+1:
                self.y[0] += 1

    def program_colors(self, scr):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)

curses.wrapper(Todolist)
print(Todolist.main.__doc__)
