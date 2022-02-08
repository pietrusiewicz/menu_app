import curses
import curses.textpad

def main(stdscr):
    win = curses.newwin(5, 60, 5, 10)

    tb = curses.textpad.Textbox(win, insert_mode=True)
    text = tb.edit()
    win.addstr(0, 0, text.encode('utf-8'))
    win.getch()

curses.wrapper(main)
