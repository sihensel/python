#!/usr/bin/env python3

'''
spells that can be casted by the player and NPCs
'''


class Spell:
    def __init__(self, name: str, mana_cost: int, target: str, effect: str,
                 amount: int, lvl: int = 1):
        self._name = name
        self._mana_cost = mana_cost
        self._target = target
        self._effect = effect
        self._amount = amount
        self._level = lvl

    def get_spell(self) -> dict:
        '''
        returns the whole object as a dict
        '''
        return {'name': self._name, 'mana_cost': self._mana_cost,
                'target': self._target, 'effect': self._effect,
                'amount': self._amount, 'level': self._level}

    def get_name(self) -> str:
        return self._name

    def get_mana_cost(self) -> int:
        return self._mana_cost

    def get_target(self) -> str:
        return self._target

    def get_effect(self) -> str:
        return self._effect

    def get_amount(self) -> int:
        return self._amount

    def get_level(self) -> int:
        return self._level


''' SPELL LIST '''
healing = Spell("Small Healing", 20, "self", "healing", 30)
fireball = Spell("Fireball", 30, "other", "damage", 35, 3)
