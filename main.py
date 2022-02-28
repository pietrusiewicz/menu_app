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
        # first time launch
        if just_created: # {{{
            file_name = s.get_filename(scr)
            text = r.get_text(file_name)
            self.d.insert_into([file_name,text, 0, 1]) # }}}

        t = self.d.select(where="WHERE last_open=1")[0]
        i = 0
        r.page_lines = 2
        self.loop=True
        while self.loop:
            # nr sentence, content
            nr_sentence, content = int(t[2]+i),t[1].split('.')
            r.read(scr, nr_sentence, content)
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
                #(text_pwd text, content text, nr_sentence real, last_open real)
                old_name = file_name
                r.files = self.d.select(cols='text_pwd')
                file_name = r.select_file_to_read(scr)
                self.d.update_row('last_open', 0, f"WHERE text_pwd='{old_name}'")
# ==============================================================================================}}}
    #def 

if __name__ == '__main__':
    curses.wrapper(Menu)
