import curses
import os
import json

class Menu:
    def __init__(self,scr):
        self.tree = {}


    def get_tree(self, path):
        "returns pwd files as tree for path"
        dirs = path.split('/')#[1:]
        dirs[0] = '/'

        # go to path in self.tree
        d = self.tree
        for key in dirs:
            if key not in list(d):
                if type(d) == dict:
                    d[key] = []
                if type(d) == list:
                    l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                    if key not in l:
                        d.append( {key: []} )
                        d = d[-1]
                    else:
                        l = list(map(lambda x : list(x)[0] if type(x) == dict else x, d))
                        d = d[l.index(key)]
            #d = [i for n, i in enumerate(d) if i not in d[n + 1:]]
            d = d[key]
        #print(self.tree)


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


if __name__ == '__main__':
    #curses.wrapper(Menu)
    m = Menu('a')
    m.get_tree('/etc')
    m.get_tree('/home')
    #print(m.tree)
    print(json.dumps(m.tree, indent=5))
