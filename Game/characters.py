#!/usr/bin/env python3

'''
This is not (and never will be) a complete or playable game
and rather just represents a collections of systems
(like an inventory, fighting, levelling up, etc.) that I did for fun


characters module
includes the player and all NPCs (including enemies)
'''

# game modules
import items
import spells


class Character:
    '''
    Class for all characters (player, enemies and NPCs)
    '''
    def __init__(self, name, maxhp, maxmp,
                 dmg=1, arm=0, race=None, _class=None):
        self.name = name
        self.max_hitpoints = maxhp
        self.max_manapoints = maxmp
        self.hitpoints = maxhp
        self.manapoints = maxmp
        self.damage = dmg
        self.armor = arm

        # duration of active buffs, can only have one buff at a time
        self.buff_duration = 0

        self.level = 1
        self.xp = 0
        # TODO implement classes (Warrior, Mage, etc)
        # classes should affect stats and levelup stats
        self.race = race
        self._class = _class

        self.strength = 1
        self.dexterity = 1
        self.intelligence = 1

        # items are auto-sorted by their type
        self.inventory = {'weapons': [], 'armor': [], 'potions': []}
        self.carry_weight = 0.0     # current carry weight
        self.max_carry_weight = int(50 + self.strength * 2 + self.level)
        self.equipped_weapon: items.Weapon = None
        self.equipped_armor: items.Armor = None
        self.known_spells = []

    def set_stats(self):
        '''
        Set stats according to the character level
        '''
        # TODO check if this is necessary (maybe for NPCs)
        if self._class == "Warrior":
            self.strength = 3
            self.dexterity = 1
            self.intelligence = 1
        elif self._class == "Ranger":
            self.strength = 1
            self.dexterity = 3
            self.intelligence = 1
        elif self._class == "Mage":
            self.strength = 1
            self.dexterity = 1
            self.intelligence = 3

    def point_buy(self):
        '''
        The player can spent attribute points on level up
        The amount of points = level / 5 + 1
        '''
        points = int(self.level/5 + 1)
        while True:
            if points >= 1:
                cmd = input(f'''\nYou have {points} points. How would you like to spend them?
                                1) Strength
                                2) Dexterity
                                3) Intelligence\n''')
                if cmd in ['1', '2', '3']:
                    if cmd == '1':
                        self.strength += 1
                        print(f'Strength increased to {self.strength}')
                    elif cmd == '2':
                        self.dexterity += 1
                        print(f'Dexterity increased to {self.dexterity}')
                    elif cmd == '3':
                        self.intelligence += 1
                        print(f'Intelligence increased to {self.intelligence}')
                    points -= 1
                else:
                    print('Please press the number of the attribute '
                          'you want to increase')
            else:
                break

    def get_hit(self, dmg: int) -> dict:
        '''
        Calculates the recieved damage (dependent on armor)
        '''
        damage_recieved = int(dmg - (20/(20 + self.armor)))
        self.hitpoints -= damage_recieved
        return {'damage': damage_recieved, 'hitpoints': self.hitpoints}

    def attack(self, target):
        '''
        Attack another character
        If the player dies, run Player.death()
        '''
        damage = 0
        if self.equipped_weapon.__class__.__name__ == "melee_weapon":
            damage = self.damage + round(0.75 * self.strength, 0)
        elif self.equipped_weapon.__class__.__name__ == "ranged_weapon":
            damage = self.damage + round(0.75*self.dexterity, 0)
        else:
            # TODO add formula for Mage characters/spells
            damage = self.damage

        result = target.get_hit(damage)
        print(f'{self.name} attacks {target.name} for '
              f'{result["damage"]} damage')
        if result['hitpoints'] <= 0:
            print(f'{target.name} died')
            if target.__class__.__name__ == 'Player':
                target.death()

    def cast_spell(self, spell, target=None):
        '''
        Cast a spell
        Check the spell type and do the corresponding action
        '''
        result = {}
        if spell.get_mana_cost() > self.manapoints:
            print("Not enough mana")
            return False
        else:
            if (spell.get_effect() == "healing" and
                    spell.get_target() == 'self'):
                self.hitpoints += int(spell.get_amount()
                                      + round(0.75*self.intelligence, 0))
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif spell.get_effect() == "damage":
                result = target.get_hit(int(spell.get_amount()
                                        + round(0.75*self.intelligence, 0)))

            self.manapoints -= spell.get_mana_cost()
            print(f'{self.name} attacks {target.name} for '
                  f'{result["damage"]} damage')
            if result['hitpoints'] <= 0:
                print(f'{target.name} died')
                if target.__class__.__name__ == 'Player':
                    target.death()

    ###################################################################
    # Inventory operations
    ###################################################################

    def add_item(self, item: items.Item) -> str:
        '''
        Add an item to the inventory
        '''
        if self.carry_weight + item.get_weight() > self.max_carry_weight:
            return "Inventory full"
        else:
            if item.__class__.__name__ == 'Weapon':
                self.inventory['weapons'].append(item)
            elif item.__class__.__name__ == 'Armor':
                self.inventory['armor'].append(item)
            elif item.__class__.__name__ == 'Potion':
                self.inventory['potions'].append(item)

            self.carry_weight += item.get_weight()
        return f'Item {item.get_name()} added to inventory'

    def remove_item(self, item: items.Item) -> str:
        '''
        Remove an item from the inventory
        Unequip the item if it is equipped
        '''
        if item == self.equipped_weapon or item == self.equipped_armor:
            self.unequip_item(item)
        if item.__class__.__name__ == 'Weapon':
            self.inventory['weapons'].remove(item)
        elif item.__class__.__name__ == 'Armor':
            self.inventory['armor'].remove(item)
        elif item.__class__.__name__ == 'Potion':
            self.inventory['potions'].remove(item)

        return f'Removed item {item.get_name()}'

    def equip_item(self, item: items.Weapon | items.Armor) -> str:
        '''
        Equip an item (if it is equippable)
        '''
        if item._is_equippable:
            if item.__class__.__name__ == 'Weapon':
                self.damage = item.get_damage()
                self.equipped_weapon = item
            elif item.__class__.__name__ == "Armor":
                self.armor = item.get_armor()
                self.equipped_armor = item
            return f'Equipped item {item.get_name}'
        else:
            return f'Item {item.get_name()} cannot be equipped'

    def unequip_item(self, item: items.Weapon | items.Armor) -> str:
        '''
        Unequip an item
        '''
        if self.equipped_weapon == item or self.equipped_armor == item:
            if item.__class__.__name__ == "Weapon":
                self.equipped_weapon = None
            elif item.__class__.__name__ == "Armor":
                self.equipped_armor = None
            return f'Unequipped item {item.get_name()}'
        else:
            return f'Item {item.get_name()} cannot be unequipped'

    def use_potion(self, item: items.Potion) -> str:
        '''
        Uses a potion and remove it aferwards
        Postions are the only items that can be used
        '''
        if item.__class__.__name__ == 'Potion':
            if item.get_type() == "health":
                if self.hitpoints == self.max_hitpoints:
                    return 'Already at maximum hitpoints'

                self.hitpoints += item.get_amount()
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif item.get_type == "mana":
                if self.manapoints == self.max_manapoints:
                    return 'Already at maximum manapoints'

                self.manapoints += item.get_amount()
                if self.manapoints > self.max_manapoints:
                    self.manapoints = self.max_manapoints
            elif item.get_type() == "buff":
                # can only have one active buff at a time
                if self.buff_duration:
                    return 'You already have an active buff'

                self.damage = self.damage + item.get_amount()
                self.armor = self.armor + item.get_amount()
                self.buff_duration = item.get_duration()
            self.remove_item(item)
            return f'Used item {item.get_name()}'
        else:
            return f'Item {item.get_name()} cannot be used'

    def learn_spell(self, spell: spells.Spell) -> str:
        '''
        The player must be at least the same level as the spell
        '''
        if self.level < spell.get_level():
            return (f'Need to be at least level {spell.get_level()} '
                    f'to learn {spell.get_name()}')
        elif spell in self.known_spells:
            return f'Already know {spell.get_name()}'
        else:
            self.known_spells.append(spell)
            return f'Learned spell {spell.get_name()}'


