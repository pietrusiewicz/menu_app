import curses
import random

class Snake:
    def __init__(self, scr):
        h,w = [_//2 for _ in scr.getmaxyx()]
        self.snake,self.game = [[w-2,h],[w-1,h],[w,h]], True
        self.xy, self.fruit = [w, h],[0,0]
        self.main(scr)

    def main(self, scr):
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        self.create_fruit(scr)
        moves=0
        while self.game:
            moves += 1
            key = scr.getkey()
            self.press_key(scr, key)
            if self.xy in self.snake and moves > 3:
                self.game=False
            scr.addstr(self.xy[1], self.xy[0], '')
            if self.xy == self.fruit:
                self.snake.append([int(self.xy[0]), int(self.xy[1])])
                self.create_fruit(scr)
            self.clear_and_display_board(scr)

    def press_key(self, scr, key):
        h,w = scr.getmaxyx()
        if key == 'KEY_UP':
            if self.xy[1] > 0:
                self.xy[1] -= 1
            else:
                self.xy[1] = h-2
        if key == 'KEY_DOWN':
            if self.xy[1] < h-2:
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

    def create_fruit(self, scr):
        h,w = [int((_-1)*random.random()) for _ in scr.getmaxyx()]
        self.fruit = [w,h]
        scr.addstr(h, w, "0", curses.color_pair(2))

    def clear_and_display_board(self, scr):
        h,w = scr.getmaxyx()
        self.snake = self.snake[1:];self.snake.append([self.xy[0], self.xy[1]])
        for y in range(h-1):
            for x in range(w):
                scr.addstr(y, x, " ")
        scr.addstr(self.fruit[1], self.fruit[0], '0', curses.color_pair(2))
        for x,y in self.snake:
            scr.addstr(y,x,'=', curses.color_pair(1))
        scr.addstr(h-1,0, f"{len(self.snake)}, {self.fruit}", curses.color_pair(2))
        scr.addstr(self.xy[1], self.xy[0], '', curses.color_pair(1))

        
curses.wrapper(Snake)
