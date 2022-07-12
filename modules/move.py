import curses

class Move:

    def __init__(self):
        self.a_z = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~\t "
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
        """
        first level in app
        """
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
            self.fill_color(self.wins[i], 2)

        if self.y > 0:
            i = [[0,1], [1,1], [0,2], [1,2]].index(self.xy())
            self.fill_color(self.wins[i], 4)


    # move in tile
    def tile_app(self, scr, win, d=['nic', 'takiego']):
        """
        display_tiles -> tile_app
        """
        self.d = d
        h,w = win.getmaxyx()
        scr.refresh()
        self.fill_color(win, 2)
        for i, line in enumerate(d):
            c = 6 if d[line] else 5
            win.addstr(i, 0, f"{line:{w}}", curses.color_pair(c))
            if self.y == i:
                win.addstr(i, 0, f"{line:{w}}", curses.color_pair(c) + curses.A_UNDERLINE)


        win.addstr(len(self.d), 0, f'{"+":{w}}', curses.color_pair(4 if len(self.d) == self.y else 2))
        win.refresh()

        k = self.press_key(scr, [self.y>0, self.y<len(self.d), 0,0])

        # arrow - move
        if not k:
            self.tile_app(scr,win, d=self.d)
        # key
        else:
            while True:
                # exit tile
                if ord(k) == 27:
                    break
                # delete item
                elif k in ("KEY_BACKSPACE", '\b', '\x7f'):
                    item = list(self.d)[self.y]
                    win.addstr(self.y,0, f"Are you sure to delete {item}? y/n")
                    while k := self.press_key(win, [0,0,0,0]).lower():
                        if k == 'y':
                            d.pop(item)
                            break
                        elif k == 'n':
                            break

                # press letter
                elif ord(k) in range(32, 127):
                    # edit add
                    key = self.edit_line(win, k)
                    d[key] = False

                # ENTER in tile
                elif ord(k) == 10:
                    if self.y < len(d):
                        d[list(d)[self.y]] = not d[list(d)[self.y]]
                    else:
                        key = self.edit_line(win, k)
                        d[key] = False


    
    #edit line in tile
    def edit_line(self, win, item):
        """
        display_tiles -> tile_app -> edit_line
        """
        win.addstr(self.y,0, f"{item}")
        while key := self.press_key(win, [0,0, 0,0]):
            #key = self.press_key(win, [0,0, 0,0])
            win.addstr(self.y,0, f"{item}")
            # press backspace
            if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                item = item[:-1]

            # press enter
            # exit insert mode 
            elif ord(key) == 10:
                return item

            # press letter
            elif key in self.a_z:
                item += key


    def fill_color(self, win, n):
        win.bkgd(' ', curses.color_pair(n))
        win.refresh()

    def xy(self):
        return [self.x,self.y]

    def yx(self):
        return [self.y,self.x]
