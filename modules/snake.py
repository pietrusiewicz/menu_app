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
            l1 = list(map(lambda x: self.direction != x, list('nswe')))
            
            l2 = [1 if self.m.y > 0 else h-2,
                 1 if self.m.y < h-2 else '0',
                 1 if self.m.x > 0 else w-1,
                 1 if self.m.x < w-1 else '0'
            ]
            l3 = list(map(lambda x : sum(list(map(int,x))) == 2, zip(l1,l2)))
            # pressed arrow
            if not self.m.press_key(scr, l3):
                self.direction = 'nswe'[l3.index(1)]
                continue
            else:
                self.press_key()
            #if self.press_key(scr, key):

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
    def press_key(self): # {{{
        h,w = scr.getmaxyx()
        # enter
        if key == '\n':
            self.game = False
        else:
            self.moves -= 1
            key = ' '

        """
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

        # is arrow or it isn't
        key = key not in self.keys
        return key
        """
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
        scr.addstr(h-1,0, f"{len(self.snake)}, {self.fruit}, {self.direction}, {self.difference_seconds()}", curses.color_pair(2))
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

#curses.wrapper(Snake)
