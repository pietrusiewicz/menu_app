import os
import curses
import math

class Reader:
    def __init__(self):
        self.config_pwd = os.getcwd()+'/config/config.json'
        self.y = 0
        #self.main(scr)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # read the text
    def read(self, scr, nr_sentence): # {{{
        w = scr.getmaxyx()[1]
        sw = (w//9)*2
        text=f"{nr_sentence}) {self.content[nr_sentence]}"
        if len(text) < w:
            scr.addstr(0,sw, f"{text:{w-sw}}", curses.color_pair(1))

        else:
            diff = math.ceil(len(text)/w)
            #text = text[]
            for i in range(diff):
                # start string index
                t = i*w
                text_var = text[t:t+w] if t+w < len(text) else text[t:-1]
                scr.addstr(i,sw, f"{text[t:t+w]:{w-sw}}", curses.color_pair(1))


        # }}}

    # select file
    def select_file_to_read(self, scr): # {{{
        self.loop = True
        self.get_files()
        while self.loop:
            self.clear_board(scr)

            # displays items
# ============================================================================================= {{{

            scr.addstr(0, 0, f"Select text file what you want to read:")
            for i in range(len(self.files)):
                scr.addstr(i+1, 0, f"{i+1}) {self.files[i]}")
            if len(self.files) == self.y:
                scr.addstr(self.y+1, 0, f"+)Add text file", curses.A_UNDERLINE)
            else:
                scr.addstr(self.y+1, 0, f"{self.y+1}) {self.files[self.y]}", curses.A_UNDERLINE)
                scr.addstr(len(self.files)+1, 0, f"+) Add text file")
                scr.addstr(len(self.files)+2, 0, f"[d]elete item")

# ============================================================================================= }}}
            self.press_a_key(scr.getkey(), scr) # }}}
        return self.selected_file

    # clear board
    def clear_board(self, scr): #{{{
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}") # }}}

    # press a key
    def press_a_key(self, key,scr): # {{{
        if key == 'KEY_UP' and self.y>0:
            self.y-=1
        if key == 'KEY_DOWN' and self.y<len(self.files):
            self.y+=1 
        # select file
        if key in ('\n', 'KEY_RIGHT'):
            self.loop = False 
            if self.y in range(len(self.files)):
                self.selected_file = self.files[self.y]
            else:
                self.clear_board(scr)
                s = Select(scr)
                # when add
                self.selected_file = s.get_filename(scr)
        if self.y in range(len(self.files)):
            if key in 'd':
                del self.files[self.y] # }}}

    # get content from text file
    def get_text(self, name): # {{{
        text = ' '.join([line.replace('\n','').replace('\'','"') for line in open(name).readlines()])
        return text
        # }}}

#curses.wrapper(Reader)
