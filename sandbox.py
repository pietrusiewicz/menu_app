import curses
import curses.ascii

def main(scr):
    curses.napms(2000)
    #key = scr.getstr().decode('UTF-8')
    key = scr.getch()
    #scr.addstr(repr(key))
    scr.addstr(repr(key))
    curses.endwin()
    print(repr(key))
    print(chr(key))
curses.wrapper(main)
