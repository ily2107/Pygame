from entities.items.base_item import Base_item

class Tranquillizer_tick(Base_item):
    def __init__(self):
        super().__init__("tranquillizer_tick")

    def use(self, level, player):
        