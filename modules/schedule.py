import calendar
import curses
import datetime
from curses import wrapper

class Schedule:
    def __init__(self):
        now = datetime.datetime.now()
        year,self.month,self.today = now.year, now.month, now.day
        self.td = ()
        self.kalendarz = calendar.monthcalendar(year, self.month)
        self.day_key = self.get_day_month(self.today)
        self.todolist = {}
        self.ver, self.hor = max([[(j, i) for j,d in enumerate(w) if d==self.today] for i,w in enumerate(self.kalendarz)])[0]
        wrapper(self.main)

    def main(self, scr):
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_YELLOW)

        while True:
            self.display_calendar(scr)
            key = scr.getkey()

            ######### if arrows pressed #########
            self.press_arrow(key)

            ############## <ENTER> ##############
            if key in ('\n'):
                self.input_item(key, scr)
            #scr.addstr(0,0,repr(key))


    # |# ##  | displaying this place
    # |# ##  |
    # |#     |
    # |#     |
    def display_calendar(self, scr):
        y,x = scr.getmaxyx()
        places_x = [(x//21)*i+x//3 for i in range(1,8)]


        for i in range(len(self.kalendarz)):
            for j, day in enumerate(self.kalendarz[i]):
                color = 2 if self.hor==i and self.ver==j else 1
                if day != 0:
                    scr.addstr(i, places_x[j], f"{day:4}", curses.color_pair(color))


        self.day_key = self.get_day_month(self.kalendarz[self.hor][self.ver])
        try:
            self.todolist[self.day_key]
        except:
            self.todolist[self.day_key]=[]


        #l = max([len(item) for item in self.todolist[self.day_key]])
        for i, item in enumerate(self.todolist[self.day_key]):
            scr.addstr(i+1,0,f"{'':{l}}")
            scr.addstr(i+1,0,f"- {item:{l}}")

    
    def press_arrow(self, pressed):
        try:
            if pressed in ('KEY_UP'):
                if self.hor-1 >= 0 and self.kalendarz[self.hor-1][self.ver] > 0:
                    self.hor -= 1
            if pressed in ('KEY_DOWN'):
                if self.hor+1 < 6 and self.kalendarz[self.hor+1][self.ver] > 0:
                    self.hor += 1

            if pressed in ('KEY_LEFT'):
                if self.ver-1 >= 0 and self.kalendarz[self.hor][self.ver-1] > 0: 
                    self.ver -= 1
            if pressed in ('KEY_RIGHT'):
                if self.hor+1 < 7 and self.kalendarz[self.hor][self.ver+1] > 0:
                    self.ver += 1

        except IndexError:
            pass

    def input_item(self, key, scr):
        #if int(self.day_key[:2]) == 0:
            #return False
        scr.addstr(0, 0, "Dodaj item:")
        item, alphabet = "", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789-=0!@#$%^&*()_+[]{};'\\:\"|,./<>?~ "
        try:
            self.day_key = self.get_day_month(self.kalendarz[self.hor][self.ver])
            y=len(self.todolist[self.day_key])+1
        except:
            self.todolist[self.day_key]=[]
            y=1
        while True:
            scr.addstr(y, 0, item)
            key = scr.getkey()
            if key in ("KEY_BACKSPACE", '\b', '\x7f'):
                item = item[:-1]
                scr.addstr(y, len(item), " ")
                #scr.addstr(len(todolist)+1,len(item), "")
            if key in alphabet:
                item += key
            if key == '\n':
                break


        try:
            self.todolist[self.day_key].append(item)
        except:
            self.todolist[self.day_key]=[item]


    def get_day_month(self, d):
        return f"{str(d).zfill(2)}-{str(self.month).zfill(2)}"
Schedule()
