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

    # place windows
    def create_tiles(self, scr):
        h,w = scr.getmaxyx()

        # localizations of tiles
        self.vals = [
                (h//2-4,w//2-6, 2,3), 
                (h//2-4,w//2-8, 2,w//2+5),
                (h//2-4,w//2-6, h//2+2, 3),
                (h//2-4,w//2-8, h//2+2, w//2+5)
            ]
        self.wins = [curses.newwin(a,b, c,d) for a,b, c,d in self.vals]
        scr.refresh()

    # display tiles
    def display_tiles(self, scr, t1=[], t2=[], t3=[], t4=[]):
        """
        first level in app
        """

        self.create_tiles(scr)

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
        second level in app
        display_tiles -> tile_app
        """
        h,w = win.getmaxyx()
        while True:

            # display todolist in tile
            scr.refresh()
            self.fill_color(win, 2)
            for i, line in enumerate(d):
                c = 6 if d[line] else 5
                win.addstr(i, 0, f"{line:{w}}", curses.color_pair(c))
                if self.y == i:
                    win.addstr(i, 0, f"{line:{w}}", curses.color_pair(c) + curses.A_UNDERLINE)


            win.addstr(len(d), 0, f'{"+":{w}}', curses.color_pair(4 if len(d) == self.y else 2))
            win.refresh()


            # press a key
            k = self.press_key(scr, [self.y>0, self.y<len(d), 0,0])

            # arrow - move
            if not k:
                continue
            # other keys
            else:
                # delete item
                if k in ("KEY_BACKSPACE", '\b', '\x7f'):
                    item = list(d)[self.y]
                    win.addstr(self.y,0, f"Are you sure to delete {item}? y/n")
                    while k := self.press_key(win, [0,0,0,0]).lower():
                        if k == 'y':
                            d.pop(item)
                            break
                        elif k == 'n':
                            break

                # exit tile
                elif ord(k) == 27:
                    break

                # press letter       A - z
                elif ord(k) in range(32, 127):
                    # edit item
                    if self.y < len(d):
                        item = list(d)[self.y]
                        newitem = self.edit_line(win, f"{item+k}")
                        d[newitem] = d[item]
                        d.pop(item)
                    # edit add
                    else:
                        key = self.edit_line(win, k)
                        d[key] = False

                # click in line ENTER
                elif ord(k) == 10:
                    if self.y < len(d):
                        d[list(d)[self.y]] = not d[list(d)[self.y]]
                    else:
                        key = self.edit_line(win, k)
                        d[key] = False
        return d

    
    # edit line in tile
    def edit_line(self, win, item):
        """
        third level in app
        display_tiles -> tile_app -> edit_line
        """
        win.addstr(self.y,0, f"{item}")
        while key := self.press_key(win, [0,0, 0,0]):
            try:
                # press backspace
                if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                    item = item[:-1]

                # press enter
                # exit insert mode 
                elif ord(key) == 10:
                    break
                # press letter
                elif key in self.a_z:
                    item += key
                win.addstr(self.y,0, f"{item+key:{win.getmaxyx()[1]-1}}")
            except KeyboardInterrupt:
                break
        return item


    def fill_color(self, win, n):
        win.bkgd(' ', curses.color_pair(n))
        win.refresh()

    def xy(self):
        return [self.x,self.y]

    def yx(self):
        return [self.y,self.x]
