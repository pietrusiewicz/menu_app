import curses

class Wydajnosc:
  def __init__(self, scr):
    self.main(scr)

  def is_prime(self, n):
    if n <= 1:
      return False
    for i in range(2, int(n**0.5) + 1):
      if n % i == 0:
        return False
    return True
  
  def main(self, scr):
    import time
    
    h,w = scr.getmaxyx()
    x,y = 0,0
    win = curses.newwin(h-4,w-6, 2,3)
  
    n,strona = 1,0
    t = time.time()
    while n:
      try:
        if self.is_prime(n):
          #print
          x += len(f"{n},")
          if x >= w-6:
            x = 0
            y+=1
            win.addstr(h-5,0, f"'{strona}. strona, n={n}, {round(time.time()-t,3)}s")
            t = time.time()
            
          if y >= h-5:
            y = 0
            strona+=1
          win.addstr(y,x, f"{n}/")
          win.refresh()
          
        n+=1
      except KeyboardInterrupt:
        print(f"n={n}")
        break
    print(f"n={n}")
if __name__ == '__main__':
  curses.wrapper(Wydajnosc)
