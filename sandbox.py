from curses import wrapper
import curses
import os
import json
import time
from modules.move import Move


#from crontab import CronTab


class Explorer(Move):
    """
    Simple explorer-like app
    On left side: list in pwd directories
    On right side: list in pwd files
    """

    def __init__(self):
      """
      File Explorer applicatoin
      """
      self.path = os.getcwd().split("/")[1:]
        #self.s1,self.s2 = set(), set()
        #self.l1,self.l2 = [], []
    
    def start(self, scr):
      
        self.get_colors()
        scr.clear()
        h,w = scr.getmaxyx()

        Lwin,Rwin = curses.newwin(h, w//2, 0, 0), curses.newwin(h, w//2, 0, w//2)
        
        Lwin.refresh()
        scr.getkey()
        #print(self.path)
        self.x,self.y,Lside=0,0,True
      
        while True:
          dirs,files=[],[]
          for df in os.listdir():
            if os.path.isdir(df): dirs.append(df)
            if os.path.isfile(df): files.append(df)
          dirs.insert(0,"..")
          # display dir list in tile

          
          self.fill_color(Lwin, 2+Lside*2)
          self.fill_color(Rwin, 4-Lside*2)
          scr.refresh()
          
          # display file list in tile
          for i, line in enumerate(dirs):
            Lwin.addstr(i, 0, f"{line}", curses.color_pair(4-Lside*2))
            if self.y == i:
              isunder = curses.color_pair(2+Lside*2) 
              if Lside:
                isunder += curses.A_UNDERLINE
              Lwin.addstr(i, 0, f"{line}", isunder)
          Lwin.refresh()

          # display file list in tile
          for i, line in enumerate(files):
            Rwin.addstr(i, 0, f"{line}", curses.color_pair(4-Lside*2))
            if self.x == i:
              isunder = curses.color_pair(2+Lside*2) 
              if not Lside:
                isunder += curses.A_UNDERLINE
              Rwin.addstr(i, 0, f"{line}", isunder)
          Rwin.refresh()

          # press a key
          dx,dy=self.x,self.y
          k=self.press_key(scr, [self.y>0, self.y<len(dirs)-1, self.x>0,self.x<len(files)-1])
          dx-=self.x; dy-=self.y
          # 0 is meaning nothing changed
          if dx!=dy:
            if dx!=0: Lside = False
            if dy!=0: Lside = True
            
          # arrow - move
          if not k:
            continue
            
          # other keys
          else:
            # delete item
            if k in ("KEY_BACKSPACE", '\b', '\x7f'):
              pass

            # esc key
            elif ord(k) == 27:
              break

            # click in line ENTER
            elif ord(k) == 10:
              if Lside:
                os.chdir(dirs[self.y])
                Lwin.clear()
                Rwin.clear()
                self.x,self.y=0,0
                #print(os.listdir())
              continue
              
          Lwin.refresh()
          Rwin.refresh()
          #scr.getkey()

    def get_colors(self):
      curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
      curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
      curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
      curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
      curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
      curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)
    
    def fill_color(self, win, n):
      win.bkgd(' ', curses.color_pair(n))
      win.refresh()
    
    
if __name__ == '__main__':
    e = Explorer()
    wrapper(e.start)
