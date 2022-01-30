import curses

class Blog:
    def __init__(self):
        self.az = '0123456789 !"#$%&\'()*+,-./:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
        self.title, self.post = 0,0

    def write_post(self):
        title = self.word_editor()
        post = self.word_editor(2)

    def word_editor(self, n=1):
        string,x,y,lines = "",0,0,[]
        while True:
            num_rows, num_cols = self.scr.getmaxyx()
            self.scr.addstr(num_rows-1, x, f"{string:{num_cols-1}}")
            ch = int(str(self.scr.getch()))
            if chr(ch) in self.az: 
                string += chr(ch)
            else:
                if ch in (65,66,67,68) and n==2:
                    if ch == 65: y -= 1 # up
                    elif ch==66: y += 1 # down
                    elif ch==67: x += 1 # right
                    elif ch==68: x -= 1 # left

                    if y<0: y = num_cols - 1
                    elif y>num_cols-1: y = 0
                    elif x<0: x=num_rows - 1
                    elif x>num_rows-1: x = 0

                elif ch in (10, 13): # press enter
                    break
                    lines.append(string)
                    string=''
                elif ch == 127: # press backspace
                    string = string[:-1]
                elif ch == 27: # press escape
                    curses.endwin()
                    break

        return string
