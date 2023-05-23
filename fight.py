import random
from settings import *


class Fight:
    def __init__(self, player, enemy):
        self.is_fighting = True
        self.first_strike = random.randint(1, 2)

    def draw(self):
        pass

    def handle_event(self):
        pass

    def main_loop(self):
        while self.is_fighting:
            self.draw()
