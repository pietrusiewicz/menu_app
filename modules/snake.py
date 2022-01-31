from curses import wrapper
import curses

class Snake:
    def __init__(self, scr):
        self.xy = [0, 0]
        self.direction = 'RIGHT'
        while True:
            scr.addstr("press any key to start")
            scr.getkey()
            break
        self.main(scr)

    def main(self, scr):
        while True:
            h,w = scr.getmaxyx()
            key = scr.getkey()
            if key == 'KEY_UP':
                if self.xy[1]-1 < 0:
                    self.xy[1] = h-1
                else:
                    self.xy[1] -= 1
            if key == 'KEY_DOWN':
                if self.xy[1]+1 >= h-1:
                    self.xy[1] = 0
                self.xy[1] += 1
            if key == 'KEY_RIGHT':
                if self.xy[0]+1 >= w-1:
                    self.xy[0] = 0
                self.xy[0] += 1
            if key == 'KEY_LEFT':
                if self.xy[0]-1 <0:
                    self.xy[0] = w-1
                self.xy[0] -= 1
            
            scr.addstr(self.xy[1], self.xy[0], ' ')


            


wrapper(Snake)
