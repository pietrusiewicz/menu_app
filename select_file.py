import curses
import os

class Select:
    def __init__(self,scr):
        self.y, self.app_running = 0, True
        self.main(scr)

    def main(self, scr):
        #curses.init_color(curses.COLOR_)
        while self.app_running:
            self.pwd = os.getcwd()
            scr.addstr(0,0, self.pwd)
            self.files = os.listdir()
            for i in range(len(self.files)):
                f = self.files[i]
                scr.addstr(i+1,0, f)
                if os.path.isdir(f):
                    scr.addstr(i+1,0, f)
            scr.addstr(self.y+1,0, self.files[self.y], curses.A_UNDERLINE)
            key = scr.getkey()
            self.press_an_arrow(scr, key)

    def press_an_arrow(self, scr, key):
        if key == 'KEY_DOWN' and self.y+1<len(self.files):
            self.y+=1
        if key == 'KEY_UP' and self.y>0:
            self.y-=1
        if key == 'KEY_LEFT':
            os.chdir('..')
            self.clear(scr)
        if key == 'KEY_RIGHT':
            f = self.files[self.y]
            if os.path.isdir(f):
                os.chdir(f)
            else:
                confirm =f"Are you sure to read {repr(f)}?"
                scr.addstr(len(self.files)+1,0, confirm)
                if scr.getkey() in 'Yy':
                    self.name = f"{self.pwd}/{f}"
                    self.app_running = False
                else:
                    scr.addstr(len(self.files)+1,0, f"{' ':{len(confirm)}}")
    def clear(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w-1):
                scr.addstr(y,x," ")
        self.y = 0

curses.wrapper(Select)
