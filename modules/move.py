class Move:
    def __init__(self, block=2):
        self.x, self.y = 0,0
        self.b = block

    def press_key(self, scr):
        k = scr.getkey()
        if k in ['KEY_RIGHT', 'KEY_LEFT', 'KEY_UP', 'KEY_DOWN']:
            if k == 'KEY_UP' and self.b==1:
                self.y -= 1
            if k == 'KEY_DOWN' and self.b==1:
                self.y += 1
            if k == 'KEY_LEFT' and self.b==0:
                self.x -= 1
            if k == 'KEY_RIGHT' and self.b==0:
                self.x += 1
            return False
        else:
            return k
    
    
