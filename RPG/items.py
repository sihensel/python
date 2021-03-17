'''
items module
contains all item classes as well as the item list
all used items will be imported from here
'''

class item:
    def __init__(self, name, weight, value=0, equippable=False, usable=False, magic=False):
        self._name = name
        self._weight = weight
        self._value = value
        self.is_equippable = equippable
        self.is_usable = usable

    def get_item(self):
        return self._name, self._weight, self._value

class weapon(item):
    def __init__(self, name, weight, value, dmg, _type):
        super().__init__(name, weight, value, equippable=True)
        self.damage = dmg
        self._type = _type
    
    def get_item(self):
        return self._name, self._weight, self._value, self.damage, self._type

class arrow(item):
    def __init__(self, name, weight, value, dmg):
        super().__init__(name, weight, value, equippable=True)
        self.damage = dmg
        self._type = "arrow"
    
    def get_item(self):
        return self._name, self._weight, self._value, self.damage, self._type

class armor(item):
    def __init__(self, name, weight, value, arm):
        super().__init__(name, weight, value, equippable=True)
        self.armor = arm
        self._type = "armor"
    
    def get_item(self):
        return self._name, self._weight, self._value, self.armor, self._type
    
class potion(item):
    def __init__(self, name, weight, value, amount, _type):
        super().__init__(name, weight, value, usable=True)
        self.amount = amount
        self._type = _type
    
    def get_potion(self):
        return self._name, self._weight, self._value, self.amount, self._type


''' ITEM LIST '''
''' WEAPONS '''
iron_sword = weapon("Iron Sword", 2, 50, 10, "melee")
iron_axe = weapon("Iron Axe", 3, 75, 15, "melee")

short_bow = weapon("Short Bow", 1, 50, 8, "ranged")
long_bow = weapon("Long Bow", 2, 150, 12, "ranged")

stone_arrow = arrow("Stone Arrow", 0, 2, 1)
iron_arrow = arrow("Iron Arrow", 0, 5, 2)

''' ARMOR '''
cloth_armor = armor("Cloth Armor", 2, 30, 4)
leather_armor = armor("Leather Armor", 5, 80, 7)
chain_armor = armor("Iron Armor", 10, 150, 13)
plate_armor = armor("Iron Plate Armor", 15, 400, 20)

''' POTIONS '''
small_health_potion = potion("Small Health Potion", 0.5, 50, 30, "health")
great_health_potion = potion("Great Health Potion", 0.5, 150, 80, "health")
small_mana_potion = potion("Small Mana Potion", 0.5, 60, 20, "mana")
great_mana_potion = potion("Great Health Potion", 0.5, 170, 45, "mana")
battle_potion = potion("Battle Potion", 0.5, 150, 5, "buff")
poison = potion("Poison", 0.5, 100, 20, "poison")

'''MISC'''
iron_ore = item("Iron Ore", 2, 5)