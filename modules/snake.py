import curses
import random
import time

class Snake:
    def __init__(self, scr):
        # beginning values of snake
        self.start_time = time.time()
        h,w = [_//2 for _ in scr.getmaxyx()]
        self.snake,self.game = [[w-2,h],[w-1,h],[w,h]], True
        self.xy, self.fruit = [w, h],[0,0]
        self.direction,self.moves = '',0
        self.keys = ("KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT")
        self.main(scr)

    # main function
    def main(self, scr): # {{{
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        # place a fruit
        self.create_fruit(scr)

        while self.game:
            scr.addstr(self.xy[1], self.xy[0], '')
            self.moves += 1
            key = scr.getkey()
            # other key pressed 
            if self.press_key(scr, key):
                continue

            # when snake ate itself
            if self.xy in self.snake and self.moves > 3: # {{{
                self.end_screen(scr) # }}}

            # when snake ate fruit
            if self.xy == self.fruit: # {{{
                self.snake.append([int(self.xy[0]), int(self.xy[1])])
                self.create_fruit(scr)
            self.display_board(scr) # }}}
            # }}}

    # press key
    def press_key(self, scr, key): # {{{
        h,w = scr.getmaxyx()
        # enter
        if key == '\n':
            self.game = False


        # arrow up
        elif key == 'KEY_UP' and self.direction != 's':
            if self.xy[1] > 0:
                self.xy[1] -= 1
            else:
                self.xy[1] = h-2
            self.direction = 'n'


        # arrow down
        elif key == 'KEY_DOWN' and self.direction != 'n':
            if self.xy[1] < h-2:
                self.xy[1] += 1
            else:
                self.xy[1] = 0
            self.direction = 's'


        # arrow left
        elif key == 'KEY_LEFT' and self.direction != 'e':
            if self.xy[0] > 0:
                self.xy[0] -= 1
            else:
                self.xy[0] = w-1
            self.direction = 'w'


        # arrow right
        elif key == 'KEY_RIGHT' and self.direction != 'w':
            if self.xy[0] < w-1:
                self.xy[0] += 1
            else:
                self.xy[0] = 0
            self.direction = 'e' 
        else:
            self.moves -= 1
            key = ' '

        # is arrow or it isn't
        key = key not in self.keys
        return key
        # }}}

    # create fruit
    def create_fruit(self, scr): # {{{
        "creating in random place fruit"
        while True:
            h,w = [int((_-1)*random.random()) for _ in scr.getmaxyx()]
            check = [[x==w, y==h] for x,y in self.snake]
            #check = [[_[0]==w,_[1]==h] for _ in self.snake]
            if [True, True] not in check:
                break
        self.fruit = [w,h]
        #scr.addstr(h, w, "0", curses.color_pair(2)) # }}}

    # display content with snake and bottombar
    def display_board(self, scr): # {{{
        # height,width of cli screen
        h,w = scr.getmaxyx()

        # clear cli screen
        self.clear_board(scr)

        # strip and stretch snake
        self.snake_when_going()

        # display content of snake
        for x,y in self.snake:
            scr.addstr(y,x,' ', curses.color_pair(1))

        # display fruit
        scr.addstr(self.fruit[1], self.fruit[0], '0', curses.color_pair(2))

        # display bottombar
        scr.addstr(h-1,0, f"{len(self.snake)}, {self.fruit}, {self.direction}, {self.difference_seconds()}", curses.color_pair(2))
        scr.addstr(self.xy[1], self.xy[0], '', curses.color_pair(1)) # }}}

    # clear board
    def clear_board(self, scr): # {{{
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w):
                scr.addstr(y, x, " ") # }}}
    
    # when snake is going
    def snake_when_going(self): # {{{
        "strip and stretch snake"
        self.snake = self.snake[1:]; 
        self.snake.append([self.xy[0], self.xy[1]]) # }}}

    # ending of game
    def end_screen(self, scr): # {{{
        h,w = [_//2 for _ in scr.getmaxyx()]
        self.game=False
        # text with points, moves and time
        text = f"You lose with {len(self.snake)} points on {self.moves} moves in {self.difference_seconds()}s"
        scr.addstr(h,w-len(text)//2,text)
        scr.addstr(h+1,w-len(text)//2,"press enter to exit")
        while True:
            # enter ends game
            if scr.getkey() == '\n':
                break # }}}

    def difference_seconds(self):
        return int(time.time())-int(self.start_time)

#curses.wrapper(Snake)
