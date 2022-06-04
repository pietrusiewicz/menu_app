import curses

class Menu:
    def __init__(self,scr):
        self.config_pwd = os.getcwd()+'/config/config.json'
        self.y = 0
        self.check_files(scr)
        self.main(scr)


    def main(self, scr):
        while True:
            self.clear_board(scr)
            scr.addstr(0,0,self.selected_file)
            key = scr.getkey()
            #f = open(self.selected_file)
            if key in ('0'):
                self.select_file_to_read(scr)


curses.wrapper(Menu)
