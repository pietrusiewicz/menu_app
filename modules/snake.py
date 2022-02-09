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
            #self.make_full_snake()
            key = scr.getkey()
            hw = scr.getmaxyx()
            self.press_an_arrow(scr,key,hw)
            scr.addstr(self.xy[1], self.xy[0], '')

    def press_an_arrow(self,scr, key, hw):
        h,w = hw
        if key == 'KEY_UP':
            if self.xy[1]-1 < 0:
                self.xy[1] = h-1
            else:
                self.xy[1] -= 1
        if key == 'KEY_DOWN':
            if self.xy[1]+1 >= h-1:
                self.xy[1] = 0
            else:
                self.xy[1] += 1
        if key == 'KEY_RIGHT':
            if self.xy[0]+1 >= w-1:
                self.xy[0] = 0
            else:
                self.xy[0] += 1
        if key == 'KEY_LEFT':
            if self.xy[0]-1 <0:
                self.xy[0] = w-1
            else:
                self.xy[0] -= 1
        if self.xy == self.fruit:
            self.make_fruit(scr, hw)

        scr.addstr(h-1,0, str(self.xy))
        scr.addstr(h-1,8, str(self.fruit))

    def make_fruit(self, scr, hw):
        scr.addstr(self.xy[1], self.xy[0], ' ')
        self.snake.append(self.xy)
        h,w = [int(_*random.random()) for _ in hw]
        self.fruit = [w,h]
        scr.addstr(h, w, '0')

    #def make_full_snake(self):
        

wrapper(Snake)
