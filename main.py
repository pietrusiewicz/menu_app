import curses
import sys

from modules.todolist import Todolist
from modules.snake import Snake
from modules.text_reader import Reader

from config.select_file import Select
from config.database import Database

class Menu:
    def __init__(self, scr):
        self.apps = ['todolist', 'blog', 'text_reader','snake', 'end']
        self.y = 0
        self.d = Database()
        self.main(scr)
    

    def main(self, scr):
        w = scr.getmaxyx()[1]//9
        # selected
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        for i in range(len(self.apps)):
            if i == self.y:
                scr.addstr(i, 0, self.apps[i], curses.color_pair(1))
            else:
                scr.addstr(i, 0, self.apps[i])

        # press any key
        key = scr.getkey() # {{{
        if key in ("KEY_UP", "KEY_DOWN"):
            if key == "KEY_UP" and self.y>0:
                self.y -= 1
            if key == "KEY_DOWN" and self.y+1<len(self.apps):
                self.y += 1
            self.main(scr)
            
        elif key in ('\n', "KEY_RIGHT"):

            if self.y==0:
                #t = Todolist(scr)
                Todolist(scr)
                #t.main(scr)

# READER ======================================================================================={{{
            if self.y==2:
                r = Reader()
                if r.files_wrong():
                    # repairs json file
                    s = Select()
                    s.get_filename(scr)
                    self.d.table_name='texts'
                    self.d.check_table()
                    #(text_pwd, content, nr_sentence, last_open)
                    content = ' '.join([line.replace('\n','').replace("'",'"') for line in open(self.name).readlines()])
                    data = [self.name, content, 0, 1]
                    self.d.insert_into(data)
                t = self.d.raw_query("SELECT * FROM texts WHERE last_open=1")[0]
                r.main(scr, t)
# ==============================================================================================}}}
            if self.y==3:
                #s = Snake(scr)
                Snake(scr)
                #s.main(scr)
            if self.y==len(self.apps)-1:
                curses.endwin()
                sys.exit()
            self.main(scr)
        else:
            self.main(scr)
        #scr.addstr(15, 15, f'{self.apps[self.y]} {self.y}')
        # }}}

if __name__ == '__main__':
    curses.wrapper(Menu)
