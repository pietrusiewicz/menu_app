import curses
import random
import time

class Snake:

    # constructor
    def __init__(self, m): # {{{
        # beginning values of snake
        self.m = m
        self.start_time = time.time()
        self.direction,self.moves = '',0
        self.fruit = [0,0]
        #self.keys = ("KEY_UP","KEY_DOWN","KEY_LEFT","KEY_RIGHT")
############################################################ }}}


    # main function
    def main(self, scr): # {{{
        h,w = list(map(lambda x: x//2, scr.getmaxyx()))
        #h,w = [_//2 for _ in scr.getmaxyx()]
        self.snake,self.game = [[w-2,h],[w-1,h],[w,h]], True
        self.m.x = w
        self.m.y = h
        self.direction = ''
        #scr.addstr(0,0, f"{self.m.x,self.m.y}")
        #self.xy = [w, h]

        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_YELLOW)

        # place a fruit
        self.create_fruit(scr)
        while self.game:
            h,w = scr.getmaxyx()
            self.display_board(scr)
            #scr.addstr(0,0, '')
            scr.addstr(0,0, f"{list(self.m.xy())==self.fruit}")
            scr.addstr(self.m.y, self.m.x, '')
            self.moves += 1
            #key = scr.getkey()
            #l1 = list(map(lambda x: self.direction != x, list('nswe')))




            #l3 = list(map(lambda x : sum(list(map(int,x))) == 2, zip(l1,l2)))
            """
            l3 = [
                (1 if self.m.y > 0 else h-2) if self.direction != 's' else 0,
                (1 if self.m.y < h-2 else '0') if self.direction != 'n' else 0,
                (1 if self.m.x > 0 else w-1) if self.direction != 'e' else 0,
                (1 if self.m.x < w-1 else '0') if self.direction != 'w' else 0,
            ]
            """
            l3 = [
                1 if self.m.y > 0 else h-2,
                1 if self.m.y < h-2 else '0',
                1 if self.m.x > 0 else w-1,
                1 if self.m.x < w-1 else '0'
            ]

            key = self.m.press_key(scr, l3, strictness=1)
            if type(key) != int:
                self.press_key(key)
            # pressed arrow
            else:
                if self.direction == 'snew'[key]:
                    continue
                else:
                    self.direction = 'nswe'[key]




            # GAMEOVER - when snake ate itself
            if self.m.xy() in self.snake and self.moves > 3: # {{{
                self.end_screen(scr) # }}}

            # +1 - when snake ate fruit
            if self.m.xy() == self.fruit: # {{{
                self.snake.append([int(self.m.x), int(self.m.y)])
                self.create_fruit(scr)
            #self.display_board(scr) # }}}
############################################################ }}}


    # press key
    def press_key(self, key): # {{{
        #h,w = scr.getmaxyx()
        # enter
        if key == '\n':
            self.game = False
        else:
            self.moves -= 1
            key = ' '

############################################################################# }}}


    # create fruit
    def create_fruit(self, scr): # {{{
        "creating in random place fruit"
        while True:
            h,w = [int((_-1)*random.random()) for _ in scr.getmaxyx()]
            check = [[x==w, y==h] for x,y in self.snake]

            if [True, True] not in check:
                break
        self.fruit = [w,h]
############################################################################# }}}


    # display content with snake and bottombar
    def display_board(self, scr): # {{{
        # height,width of cli screen
        h,w = scr.getmaxyx()

        # clear cli screen
        self.m.clear_board(scr)

        # strip and stretch snake
        self.snake_when_going()

        # display content of snake
        for x,y in self.snake:
            scr.addstr(y,x,' ', curses.color_pair(1))

        # display fruit
        scr.addstr(self.fruit[1], self.fruit[0], '0', curses.color_pair(2))

        # display bottombar
        bottombar = f"{len(self.snake)}, {self.fruit}, {self.direction}, {self.difference_seconds()}"
        scr.addstr(h-1,0, bottombar, curses.color_pair(2))
        scr.addstr(self.m.y, self.m.x, '', curses.color_pair(1))
############################################################################# }}}


    # when snake is going
    def snake_when_going(self): # {{{
        "strip and stretch snake"
        self.snake = self.snake[1:]; 
        self.snake.append([self.m.x, self.m.y])

############################################################################# }}}


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
                break 
############################################################################# }}}


    def difference_seconds(self): # {{{
        return int(time.time())-int(self.start_time)

############################################################################# }}}

if __name__ == '__main__':
    s = Snake(__import__('move').Move())
    curses.wrapper(s.main)
