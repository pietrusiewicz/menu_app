import curses
import curses.textpad

class Snake:
    def __init__(self, scr):
        self.snake, self.xy,self.game = [], [0,0], True
        self.main(scr)

    def main(self, scr):
        while self.game:
            key = scr.getkey()
            self.press_key(scr, key)
            scr.addstr(self.xy[1], self.xy[0], '')

    def press_key(self, scr, key):
        h,w = scr.getmaxyx()
        if key == 'KEY_UP':
            if self.xy[1] > 0:
                self.xy[1] -= 1
            else:
                self.xy[1] = h-1
        if key == 'KEY_DOWN':
            if self.xy[1] < h-1:
                self.xy[1] += 1
            else:
                self.xy[1] = 0
        if key == 'KEY_LEFT':
            if self.xy[0] > 0:
                self.xy[0] -= 1
            else:
                self.xy[0] = w-1
        if key == 'KEY_RIGHT':
            if self.xy[0] < w-1:
                self.xy[0] += 1
            else:
                self.xy[0] = 0
        if key == '\n':
            self.game = False
        
curses.wrapper(Snake)
