import curses

def main(scr):
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    #curses.start_color()
    statusbar = (curses.A_UNDERLINE | curses.color_pair(1))
    scr.addstr('kowno', statusbar)
    scr.getkey()

curses.wrapper(main)
