import curses
import os
import json

class Select:
    def __init__(self,scr):
        self.y, self.app_running = 0, True
        self.main(scr)
        self.save_file_name()

    def main(self, scr):
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
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

    def clear(self, scr):
        h,w = scr.getmaxyx()
        for y in range(h-1):
            scr.addstr(y,0,f"{' ':{w-1}}")
        self.y = 0
    def save_file_name(self):
        try:
            f = json.load(open('config.json'))['files']
            f.append(self.name)
            json.dump({'files': f}, open('config.json','w'), indent=4, ensure_ascii=False)
        except:
            json.dump({'files':[]}, open('config.json','w'), indent=4, ensure_ascii=False)
            self.save_file_name()



curses.wrapper(Select)
