#!/usr/bin/env python3

'''
spells that can be casted by the player and NPCs (incliuding enemies)
'''


class Spell:
    def __init__(self, name, mana_cost, target, effect, amount,
                 duration=0, lvl=1):
        self._name = name
        self._mana_cost = mana_cost
        self._target = target
        self._effect = effect
        self._amount = amount
        self._duration = duration
        self._level = lvl

    def get_spell(self):
        return {'name': self._name, 'mana_cost': self._mana_cost,
                'target': self._target, 'effect': self._effect,
                'amount': self._amount, 'duraction': self._duration,
                'level': self._level}


''' SPELL LIST '''
# TODO: Effects need to be reworked
weak_healing = Spell("Small Healing", 20, "self", "healing", 30)
fireball = Spell("Fireball", 30, "other", "damage", 35)
magic_armor = Spell("Magic Armor", 40, "self", "buff", 30, 5, 3)
weaken = Spell("Weaken", 40, "other", "debuff", 10, 5, 3)