class Player(Character):
    def __init__(self, name, maxhp, maxmp,
                 race=None, _class=None, dmg=1, arm=0, is_enemy=False):
        super().__init__(name, maxhp, maxmp, race, _class, dmg, arm)

    def gain_xp(self, amount):
        '''
        only the player can get xp

        level formula: (100 * (level + 1) ** 2) - 100 * (level + 1)
        lvl 1   0
        lvl 2   200
        lvl 3   600
        lvl 4   1200, etc.
        '''
        self.xp += amount
        print(f'{amount} xp recieved')
        if self.xp >= (100 * (self.level + 1) ** 2) - 100 * (self.level + 1):
            self.level_up()

    def level_up(self):
        print('Level up!')
        self.level += 1

        # TODO reimplement levelling of charachter attributes
        self.max_hitpoints += self.level * 10
        self.max_manapoints += self.level * 5

        self.hitpoints = self.max_hitpoints
        self.manapoints = self.max_manapoints

        self.point_buy()
        self.max_carry_weight = int(50 + self.strength * 2 + self.level)

    def calculate_xp(self, target_level: int):
        '''
        If an attacked target dies, gain xp proportial to the level difference

        if enemy is same or higher level:
        ((100 * self.level ** 2) - 100 * self.level) * leveldiff + 1 / 7

        if enemy is lower level:
        ((100 * self.level ** 2) - 100 * self.level) * 1 / 7 / leveldiff + 1
        '''
        if target_level >= self.level:
            xp_gain = (((100 * (self.level + 1) ** 2)
                        - 100 * (self.level + 1))
                       * (target_level - self.level + 1) / 7)
        else:
            xp_gain = (((100 * (self.level + 1) ** 2)
                        - 100 * (self.level + 1))
                       * 1 / 7 / (self.level - target_level + 1))
        self.gain_xp(round(xp_gain, 2))

    def attack(self, target):
        '''
        Attack another character
        '''
        if self.equipped_weapon.get_type() == 'melee':
            damage = int(self.damage + round(0.75 * self.strength, 0))
        elif self.equipped_weapon.get_type() == 'ranged':
            damage = int(self.damage + round(0.75*self.dexterity, 0))
        elif self.equipped_weapon.get_type() == 'magic':
            damage = int(self.damage + round(0.75*self.intelligence, 0))
        else:
            damage = self.damage

        result = target.get_hit(damage)

        print(f'{self.name} attacks {target.name} for '
              f'{result["damage"]} damage')
        if result['hitpoints'] <= 0:
            print(f'{target.name} died')
            self.calculate_xp(target.level)

    def cast_spell(self, spell, target=None):
        '''
        Cast a spell
        Check the spell type and do the corresponding action
        '''
        result = {}
        if spell.get_mana_cost() > self.manapoints:
            print("Not enough mana")
        else:
            if (spell.get_effect() == "healing" and
                    spell.get_target() == 'self'):
                self.hitpoints += int(spell.get_amount()
                                      + round(0.75*self.intelligence, 0))
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif spell.get_effect() == "damage":
                result = target.get_hit(int(spell.get_amount()
                                            + round(0.75
                                                    * self.intelligence, 0)))

            self.manapoints -= spell.get_mana_cost()
            print(f'{self.name} attacks {target.name} for '
                  f'{result["damage"]} damage')
            if result['hitpoints'] <= 0:
                print(f'{target.name} died')
                self.calculate_xp(target.level)

    def death(self):
        '''
        Reset part of the progress to the next level
        If xp > (xp for next level) / 2 -> set xp to half xp for next level
        If xp < (xp for next level) / 2 -> set xp to start of xp for next level
        '''

        if self.xp > ((100 * (self.level + 1) ** 2)
                      - 100 * (self.level + 1)) / 2:
            self.xp = ((100 * (self.level + 1) ** 2)
                       - 100 * (self.level + 1)) / 2
        elif self.xp < ((100 * (self.level + 1) ** 2)
                        - 100 * (self.level + 1)) / 2:
            self.xp = (100 * (self.level) ** 2) - 100 * (self.level)
        return "You died!"

    def show_intentory(self):
        '''
        Print the inventory to the screen
        '''
        # TODO test different layouts
        print('---WEAPONS---')
        for item in self.inventory['weapons']:
            item = item.get_item()
            print(item)
            print(f"{item['name']}, {item['weight']} kg "
                  f"{item['value']} gold, {item['damage']} damage")

        print('---ARMOR---')
        for item in self.inventory['armor']:
            print(item.get_item())

        print('---POTIONS---')
        for item in self.inventory['potions']:
            print(item.get_item())

    def show_spells(self):
        '''
        Print all knows spells to the screen
        '''
        print('--- SPELLS ---')
        for spell in self.known_spells:
            print(f'{spell.get_name()}, {spell.get_mana_cost()} '
                  f'{spell.get_target()}, {spell.get_effect()}, '
                  f'{spell.get_amount()}, {spell.get_duration()}, '
                  f'{spell.get_level()}')


''' TEST AREA '''

p = Player("Main Character", 50, 25, 1, 0)
e = Character("Sample Enemy", 5, 25, 10)

p.add_item(items.iron_sword)
p.add_item(items.chain_armor)

print(p.equip_item(p.inventory['weapons'][0]))
print(p.equip_item(p.inventory['armor'][0]))

p.attack(e)
