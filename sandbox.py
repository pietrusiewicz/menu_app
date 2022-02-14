import curses
import os

class Reader:
    def __init__(self,scr):
        self.y = 0
        self.main(scr)

    def main(self, scr):
        #curses.init_color(curses.COLOR_)
        while True:
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
                scr.addstr(0,10, f"edytujesz {f}")
                scr.getkey()
    def clear(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w-1):
                scr.addstr(y,x," ")
        self.y = 0

curses.wrapper(Reader)
