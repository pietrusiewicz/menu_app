import curses
from curses.textpad import rectangle

def main():
    pad = curses.newpad(100,100)
    for y in range(99):
        for x in range(99):
            pad.addstr(y,x, "kowno")
    scr.getkey()
    
#curses.wrapper(main)
main()
