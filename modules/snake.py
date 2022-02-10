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
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        hw = scr.getmaxyx()
        self.make_fruit(scr,hw)
        while True:
            self.clear_board(scr)
            self.make_full_snake(scr)
            key = scr.getkey()
            hw = scr.getmaxyx()
            self.press_an_arrow(scr,key,hw)

    def make_full_snake(self,scr):
        for x,y in self.snake:
            scr.addstr(y, x, ' ', curses.color_pair(1))
        scr.addstr(self.fruit[1], self.fruit[0], '0', curses.color_pair(2))
        scr.addstr(self.xy[1], self.xy[0], '',curses.color_pair(1))
            #scr.addstr(10,0, f"{x} {y}")

    def clear_board(self, scr):
        h, w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w-1):
                scr.addstr(y, x, ' ')

    # eat a fruit
    def eat_fruit(self):
        self.snake.append(self.xy)

    # make a fruit
    def make_fruit(self, scr, hw): #{{{
        #scr.addstr(self.xy[1], self.xy[0], ' ', curses.color_pair(1))
        #self.snake.append(self.xy)
        h,w = [int(_*random.random()) for _ in hw]
        self.fruit = [w,h]
        scr.addstr(h, w, '0', curses.color_pair(2)) #}}}

    # press an arrow
    def press_an_arrow(self,scr, key, hw): # {{{
        h,w = hw
        if key == 'KEY_UP':
            if self.xy[1]-1 < 0:
                self.xy[1] = h-1
            else:
                self.xy[1] -= 1
        if key == 'KEY_DOWN':
            if self.xy[1]+1 >= h:
                self.xy[1] = 0
            else:
                self.xy[1] += 1
        if key == 'KEY_RIGHT':
            if self.xy[0]+1 >= w:
                self.xy[0] = 0
            else:
                self.xy[0] += 1
        if key == 'KEY_LEFT':
            if self.xy[0]-1 <0:
                self.xy[0] = w-1
            else:
                self.xy[0] -= 1
        if key == '\n':
            scr.addstr(h-1,0, str(self.xy))
            scr.addstr(h-1,8, str(self.fruit))

        if self.xy == self.fruit:
            self.eat_fruit()
            self.make_fruit(scr, hw)

        # }}}

wrapper(Snake)
