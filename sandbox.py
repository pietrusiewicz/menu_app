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
        for line in dirs:
            if type(d) == list:
                if line not in d:
                    d.append( {line:[]} )
                l = list(map(lambda x: list(x.keys())[0] if type(x)==dict else x, d)) 
                i = l.index(line)
                print(i)
                d = d[i]
            elif line not in self.tree.keys():
                d[line] = []
                d = d[line]
            else:
                d = d[line]

        for f in os.listdir(path):
            if os.path.isdir(path+f):
                d.append( { f:[] } )
            else:
                d.append( f )


#curses.wrapper(Menu)
m = Menu('a')
#print(m.tree)
print(json.dumps(m.tree, indent=5))
