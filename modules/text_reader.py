import os
import curses
import json

#from config.select_file import Select
#s = curses.wrapper(Select)
#file_name = s.name

class Reader:
    def __init__(self,scr):
        self.config_pwd = os.getcwd()+'/config/config.json'
        self.y = 0
        #self.main(scr)


    def main(self, scr):
        while True:
            self.clear_board(scr)
            scr.addstr(0,0,self.selected_file)
            key = scr.getkey()
            #f = open(self.selected_file)
            if key in ('0'):
                self.select_file_to_read(scr)


    # select file
    def select_file_to_read(self,scr): # {{{
        self.loop = True
        self.get_files()
        while self.loop:
            self.clear_board(scr)

            # display items
            scr.addstr(0, 0, f"Select text file what you want read:") # {{{
            for i in range(len(self.files)):
                scr.addstr(i+1, 0, f"{i+1}) {self.files[i]}")
            if len(self.files) == self.y:
                scr.addstr(self.y+1, 0, f"+)Add text file", curses.A_UNDERLINE)
            else:
                scr.addstr(self.y+1, 0, f"{self.y+1}) {self.files[self.y]}", curses.A_UNDERLINE)
                scr.addstr(len(self.files)+1, 0, f"+) Add text file") # }}}
            self.move_to_select(scr.getkey(), scr) # }}}

    # clear board
    def clear_board(self, scr): #{{{
        h,w = scr.getmaxyx()
        for i in range(h-1):
            scr.addstr(i,0,f"{' ':{w-1}}") # }}}

    # press an arrow
    def move_to_select(self, key,scr): # {{{
        if key == 'KEY_UP' and self.y>0:
            self.y-=1
        if key == 'KEY_DOWN' and self.y<len(self.files):
            self.y+=1 
        #if key == 'KEY_LEFT':
        if key in ('\n', 'KEY_RIGHT'):
            self.loop = False 
            if self.y in range(len(self.files)):
                #self.selected_file = self.files[self.y]
                f = open(self.config_pwd, 'w')
                jsonfile = json.dump({'files': self.files, 'selected':self.selected_file},f)
                #self.selected_file = self.files[self.y]
            else:
                self.clear_board(scr)
                Select(scr)
                self.selected_file = json.load(open(self.config_pwd))['selected']
            # }}}

    # valid the files
    def files_wrong(self): # {{{
        try:
            # check syntax json file
            self.get_files()
            return False
        except:
            # when syntax json is wrong or empty
            return True

    # get self.files and self.selected_file
    def get_files(self):
        jsonfile = json.load(open(self.config_pwd))
        self.files = jsonfile['files']
        self.selected_file = jsonfile['selected']

#curses.wrapper(Reader)
