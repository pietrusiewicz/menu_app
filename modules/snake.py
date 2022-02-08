from curses import wrapper
import curses
import random

class Snake:
    def __init__(self, scr):
        self.xy = [0, 0]
        self.direction = 'RIGHT'
        self.fruit = [0,0]
        self.snake = []

        while True:
            scr.addstr("press any key to start")
            scr.getkey()
            scr.addstr(0,0,"                      ")
            break
        self.main(scr)

    def main(self, scr):
        hw = scr.getmaxyx()
        self.make_fruit(scr,hw)
        while True:
            key = scr.getkey()
            hw = scr.getmaxyx()
            self.press_an_arrow(scr,key,hw)
            scr.addstr(self.xy[1], self.xy[0], ' ')

    def press_an_arrow(self,scr, key, hw):
        h,w = hw
        if key == 'KEY_UP':
            if self.xy[1]-1 < 0:
                self.xy[1] = h-1
            self.xy[1] -= 1
        if key == 'KEY_DOWN':
            if self.xy[1]+1 >= h-1:
                self.xy[1] = 0
            self.xy[1] += 1
        if key == 'KEY_RIGHT':
            if self.xy[0]+1 >= w-1:
                self.xy[0] = 0
            self.xy[0] += 1
        if key == 'KEY_LEFT':
            if self.xy[0]-1 <0:
                self.xy[0] = w-1
            self.xy[0] -= 1

    def make_fruit(self, scr, hw):
        h,w = [int(_*random.random()) for _ in hw]
        self.fruit = [h,w]
        scr.addstr(h, w, '_')

    def eat_fruit(self):
        self.snake.append((self.xy[0], self.xy[1]))
            


wrapper(Snake)
