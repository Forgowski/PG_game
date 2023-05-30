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
                "level_up": pygame.image.load("assets/items/level_up.png"),
                }


def create_item(name):
    item = Item(*items[name])
    return item


class Equipment:
    def __init__(self):
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

    def add_item(self, item):
        if len(self.items) == self.capacity:
            return 0

        elif item.stackable and any(each.name == item.name for each in self.items):
            for each in self.items:
                if each.name == item.name:
                    each.amount += 1
                    self.subtract_gold(item.price)
                    return 1
        else:
            self.items.append(item)
            self.items[-1].amount += 1
            self.subtract_gold(item.price)
            return 1

    def add_gold(self, value):
        self.gold += value
        for i in range(value):
            self.add_item(create_item("gold"))

    def subtract_gold(self, value):
        self.gold -= value
        self.items[0].amount = self.gold

    def sell_item(self, item):
        if item.sellable and item in self.items:
            self.add_gold(item.price // 2)
            item.amount -= 1
            self.check_items_amount()

    def check_items_amount(self):
        for i in self.items:
            if i.amount == 0 and i.name != "gold":
                self.items.remove(i)

    def draw(self):
        for each in self.eq_background_rectangles:
            pygame.draw.rect(WIN, BLACK, each)
        for each in self.eq_rectangles:
            pygame.draw.rect(WIN, BROWN, each)
        for index, each in enumerate(self.items):
            each.update_amount_text()
            item_position = self.eq_rectangles[self.capacity - index - 1].topleft
            WIN.blit(each.item_image, item_position)
            each.rectangle.topleft = item_position
            if each.stackable:
                text_pos_x = item_position[0] + each.rectangle.width - each.amount_text.get_width()
                text_pos_y = item_position[1] + each.rectangle.height - each.amount_text.get_height()
                WIN.blit(each.amount_text, (text_pos_x, text_pos_y))

    def item_used(self, i):
        i = self.items.index(i)
        self.items[i].amount -= 1
        self.check_items_amount()


class Item:
    def __init__(self, name, sellable, usable, stackable, attack_power, price, description, use):
        self.name = name
        self.price = price
        self.attack_power = attack_power
        self.item_image = ITEMS_IMAGES[name]
        self.rectangle = self.item_image.get_rect()
        self.sellable = sellable
        self.usable = usable
        self.stackable = stackable
        self.use = use
        self.amount = 0
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))
        self.description = description
        if self.attack_power == 0:
            self.info_text = my_font.render(f"price: {self.price} description: {self.description}", True,
                                            (255, 255, 255))
        else:
            self.info_text = my_font.render(f"price: {self.price} description: attack power +{self.attack_power}", True,
                                            (255, 255, 255))
        self.info_rectangle = self.info_text.get_rect()

    def update_amount_text(self):
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))


class Store:
    def __init__(self, hero_type):
        self.available_items = []
        if hero_type == "knight":
            self.available_items.append(create_item("hp_potion"))
            self.available_items.append(create_item("sword_1"))
            self.available_items.append(create_item("sword_2"))
            self.available_items.append(create_item("sword_3"))
            self.available_items.append(create_item("sword_4"))
            self.available_items.append(create_item("level_up"))
        else:
            self.available_items.append(create_item("hp_potion"))
            self.available_items.append(create_item("ring_1"))
            self.available_items.append(create_item("ring_2"))
            self.available_items.append(create_item("ring_3"))
            self.available_items.append(create_item("ring_4"))
            self.available_items.append(create_item("level_up"))

        self.is_visible = False
        self.rectangles = []
        self.background_rectangles = []
        for each in range(len(self.available_items)):
            rectangle = pygame.Rect((WIDTH / 2) + len(self.available_items) / 2 * 40 - each * 40,
                                    HEIGHT / 4, ITEMS_WIDTH, ITEMS_HEIGHT)
            background_rectangle = pygame.Rect(WIDTH / 2 + len(self.available_items) / 2 * 40 - each * 40 - 4,
                                               HEIGHT / 4 - 4, 40, 40)
            self.rectangles.append(rectangle)
            self.background_rectangles.append(background_rectangle)

    def draw(self):
        if self.is_visible:
            for each in self.background_rectangles:
                pygame.draw.rect(WIN, BLACK, each)
            for each in self.rectangles:
                pygame.draw.rect(WIN, BROWN, each)
            for each in self.available_items:
                item_position = self.rectangles[
                    len(self.available_items) - self.available_items.index(each) - 1].topleft
                WIN.blit(each.item_image, item_position)
                each.rectangle.topleft = item_position


def use_hp_potion(player):
    return player.heal(50)


items = {
    "gold": ["gold", False, False, True, 0, 0, "use to buy items", None],
    "hp_potion": ["hp_potion", True, True, True, 0, 2, "heal 50hp", use_hp_potion],
    "sword_1": ["sword_1", True, False, False, 20, 30, None, None],
    "sword_2": ["sword_2", True, False, False, 100, 150, None, None],
    "sword_3": ["sword_3", True, False, False, 200, 500, None, None],
    "sword_4": ["sword_4", True, False, False, 500, 1500, None, None],
    "ring_1": ["ring_1", True, False, False, 20, 30, None, None],
    "ring_2": ["ring_2", True, False, False, 100, 50, None, None],
    "ring_3": ["ring_3", True, False, False, 200, 500, None, None],
    "ring_4": ["ring_4", True, False, False, 500, 1500, None, None],
    "level_up": ["level_up", False, False, True, 0, 10,
                 "buy to level up enemies (be careful, this effect cannot be undone)", None]
}
