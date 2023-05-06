from settings import *

ITEMS_IMAGES = {"gold": pygame.transform.scale(pygame.image.load("assets/items/gold.png"), (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "hp_potion": pygame.transform.scale(pygame.image.load("assets/items/hp_potion.png"),
                                                    (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "sword_1": pygame.transform.scale(pygame.image.load("assets/items/sword_1.png"),
                                                  (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "sword_2": pygame.transform.scale(pygame.image.load("assets/items/sword_2.png"),
                                                  (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "sword_3": pygame.transform.scale(pygame.image.load("assets/items/sword_3.png"),
                                                  (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "sword_4": pygame.transform.scale(pygame.image.load("assets/items/sword_4.png"),
                                                  (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "ring_1": pygame.transform.scale(pygame.image.load("assets/items/ring_1.png"),
                                                 (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "ring_2": pygame.transform.scale(pygame.image.load("assets/items/ring_2.png"),
                                                 (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "ring_3": pygame.transform.scale(pygame.image.load("assets/items/ring_3.png"),
                                                 (ITEMS_WIDTH, ITEMS_HEIGHT)),
                "ring_4": pygame.transform.scale(pygame.image.load("assets/items/ring_4.png"),
                                                 (ITEMS_WIDTH, ITEMS_HEIGHT)),
                }


class Equipment:
    def __init__(self, hero_type):
        self.items = []
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
        self.add_item(items["gold"])

    def add_item(self, item):
        if len(self.items) == self.capacity:
            pass
        elif self.check_if_in_eq_and_stackable(item.name):
            for each in self.items:
                if each.name == item.name and item.stackable:
                    each.amount += 1
                    each.update_amount_text()
        else:
            self.items.append(item)

    def add_gold(self, value):
        for i in range(value):
            self.add_item(items["gold"])

    def delete_item(self):
        pass

    def check_if_in_eq_and_stackable(self, name):
        for each in self.items:
            if each.name == name and each.stackable:
                return True
        return False

    def change_visibility(self):
        self.is_visible = not self.is_visible

    def draw(self):
        for each in self.eq_background_rectangles:
            pygame.draw.rect(WIN, BLACK, each)
        for each in self.eq_rectangles:
            pygame.draw.rect(WIN, BROWN, each)
        for each in self.items:
            item_position = self.eq_rectangles[self.capacity - self.items.index(each) - 1].topleft
            WIN.blit(each.item_image, item_position)
            if each.stackable:
                text_pos_x = item_position[0] + each.item_image.get_rect().width - each.amount_text.get_width()
                text_pos_y = item_position[1] + each.item_image.get_rect().height - each.amount_text.get_height()
                WIN.blit(each.amount_text, (text_pos_x, text_pos_y))


class Item:
    def __init__(self, name, sellable=True, usable=True, stackable=True):
        self.name = name
        self.item_image = ITEMS_IMAGES[name]
        self.sellable = sellable
        self.usable = usable
        self.stackable = stackable
        self.amount = 1
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))

    def update_amount_text(self):
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))


class Store:
    def __init__(self):
        self.is_visible = False


items = {
    "gold": Item("gold", False, False, True),
    "hp_potion": Item("hp_potion", True, True, True),
    "sword_1": Item("sword_1", True, True, False),
    "sword_2": Item("sword_2", True, True, False),
    "sword_3": Item("sword_3", True, True, False),
    "sword_4": Item("sword_4", True, True, False),
    "ring_1": Item("ring_1", True, True, False),
    "ring_2": Item("ring_2", True, True, False),
    "ring_3": Item("ring_3", True, True, False),
    "ring_4": Item("ring_4", True, True, False),
}
