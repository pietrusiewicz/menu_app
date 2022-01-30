import calendar, curses, datetime
from curses import wrapper

def display_calendar(scr, selyx, kalendarz):
    y,x = scr.getmaxyx()

    inty = [(x//21)*i+x//3 for i in range(1,8)]
    for i, week in enumerate(kalendarz):
        for j, day in enumerate(week):
            color = curses.color_pair(1)
            if day == 0: 
                if i==selyx[0] and j==selyx[1]:
                    color = curses.color_pair(2)
                    scr.addstr(i, inty[j], f"    ", color)
                else:
                    color = curses.color_pair(1)
                    scr.addstr(i, inty[j], f"    ", color)

            elif i==selyx[0] and j==selyx[1]:
                color = curses.color_pair(2)
                scr.addstr(i, inty[j], f"{day:4}", color)
            else:
                scr.addstr(i, inty[j], f"{day:4}", color)


def main(scr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)
    now = datetime.datetime.now()
    year, month, today = now.year, now.month, now.day
    kalendarz = calendar.monthcalendar(year, month)
    ver, hor = 0,0
    todolist = []

    while True:
        for i, item in enumerate(todolist):
            scr.addstr(i+1, 0, repr(item))
        display_calendar(scr, [hor,ver], kalendarz)
        key = scr.getkey()
        scr.addstr(0,0,repr(key))
        week = list(range(7))

        if hor > 0 and key in ('KEY_UP'):
            hor -= 1
        if hor < 5 and key in ('KEY_DOWN'):
            hor += 1
        if ver-1 in week and key in ('KEY_LEFT'):
            ver -= 1
        if ver+1 in week and key in ('KEY_RIGHT'):
            ver += 1

        if key in ('\n'):
            day = f"{str(kalendarz[hor][ver]).zfill(2)}-{str(month).zfill(2)}"
            if int(day[:2]) == 0:
                continue
            scr.addstr(0, 0, "Dodaj item:")
            item, alphabet = "", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~ "
            while True:
                scr.addstr(len(todolist)+1, 0, item)
                key = scr.getkey()
                if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                    item = item[:-1]
                    scr.addstr(len(todolist)+1,len(item), " ")
                    #scr.addstr(len(todolist)+1,len(item), "")
                if key in alphabet:
                    item += key
                if key == '\n':
                    break
            todolist.append((day, item))

wrapper(main)
