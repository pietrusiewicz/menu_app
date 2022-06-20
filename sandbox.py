import curses
import os
import json

class Menu:
    def __init__(self,scr):
        self.tree = {}
        self.get_tree('/etc')


    def get_tree(self, path):
        "returns pwd files as tree for path"
        dirs = path.split('/')#[1:]
        dirs[0] = '/'

        # go to path in self.tree
        d = self.tree
        for key in dirs:
            if type(d) == dict:
                d[key] = []
            if type(d) == list:
                if key not in d:
                    d.append( {key: []} )
                l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                d = d[l.index(key)]

            d = d[key]
                #l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))

        for f in os.listdir(path):
            if os.path.isdir(path+f):
                d.append( { f: [] } )
            else:
                d.append( f )


#curses.wrapper(Menu)
m = Menu('a')
#print(m.tree)
print(json.dumps(m.tree, indent=5))
