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

        Lwin = curses.newwin(h, w//2, 0, 0)
        Rwin = curses.newwin(h, w//2, 0, w//2)
        
        Lwin.refresh()
        scr.getkey()
        #print(self.path)
        self.x,self.y=0,0
        while True:
          dirs,files=[],[]
          for df in os.listdir():
            if os.path.isdir(df): dirs.append(df)
            if os.path.isfile(df): files.append(df)
          # display dir list in tile
          scr.refresh()
          self.fill_color(Lwin, 2)
          
          for i, line in enumerate(dirs):
            Lwin.addstr(i, 0, f"{line}", curses.color_pair(2))
            if self.y == i:
              Lwin.addstr(i, 0, f"{line}", curses.color_pair(4) + curses.A_UNDERLINE)
              #Lwin.addstr(len(dirs), 0, f'{"+":{w}}', curses.color_pair(4 if len(dirs) == dy else 2))
          Lwin.refresh()

          for i, line in enumerate(files):
            Rwin.addstr(i, 0, f"{line}", curses.color_pair(4))
            if self.x == i:
              Rwin.addstr(i, 0, f"{line}", curses.color_pair(2) + curses.A_UNDERLINE)
              #Lwin.addstr(len(dirs), 0, f'{"+":{w}}', curses.color_pair(4 if len(dirs) == dy else 2))
          Rwin.refresh()

          # press a key
          k=self.press_key(scr, [self.y>0, self.y<len(dirs)-1, self.x>0,self.x<len(files)-1])

          # arrow - move
          if not k:
            continue
          # other keys
          else:
            # delete item
            if k in ("KEY_BACKSPACE", '\b', '\x7f'):
              pass

            # esc key
            elif k==str and ord(k) == 27:
              break

            # click in line ENTER
            elif k==str and ord(k) == 10:
              pass
            """
            if self.y < len(d):
              d[list(d)[self.y]] = not d[list(d)[self.y]]
            else:
              key = self.edit_line(win, k)
              d[key] = False
            """
          
          #TODO
          # display lists of dirs and files
          for i,d in enumerate(dirs):
            Lwin.addstr(i,0,d)
          for i,f in enumerate(files):
            Rwin.addstr(i,0,f)
          #Lwin.addstr(0,0, dirsfiles[0][1])
          #Rwin.addstr(0,0, dirsfiles[3][1])
          Lwin.refresh()
          Rwin.refresh()
          scr.getkey()

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
    
    """
    # tree about selected path
    def get_tree(self, path):
        "It does tree of selected directories"

        # list of directories for path
        dirs = path.split('/')#[1:]
        dirs[0] = '/'

        # set branch as self.tree
        d = self.tree

        # make json' tree through dirs (23 line)
        for key in dirs:
            # if path doesn't exist
            if key not in list(d):
                # is it new?
                if type(d) == dict:
                    d[key] = []

                # is it exists?
                if type(d) == list:
                    l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                    if key not in l:
                        d.append( {key: []} )
                        d = d[-1]
                    else:
                        l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                        d = d[l.index(key)]

            # go to the next dir
            d = d[key]


        # creating list in dict (directory) or string (file)
        for f in os.listdir(path):
            try:
                if os.path.isdir(path+'/'+f):
                    #d.append( { f: [] } )
                    self.get_tree(path+'/'+f)
                else:
                    d.append( f )
                    #print(path+'/'+f)
            except PermissionError:
                continue


    def print_json(self):
        return json.dumps(self.tree, indent=5)

    def save_json(self):
        if 'files' not in os.listdir():
            os.mkdir('files') 
        name = time.strftime("%Y%m%d%H%M%S")
        f = open(f'files/{name}.json', 'w')
        json.dump(self.tree, f, indent=5)
        #f.save()
    # prepairing to compare
    #def prepare2comparsion(self, d1, d2):
        "
        func gets 2 dicts
        ""
        #self.convert_dict2list(d1, 1)
        #self.convert_dict2list(d2, 2)

    # converts to set
    def convert_dict2set(self, d, n):
        s = self.s1 if n == 1 else self.s2
        for key in d:
            self.path.append(key)
            for i in range(len(d[key])):
                if type(d[key][i]) == dict:
                    self.convert_dict2set(d[key][i], n)
                    s.add(f"/{'/'.join(self.path[1:])}")
                else:
                    s.add(f"/{'/'.join(self.path[1:])}/{d[key][i]}")
            self.path = self.path[:-1]

    def config_app(self,scr):
        "edit app"
        username = os.getenv('USER')
        for i, dr in enumerate([_ for _ in map(lambda x: f"/{x}" if os.path.isdir(f'/{x}') else None, os.listdir('/')) if _ !=None]):
            scr.addstr(i,0, f"{dr}")

    def compare_jsons(self, indexes=[-2, -1]):
        self.s1=set()
        self.s2=set()

        if len(os.listdir('files')) >= 2:
            d1,d2 = list(map(lambda x: json.load(open(f"files/{x}", encoding='utf-8')), [sorted(os.listdir('files'))[i] for i in indexes]))
            self.convert_dict2set(d1, 1)
            self.convert_dict2set(d2, 2)
            #print(self.s1.difference(self.s2))
            diff = self.s2.difference(self.s1)
            return diff
      """
if __name__ == '__main__':
    e = Explorer()
    wrapper(e.start)
