import curses
import os
import json

class Menu:
    def __init__(self,scr):
        self.tree = { '/':[] }
        self.get_tree('/')


    def get_tree(self, path):
        ""
        #self.tree[pwd] = []
        # enter to inheritance dict
        d = self.tree['/']

        # directories in path
        dirs = path.split('/')
        #lines = list(filter(str, dirs[:-1]))
        #print(dirs)
        #for line in lines:
            #print(line)
        #    d = d[line]

        #d = self.tree[pwd]

        # files in path
        for line in os.listdir(path):
            try:
                if os.path.isdir(path+line):
                    d.append({ line:[] })
                    #self.get_tree(path+line)
                else:
                    #print(d)
                    d.append(line)
            except PermissionError:
                continue


#curses.wrapper(Menu)
m = Menu('a')
#print(m.tree)
print(json.dumps(m.tree, indent=5))
