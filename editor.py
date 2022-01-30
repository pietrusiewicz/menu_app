import curses

scr = curses.initscr()
y = 0
l,word = [], ''

for i,j in enumerate(range(10)):
    scr.addstr(i, 0, str(i))
scr.refresh()
curses.napms(3000)
curses.endwin()
