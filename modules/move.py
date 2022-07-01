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
    def clear_board(self, scr): # {{{
        h,w = scr.getmaxyx()
        for y in range(h-1):
            for x in range(w):
                scr.addstr(y, x, " ")
############################################################################# }}}

    def xy(self):
        return [self.x,self.y]

    def yx(self):
        return [self.y,self.x]
