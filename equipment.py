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
        self.add_item("gold", False, False, True)

    def add_item(self, item_name, sellable, usable, stackable):
        if len(self.items) == 6:
            pass
        elif self.check_if_in_eq_and_stackable(item_name):
            for each in self.items:
                if each.name == item_name:
                    each.amount += 1
                    each.update_amount_text()
        else:
            item = Item(item_name, self.eq_rectangles[self.capacity - 1 - len(self.items)].topleft, sellable, usable,
                        stackable)
            self.items.append(item)

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
            WIN.blit(each.item_image, each.item_position)
            if each.stackable:
                print(each.item_image.get_rect())
                text_pos_x = each.item_position[0] + each.item_image.get_rect().width - each.amount_text.get_width()
                text_pos_y = each.item_position[1] + each.item_image.get_rect().height - each.amount_text.get_height()
                WIN.blit(each.amount_text, (text_pos_x, text_pos_y))


class Item:
    def __init__(self, name, position, sellable=True, usable=True, stackable=True):
        self.name = name
        self.item_image = ITEMS[name]
        self.item_position = position
        self.sellable = sellable
        self.usable = usable
        self.stackable = stackable
        self.amount = 1
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))

    def update_amount_text(self):
        self.amount_text = my_bold_font.render(str(self.amount), True, (0, 255, 0))


class Store:
    def __init__(self):
        pass
