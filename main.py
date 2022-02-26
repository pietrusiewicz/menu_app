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

            if self.y==2:
                self.launch_reader(scr)

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

# READER ======================================================================================={{{
    def launch_reader(self, scr):
        self.d.table_name='texts'
        just_created = self.d.check_table()
        r = Reader()
        s = Select()
        if just_created:
            file_name = s.get_filename(scr)
            text = r.get_text()
            self.d.insert_into([file_name,text, 0, 1])
            #got_filename = s.selected_file
            r.select_file_to_read(scr)
        t = self.d.select("WHERE last_open=1")[0]
        #t = "Kobyła. ma. mały. bok."
        i = 0
        r.page_lines = 5
        self.loop=True
        while self.loop:
            r.read(scr, t[3]+i)
            key = scr.getkey()
            if key == 'KEY_DOWN':
                i += 1
            if key == 'KEY_UP':
                i -= 1
            if key == 'KEY_RIGHT':
                i += r.page_lines
            if key == 'KEY_LEFT':
                i -= r.page_lines
            if key == 'q':
                self.loop = False
            # change read file
            if key == '0':
                return r.select_file_to_read(scr) #}}}
# ==============================================================================================}}}
    #def 

if __name__ == '__main__':
    curses.wrapper(Menu)
