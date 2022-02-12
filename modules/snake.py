import curses
import random
import time

class Snake:
    def __init__(self, scr):
        h,w = [_//2 for _ in scr.getmaxyx()]
        self.snake,self.game = [[w-2,h],[w-1,h],[w,h]], True
        self.xy, self.fruit = [w, h],[0,0]
        self.direction,self.moves = '',0
        self.keys = ("KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT")
        self.main(scr)

    def main(self, scr):
        now = time.time()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_YELLOW)
        self.create_fruit(scr)
        while self.game:
            self.moves += 1
            key = scr.getkey()
            if self.press_key(scr, key):
                continue
            if self.xy in self.snake and self.moves > 3:
                self.end_screen(scr, now)
            if self.xy == self.fruit:
                self.snake.append([int(self.xy[0]), int(self.xy[1])])
                self.create_fruit(scr)
            self.display_board(scr)
            scr.addstr(self.xy[1], self.xy[0], '')

    # press key
    def press_key(self, scr, key): # {{{
        h,w = scr.getmaxyx()
        if key == '\n':
            self.game = False
        elif key == 'KEY_UP' and self.direction != 's':
            if self.xy[1] > 0:
                self.xy[1] -= 1
            else:
                self.xy[1] = h-2
            self.direction = 'n'
        elif key == 'KEY_DOWN' and self.direction != 'n':
            if self.xy[1] < h-2:
                self.xy[1] += 1
            else:
                self.xy[1] = 0
            self.direction = 's'
        elif key == 'KEY_LEFT' and self.direction != 'e':
            if self.xy[0] > 0:
                self.xy[0] -= 1
            else:
                self.xy[0] = w-1
            self.direction = 'w'
        elif key == 'KEY_RIGHT' and self.direction != 'w':
            if self.xy[0] < w-1:
                self.xy[0] += 1
            else:
                self.xy[0] = 0
            self.direction = 'e' 
        else:
            self.moves -= 1
            key = ' '
        key = key not in self.keys
        return key
        # }}}

    def create_fruit(self, scr):
        h,w = [int((_-1)*random.random()) for _ in scr.getmaxyx()]
        self.fruit = [w,h]
        scr.addstr(h, w, "0", curses.color_pair(2))

    def display_board(self, scr):
        h,w = scr.getmaxyx()
        self.clear_board(scr)
        self.snake_when_going()
        scr.addstr(self.fruit[1], self.fruit[0], '0', curses.color_pair(2))
        for x,y in self.snake:
            scr.addstr(y,x,'=', curses.color_pair(1))
        scr.addstr(h-1,0, f"{len(self.snake)}, {self.fruit}, {self.direction} ", curses.color_pair(2))
        scr.addstr(self.xy[1], self.xy[0], '', curses.color_pair(1))

    def clear_board(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w):
                scr.addstr(y, x, " ")
    
    def snake_when_going(self):
        self.snake = self.snake[1:]; 
        self.snake.append([self.xy[0], self.xy[1]])

    def end_screen(self, scr, start_time):
        h,w = [_//2 for _ in scr.getmaxyx()]
        self.game=False
        text = f"You lose with {len(self.snake)} points on {self.moves} moves in {int(time.time())-int(start_time)}s"
        scr.addstr(h,w-len(text)//2,text)
        scr.getkey()
        
curses.wrapper(Snake)
