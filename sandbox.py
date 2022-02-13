import curses
from curses.textpad import Textbox, rectangle

def main1(scr):
    scr.addstr(0,0, "Enter IM message: (hit c-G to send)")
    
    win = curses.newwin(5,30, 2,1)
    rectangle(scr, 1,0,1+5+1, 1+30+1)
    scr.refresh()

    box = Textbox(win)

    # let the user edit untilc c-G is struck
    box.edit()

    # Get resulting contents
    return box.gather()

def main2(scr):
    scr.addstr(0,0,"ąęćół")
    x,y = 30,5
    win = curses.newwin(y,x, 2,1)
    rectangle(scr, 1,0,1+y+1, 1+x+1)
    scr.refresh()
    box = Textbox(win, True)
    box.edit()
    return box.gather()

def main3(scr):
    word = ""
    while True:
        key = chr(scr.getch())
        if key == '\n':
            break
        else:
            word += key
        scr.addstr(0,0,word)
    return word
kowno = curses.wrapper(main3)
print(kowno)
