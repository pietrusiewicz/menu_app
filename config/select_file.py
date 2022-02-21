import curses
import os,sys
import json

class Select:
    def __init__(self,scr):
        self.config_pwd = f"{os.getcwd()}/config/config.json"
        self.y, self.app_running = 0, True
        self.main(scr)

    def main(self, scr):
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
        #self.pwd = os.chdir(self.start_pwd)
        # 
        while self.app_running:
            self.pwd = os.getcwd()
            scr.addstr(0,0, self.pwd)
            self.files = os.listdir()
            # when directory is empty 
            if len(self.files) == 0: #{{{
                os.chdir('..')
                self.clear(scr)
                continue # }}}

            # displays content of directory
            for i in range(len(self.files)): # {{{
                f = self.files[i]
                # check valid directory
                color = curses.color_pair(1) if os.path.isdir(f) else curses.color_pair(2)
                scr.addstr(i+1,0, f, color)

            styl = (curses.A_UNDERLINE | curses.color_pair(1)) if os.path.isdir(self.files[self.y]) else curses.A_UNDERLINE
            scr.addstr(self.y+1,0, self.files[self.y], styl) # }}}
            key = scr.getkey()
            self.press_an_arrow(scr, key)
        self.save_file_name()

    # press an arrow
    def press_an_arrow(self, scr, key): # {{{
        if key == 'KEY_DOWN' and self.y+1<len(self.files):
            self.y+=1
        if key == 'KEY_UP' and self.y>0:
            self.y-=1
        if key == 'KEY_LEFT':
            os.chdir('..')
            self.clear(scr)
        if key == 'KEY_RIGHT':
            f = self.files[self.y]
            if os.path.isdir(f):
                os.chdir(f)
            else:
                confirm =f"Are you sure to read {repr(f)}?"
                scr.addstr(len(self.files)+1,0, confirm)
                if scr.getkey() in 'Yy':
                    self.name = f"{self.pwd}/{f}"
                    self.app_running = False
                else:
                    scr.addstr(len(self.files)+1,0, f"{' ':{len(confirm)}}")
            self.clear(scr) # }}}

    # clears board
    def clear(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            scr.addstr(y,0,f"{' ':{w-1}}")
        self.y = 0

    # after select
    def save_file_name(self):
        # operation in json file
        try: # {{{
            jsonfile = json.load(open(self.config_pwd))['files']
            jsonfile.append(self.name)
        except:
            jsonfile = [self.name] #}}}
        f = open(self.config_pwd,'w')
        json.dump({'files': jsonfile, 'selected': self.name}, f, indent=4, ensure_ascii=False)

    """
    def add_text_to_db():
        # add to sqlite db
        try:
            conn = sqlite3.connect('texts.db')
            cur = conn.cursor()
            max_val = len(cur.execute("SELECT DISTINCT id FROM sentences"))
            f = open('text.txt').readlines()
            text_file = ' '.join([line.replace('\n','').replace("'",'"') for line in f])
            cur.execute(f"INSERT INTO texts
                    VALUES ('{self.name}', '{text_file}')")
        except:
            conn = sqlite3.connect('texts.db')
            cur = conn.cursor()
            cur.execute("CREATE TABLE texts
                    (text_pwd text, content text)")
            self.add_text_to_db()
    """
#curses.wrapper(Select)
