'''
spells that can be casted by the player and NPCs (incliuding enemies)
'''

class spell:
    def __init__(self, name, cost, target, effect, amount, duration=0, min_lvl=1):
        self.name = name
        self.cost = cost
        self.target = target
        self.effect = effect
        self.amount = amount
        self.duration = duration
        self.min_level = min_lvl
    
    def get_spell(self):
        return self.name, self.cost, self.target, self.effect, self.amount, self.duration, self.min_level

''' SPELL LIST '''
weak_healing = spell("Small Healing", 20, "self", "healing", 30)
fireball = spell("Fireball", 30, "enemy", "damage", 35)
magic_armor = spell("Magic Armor", 40, "self", "buff", 30, 5, 3)
weaken = spell("Weaken", 40, "enemy", "debuff", 10, 5, 3)