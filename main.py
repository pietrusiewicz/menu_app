import curses
#from modules.todolist import Todolist

class Menu:
    def __init__(self, scr):
        self.apps = ['todolist', 'blog', 'pdf_reader']
        self.y = 0
        self.main(scr)
    
    def main(self, scr):
        while True:
            # selected
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

            for i in range(len(self.apps)):
                if i == self.y:
                    scr.addstr(i, 0, self.apps[i], curses.color_pair(1))
                else:
                    scr.addstr(i, 0, self.apps[i])

            key = scr.getkey()
            if key in ("KEY_UP", "KEY_DOWN"):
                if key == "KEY_UP" and self.y>0:
                    self.y -= 1
                if key == "KEY_DOWN" and self.y+1<len(self.apps):
                    self.y += 1
            scr.addstr(15, 15, f'{self.apps[self.y]} {self.y}')
            

if __name__ == '__main__':
    curses.wrapper(Menu)
