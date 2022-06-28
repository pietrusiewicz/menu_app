import curses
import os
import json
import time


class Snapshot:
    "it does snapshot for selected directories"

    def __init__(self,scr, ls=['/home']):
        self.tree = {}
        [self.get_tree(d) for d in ls]
        self.path = []
        self.s1,self.s2 = set(), set()
        #self.l1,self.l2 = [], []

    # tree about selected path
    def get_tree(self, path): # {{{
        "It does tree of selected directories"

        # list of directories for path
        dirs = path.split('/')#[1:]
        dirs[0] = '/'

        # go to path in self.tree
        d = self.tree

        # make json' tree through dirs (17 line)
        for key in dirs: # {{{
            # if path doesn't exist
            if key not in list(d):
                # is it new?
                if type(d) == dict:
                    d[key] = []

                # is it exists?
                if type(d) == list: # {{{
                    l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                    if key not in l:
                        d.append( {key: []} )
                        d = d[-1]
                    else:
                        l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                        d = d[l.index(key)] # }}}

            # go to the next dir
            d = d[key] # }}}


        # creating list in dict (directory) or string (file)
        for f in os.listdir(path): # {{{
            try:
                if os.path.isdir(path+'/'+f):
                    #d.append( { f: [] } )
                    self.get_tree(path+'/'+f)
                else:
                    d.append( f )
                    #print(path+'/'+f)
            except PermissionError:
                continue # }}}
    # }}}

    def print_json(self):
        return json.dumps(self.tree, indent=5)

    def save_json(self): # {{{
        if 'files' not in os.listdir():
            os.mkdir('files') 
        name = time.strftime("%Y%m%d%H%M%S")
        f = open(f'files/{name}.json', 'w')
        json.dump(self.tree, f, indent=5) # }}}
        #f.save()

    # prepairing to compare
    def prepare2comparsion(self, d1, d2): # {{{
        """
        func gets 2 dicts
        """
        self.convert_dict2list(d1, 1)
        self.convert_dict2list(d2, 2) # }}}

    # converts to list
    def convert_dict2list(self, d, n): # {{{
        s = self.s1 if n == 1 else self.s2
        for key in d:
            self.path.append(key)
            for i in range(len(d[key])):
                if type(d[key][i]) == dict:
                    self.convert_dict2list(d[key][i], n)
                    s.add(f"/{'/'.join(self.path[1:])}")
                else:
                    s.add(f"/{'/'.join(self.path[1:])}/{d[key][i]}")
            self.path = self.path[:-1] # }}}

if __name__ == '__main__':
    #curses.wrapper(Menu)
    s = Snapshot('a', ['/home'])
    s.save_json()
    if len(os.listdir('files')) >= 2:
        d1,d2 = map(lambda x: json.load(open(f"files/{x}", encoding='utf-8')), sorted(os.listdir('files'))[-2:])
        s.prepare2comparsion(d1, d2)
        print(s.s1.difference(s.s2))
        print('='*20)
        print(s.s2.difference(s.s1))

