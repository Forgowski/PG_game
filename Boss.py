from enemy import *


class Boss(Enemy):
    def __init__(self):
        super().__init__(0)
        self.stats = Stats(1000, 50, 30, 50)
        self.hp = 100
        self.exp_drop = 300
        self.gold_drop = 50

    def level_up(self):
        self.lvl += 1
        self.stats.max_hp *= 2
        self.hp *= 2
        self.stats.attack_power *= 2
        self.exp_drop *= 3
        self.gold_drop *= 3
