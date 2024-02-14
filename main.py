import curses
import time
import sys
import json
import os


from modules.snake import Snake
from modules.snapshot_ls import Snapshot
from modules.todolist import Todolist
from modules.move import Move
from modules.explorer import Explorer
from modules.primary import Wydajnosc

#from sandbox import Explorer


class Menu(Move):

  def __init__(self):
    Move.__init__(self)
    """
        load_t1-t4 is created for todolist contained under 48 line
        """
    load_t1_t4 = Todolist().load_tasks()
    self.t1, self.t2, self.t3, self.t4 = load_t1_t4

  def display_list(self, lines, n):
    for i, line in enumerate(list(lines)):
      self.wins[n].addstr(i, 0, line)
    self.wins[n].refresh()
    self.wins[n].getkey()

  # menu what displayes menu
  def main(self, scr):
    """
        first level in app
        """

    self.load_colors()
    # content
    #s = Snapshot(self.c['snapshot_ls'])
    self.content = {
        "start": [{"start1"}, {'start2'}, {'start3'}, {'wydajnosc': lambda: Wydajnosc(scr)}],
        "todolist": [
            {
                f"{list(self.t1)}": lambda: self.clicked_tile(scr, 0)
            },
            {
                f"{list(self.t2)}": lambda: self.clicked_tile(scr, 1)
            },
            {
                f"{list(self.t3)}": lambda: self.clicked_tile(scr, 2)
            },
            {
                f"{list(self.t4)}": lambda: self.clicked_tile(scr, 3)
            },
        ],
        "snake": [{
            "launch snake":
            lambda: print("maintenance break")
            #lambda: [s := Snake(Move()), s.main(scr)]
        }, 
        {}, {}, {}],
        "explorer": [
          {
            "enter explorer": lambda: [e:=Explorer(), e.start(scr)]
          }, {
            f"{time.strftime('%D %H:%M:%S')}": lambda:time.strftime("%D")
          }, 
          {}, {}

          #{"vim-like editor": lambda: explorer.editor},
          #{"sprawdz wydajnosc pc": lambda: liczby_pierwsze()},
        ]
    }

    while True:
      try:
        
        self.display_menu(scr)

        # conditions for move arrows
        l = [
            self.y > 0, self.y < 2, self.x > 0, self.x < len(self.content) - 1
        ]
        self.key = self.press_key(
            scr,
            l,
            enter=lambda: list(self.content[self.category][self.y + self.x].
                               values())[0]())
        self.display_menu(scr)
        #if self.key:
        #  self.pressed_a_key(scr)
      except KeyboardInterrupt:
        break

  # display menu
  def display_menu(self, scr):
    """
        first level in app
        main -> tiles_menu
        """
    # refresh screen
    self.clear_board(scr)

    # display topbar
    self.topbar(scr)

    # mark hovering tile
    if self.y > 0:
      self.tiles_menu(scr)
      self.display_menu(scr)

  # action in tiles menu
  def tiles_menu(self, scr):
    """
        second level in app
        display_menu -> tiles_menu
        """
    beg = self.x
    self.x = 0
    while True:

      self.display_tiles(
          scr,
          t1=self.content[self.category][0],
          t2=self.content[self.category][1],
          t3=self.content[self.category][2],
          t4=self.content[self.category][3],
      )

      key = self.press_key(
          scr,
          cnds=[self.y > 0, self.y < 2, self.x > 0, self.x < 1],
          enter=lambda: list(self.content[self.category][2 * (
              self.y - 1) + self.x].values())[0]() )
      
      if self.y == 0:
        break
      """
            if type(key)!= bool and ord(key) == 10:
                d = self.content[self.category][2*(self.y-1) + self.x]
                if type(d) == dict:
                    app = list(d.values())[0]
                    app()
                    
                    #d = ditem
                    #for value in d.values():
                    #    value()
            """

    self.x = beg

  # enter tile
  def clicked_tile(self, scr, n):
    """
        third level in app
        display_menu -> tiles_menu -> clicked_tile
        """
    win = self.wins[n]
    d = eval(f"self.t{n+1}")
    # execute app in tile
    d = self.tile_app(scr, win, d=d)

  # press a key not arrow
  #def pressed_a_key(self, scr):
    # ESC key
   # if ord(self.key) == 27:
    #  sys.exit()

    # ENTER key
    #elif self.key == "KEY_ENTER":
    #elif ord(self.key) == 10:
     # pass  #list(self.content[self.category][self.y + self.x].values())[0]()
      # launching app in tile
      #app_name = self.content[self.category][self.y + self.x]
      # launch from self.content
      #if type(app_name) == dict:
      #   d = app_name
      #  for value in d.values():
      #     value()
  """
            scr.getkey()
            scr.getkey()
            scr.getkey()
            scr.getkey()
  """

  def get_config(self):
    if 'config.json' not in os.listdir():
      d = {
          'snapshot_ls': ['/home'],
          'snake': [],
          'todolist': [],
      }
      json.dump(d, open('config.json', 'w', encoding='utf-8'))
    self.c = json.load(open('config.json', encoding='utf-8'))

  def load_colors(self):
    """
    loading colors
    """
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_GREEN)

  def topbar(self, scr):
    menu_str = "/0) start      /1) todolist   /2) snake      /3) explorer"
    scr.addstr(0, 0, menu_str, curses.color_pair(1))

    # mark selected option in topbar
    if self.y == 0:
      start_index = menu_str.find(str(self.x)) - 1
      end_index = menu_str.find(str(self.x + 1)) - 2
      scr.addstr(0, start_index, menu_str[start_index:end_index],
                 curses.color_pair(2))

      #key = list(self.content)[self.x]
      self.category = list(self.content)[self.x]

      self.display_tiles(
          scr,
          t1=self.content[self.category][0],
          t2=self.content[self.category][1],
          t3=self.content[self.category][2],
          t4=self.content[self.category][3],
      )


if __name__ == '__main__':
  m = Menu()
  m.get_config()
  curses.wrapper(m.main)
  #m.main()
