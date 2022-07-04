from modules import move
import curses

class Program(move.Move):

    def colors(self):
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)

    def main(self, scr):
        self.colors()

        menu_str = "/0) start      /1) todolist   /2) snake      /3) snapshot_ls"
        scr.addstr(0,0,menu_str, curses.color_pair(1))

        if self.y == 0:
            start_index = menu_str.find(str(self.x))-1
            end_index = menu_str.find(str(self.x+1))-2
            scr.addstr(0, start_index, menu_str[start_index:end_index], curses.color_pair(2))

        #self.display_tiles(scr)
        self.press_key(scr, cnds=[self.y>0,self.y<2, self.x>0,self.x<3])
        if self.y > 0:
            beg = self.x
            self.tiles_for_app(scr)
            self.x = beg
        self.main(scr)

    def tiles_for_app(self, scr):
        self.x = 0 
        self.display_tiles(scr, ['arsen'])

if __name__ == '__main__':
    p = Program()
    curses.wrapper(p.main)
