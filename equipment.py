from settings import *

ITEMS = {"gold": pygame.transform.scale(pygame.image.load("assets/items/gold.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "hp_potion": pygame.transform.scale(pygame.image.load("assets/items/hp_potion.png"),
                                             (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "sword_1": pygame.transform.scale(pygame.image.load("assets/items/sword_1.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "sword_2": pygame.transform.scale(pygame.image.load("assets/items/sword_2.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "sword_3": pygame.transform.scale(pygame.image.load("assets/items/sword_3.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "sword_4": pygame.transform.scale(pygame.image.load("assets/items/sword_4.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "ring_1": pygame.transform.scale(pygame.image.load("assets/items/ring_1.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "ring_2": pygame.transform.scale(pygame.image.load("assets/items/ring_2.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "ring_3": pygame.transform.scale(pygame.image.load("assets/items/ring_3.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         "ring_4": pygame.transform.scale(pygame.image.load("assets/items/ring_4.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
         }


class Equipment:
    def __init__(self, hero_type):
        self.items = [ITEMS["gold"]]
        self.is_visible = False
        self.image = None
        self.capacity = 6
        self.gold = 0
        self.eq_rectangles = []
        self.eq_background_rectangles = []
        for each in range(self.capacity):
            eq_rectangle = pygame.Rect((WIDTH / 2) + self.capacity / 2 * 40 - each * 40,
                                       HEIGHT / 2, ITEMS_WIDTH, ITEMS_HEIGHT)
            eq_background_rectangle = pygame.Rect(WIDTH / 2 + self.capacity / 2 * 40 - each * 40 - 4,
                                                  HEIGHT / 2 - 4, 40, 40)

            self.eq_rectangles.append(eq_rectangle)
            self.eq_background_rectangles.append(eq_background_rectangle)

    def add_item(self):
        pass

    def delete_item(self):
        pass

    def change_visibility(self):
        self.is_visible = not self.is_visible


class Item:
    def __init__(self):
        pass


class Store:
    def __init__(self):
        pass
