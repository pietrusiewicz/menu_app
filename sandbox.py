import curses
import os

class Program:
    def __init__(self):
        self.tree = {}

    def main(self, ls=["/home"]):
        for item in ls:
            k = os.listdir(item)
            self.tree[k] = []

if __name__ == '__main__':
    p = Program()
    p.main()
