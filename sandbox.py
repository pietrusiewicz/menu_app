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
        File Explorer application
        """
        self.path = os.getcwd().split("/")[1:]
        
        #self.s1,self.s2 = set(), set()
        #self.l1,self.l2 = [], []
    
    def start(self, scr):
        """
        Starts the application
        """
        self.get_colors()
        
        h,w = scr.getmaxyx()
        self.Lwin,self.Rwin = curses.newwin(h, w//2, 0, 0), curses.newwin(h, w//2, 0, w//2)
        scr.clear()
        self.x,self.y, Lside=0,0, True

        self.w = True
        while self.w:
          self.dirs,files=[],[]
          for df in os.listdir():
            if os.path.isdir(df): self.dirs.append(df)
            if os.path.isfile(df): files.append(df)
          self.dirs.insert(0,"..")
          
          
          # prepare windows for dirs/files
          self.fill_color(self.Lwin, 2+Lside*2)
          self.fill_color(self.Rwin, 4-Lside*2)
          scr.refresh()

          
          # display dir list in tile
          for i, line in enumerate(self.dirs):
            self.Lwin.addstr(i, 0, f"{line}", curses.color_pair(4-Lside*2))
            if self.y == i:
              isunder = curses.color_pair(2+Lside*2) 
              if Lside:
                isunder += curses.A_UNDERLINE
              self.Lwin.addstr(i, 0, f"{line}", isunder)
          self.Lwin.refresh()

          
          # display file list in tile
          for i, line in enumerate(files):
            self.Rwin.addstr(i, 0, f"{line}", curses.color_pair(4-Lside*2))
            if self.x == i:
              isunder = curses.color_pair(2+Lside*2) 
              if not Lside:
                isunder += curses.A_UNDERLINE
              self.Rwin.addstr(i, 0, f"{line}", isunder)
          self.Rwin.refresh()

          # press a key
          dx,dy=self.x,self.y
          self.Lwin.refresh()
          self.Rwin.refresh()
          k=self.press_key(scr, 
                           cnds=[self.y>0 or len(self.dirs)==1,
                                 self.y<len(self.dirs)-1 or len(self.dirs)==1,
                                 self.x>0,
                                 self.x<len(files)-1],
                           enter=lambda: self.enter_dir() if Lside else 0,
                           escape=lambda: self.exit_dir()
                          )
          
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

    def enter_dir(self):
      if len(self.dirs) == 1:
        os.chdir('..')
      else:
        os.chdir(self.dirs[self.y])
      self.Lwin.clear()
      self.Rwin.clear()
      self.x,self.y = 0,0

    def exit_dir(self):
      self.w = False
      
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
