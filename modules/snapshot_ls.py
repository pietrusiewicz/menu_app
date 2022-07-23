import curses
import os
import json
import time
#from crontab import CronTab


class Snapshot:
    """
    Make a snapshot for selected directories
    1. difference between 1 and 2 file if they exist
    2. saves to json all files and dirs in each directory
    """

    def __init__(self, ls):
        self.tree = {}
        [self.get_tree(d) for d in ls]
        self.path = []
        self.s1,self.s2 = set(), set()
        #self.l1,self.l2 = [], []

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
                fpath = path+'/'+f
                if os.path.isdir(fpath):
                    #d.append( { f: [] } )
                    self.get_tree(fpath)
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
        """
        func gets 2 dicts
        """
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

if __name__ == '__main__':
    ls = json.load(open('config.json', encoding='utf-8'))
    s = Snapshot(['/home'])
    s.save_json()
    diff = s.compare_jsons()
    print(diff)
    diff = s.compare_jsons([-3,-2])
    print(diff)
"""
    #curses.wrapper(Menu)
    s = Snapshot(['/home'])
    s.app()
    #s.save_json()
    #if len(os.listdir('files')) >= 2:
        #d1,d2 = map(lambda x: json.load(open(f"files/{x}", encoding='utf-8')), sorted(os.listdir('files'))[-2:])
        #s.prepare2comparsion(d1, d2)
        #print(s.s1.difference(s.s2))
        #print('='*20)
        #print(s.s2.difference(s.s1))
"""
