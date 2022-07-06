import curses

class Move:

    def __init__(self):
        self.x, self.y = 0,0

    def press_key(self, scr, cnds=[1,1,1,1], strictness=0):
        k = scr.getkey()
        if k in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
            if k == 'KEY_UP' and cnds[0]:
                self.y = self.y-1 if cnds[0] == 1 else int(cnds[0])
                if strictness:
                    return 0

            if k == 'KEY_DOWN' and cnds[1]:
                self.y = self.y+1 if cnds[1] == 1 else int(cnds[1])
                if strictness:
                    return 1

            if k == 'KEY_LEFT' and cnds[2]:
                self.x = self.x-1 if cnds[2] == 1 else int(cnds[2])
                if strictness:
                    return 2

            if k == 'KEY_RIGHT' and cnds[3]:
                self.x = self.x+1 if cnds[3] == 1 else int(cnds[3])
                if strictness:
                    return 3
            return False
        else:
            return k
    
    # clear board
    def clear_board(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w):
                scr.addstr(y, x, " ")

    # display tiles
    def display_tiles(self, scr, t1=[], t2=[], t3=[], t4=[]):
        h,w = scr.getmaxyx()
        #key = list(self.content)[self.m.x]

        # render background for [0] row
        for i in range(2, int(h//2)-2):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))
        if [self.x,self.y] == [0,1]:
            scr.addstr(2, 3, f'{" ":{w//2-6}}', curses.color_pair(4))
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(4))
        if [self.x,self.y] == [1,1]:
            scr.addstr(2, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(4))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(4))


        # render [1] row
        for i in range(int(h//2)+2, h-3):
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(2))
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(2))
        if [self.x,self.y] == [0,2]:
            scr.addstr(i, 3, f'{" ":{w//2-6}}', curses.color_pair(4))
            scr.addstr(h//2+2, 3, f'{" ":{w//2-6}}', curses.color_pair(4))
        if [self.x,self.y] == [1,2]:
            scr.addstr(i, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(4))
            scr.addstr(h//2+2, w//2+5, f'{" ":{w//2-8}}', curses.color_pair(4))

        # [0][0]
        for i, line in enumerate(t1):
            scr.addstr(3+i, 3, line, curses.color_pair(2))

        # [0][1]
        for i, line in enumerate(t2):
            scr.addstr(3+i, w//2+5, line, curses.color_pair(2))


        # [1][0]
        for i, line in enumerate(t3):
            scr.addstr(h//2+5+i, 3, f"{line:{w//2-6}}", curses.color_pair(2))

        # [1][1]
        for i, line in enumerate(t4):
            scr.addstr(h//2+5+i, w//2+5, f"{line:{w//2-8}}", curses.color_pair(2))





    def xy(self):
        return [self.x,self.y]

    def yx(self):
        return [self.y,self.x]
