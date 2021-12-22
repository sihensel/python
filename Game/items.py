'''
items module
contains all item classes as well as the item list
all used items will be imported from here
'''

class Item:
    def __init__(self, name, weight, value=0, equippable=False, usable=False, magic=False):
        self._name = name
        self._weight = weight
        self._value = value
        self._is_equippable = equippable
        self._is_usable = usable

    def get_item(self):
        return {'name': self._name, 'weight': self._weight, 'value': self._value,
                'is_equippable': self._is_equippable, 'is_usable': self._is_usable}

class Weapon(Item):
    def __init__(self, name, weight, value, dmg, _type):
        super().__init__(name, weight, value, equippable=True)
        self._damage = dmg
        self._type = _type
    
    def get_item(self):
        return {'name': self._name, 'weight': self._weight, 'value': self._value,
                'is_equippable': self._is_equippable, 'is_usable': self._is_usable,
                'damage': self._damage, 'type': self._type}

class Arrow(Item):
    def __init__(self, name, weight, value, dmg):
        super().__init__(name, weight, value, equippable=True)
        self._damage = dmg
        self._type = "arrow"
    
    def get_item(self):
        return {'name': self._name, 'weight': self._weight, 'value': self._value,
                'is_equippable': self._is_equippable, 'is_usable': self._is_usable,
                'damage': self._damage, 'type': self._type}

class Armor(Item):
    def __init__(self, name, weight, value, arm):
        super().__init__(name, weight, value, equippable=True)
        self._armor = arm
        self._type = "armor"
    
    def get_item(self):
        return {'name': self._name, 'weight': self._weight, 'value': self._value,
                'is_equippable': self._is_equippable, 'is_usable': self._is_usable,
                'armor': self._armor, 'type': self._type}
    
class Potion(Item):
    def __init__(self, name, weight, value, amount, _type):
        super().__init__(name, weight, value, usable=True)
        self._amount = amount
        self._type = _type
    
    def get_potion(self):
        return {'name': self._name, 'weight': self._weight, 'value': self._value,
                'is_equippable': self._is_equippable, 'is_usable': self._is_usable,
                'amount': self._amount, 'type': self._type}


''' ITEM LIST '''
''' WEAPONS '''
iron_sword = Weapon("Iron Sword", 2, 50, 10, "melee")
iron_axe = Weapon("Iron Axe", 3, 75, 15, "melee")

short_bow = Weapon("Short Bow", 1, 50, 8, "ranged")
long_bow = Weapon("Long Bow", 2, 150, 12, "ranged")

stone_arrow = Arrow("Stone Arrow", 0, 2, 1)
iron_arrow = Arrow("Iron Arrow", 0, 5, 2)

''' ARMOR '''
cloth_armor = Armor("Cloth Armor", 2, 30, 4)
leather_armor = Armor("Leather Armor", 5, 80, 7)
chain_armor = Armor("Iron Armor", 10, 150, 13)
plate_armor = Armor("Iron Plate Armor", 15, 400, 20)

''' POTIONS '''
small_health_potion = Potion("Small Health Potion", 0.5, 50, 30, "health")
great_health_potion = Potion("Great Health Potion", 0.5, 150, 80, "health")
small_mana_potion = Potion("Small Mana Potion", 0.5, 60, 20, "mana")
great_mana_potion = Potion("Great Health Potion", 0.5, 170, 45, "mana")
battle_potion = Potion("Battle Potion", 0.5, 150, 5, "buff")
poison = Potion("Poison", 0.5, 100, 20, "poison")

'''MISC'''
iron_ore = Item("Iron Ore", 2, 5)
