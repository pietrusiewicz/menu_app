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

        # localizations of tiles
        self.vals = [
                (h//2-4,w//2-6, 2,3), 
                (h//2-4,w//2-8, 2,w//2+5),
                (h//2-4,w//2-6, h//2+2, 3),
                (h//2-4,w//2-8, h//2+2, w//2+5)
            ]
        self.wins = [curses.newwin(a,b,c,d) for a,b,c,d in self.vals]
        scr.refresh()

        for i in range(4):
            for line in eval(f"t{i+1}"):
                self.wins[i].addstr(line, curses.color_pair(2))
            self.fill_color(i, 2)

        if self.y > 0:
            i = [[0,1], [1,1], [0,2], [1,2]].index(self.xy())
            self.fill_color(i, 4)

    # move in tile
    def inside_tile(self, scr, l):
        beg = self.xy()
        i = [[0,1], [1,1], [0,2], [1,2]].index(self.xy())
        win = self.wins[i]
        h,w = self.vals[i][:2]
        while True:
            for i, line in enumerate(l):
                win.addstr(i, 0, line)
            self.fill_color(i, 2)
            k = self.press_key(scr, [0,0, self.x>0,self.x<1])
            if type(k) != bool and ord(k) == 27:
                break
        
        self.x, self.y = beg

    def fill_color(self, i, n):
        self.wins[i].bkgd(' ', curses.color_pair(n))
        self.wins[i].refresh()

    def xy(self):
        return [self.x,self.y]

    def yx(self):
        return [self.y,self.x]
