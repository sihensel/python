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

# TODO change returns for print()


class Character:
    '''
    Class for all characters (player, enemies and NPCs)
    '''
    def __init__(self, name, maxhp, maxmp,
                 race=None, _class=None, dmg=1, arm=0, is_enemy=False):
        # set hitpoints and mana to max when initializing a new character
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

        # TODO rethink this
        self.strength = self.level
        self.dexterity = self.level
        self.intelligence = self.level

        # items are auto-sorted by their type
        self.inventory = {'weapons': [], 'armor': [], 'potions': []}
        self.carry_weight = 0.0
        # TODO max_carry_weight should depend on level or strength
        self.max_carry_weight = 50.0
        self.known_spells = []
        self.equipped_weapon = None
        self.equipped_armor = None

        # TODO rethink how hostile NPCs work, maybe leeave it out
        self.is_enemy = is_enemy

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
        # TODO implement user input
        points = int(self.level/5 + 1)
        print(f"You have {points} points. How would you like to spend them?")
        # input('1 - str, 2 - dex, 3 - int')
        pass

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

        info = target.get_hit(damage)
        print(f'{self.name} attacks {target.name} for {info["damage"]} damage')
        if info['hitpoints'] <= 0:
            if target.__class__.__name__ == 'Player':
                target.death()

    def cast_spell(self, spell, target=None):
        if spell.get_spell()[1] > self.manapoints:
            return "Not enough mana"
        else:
            if spell.get_spell()[3] == "healing":
                self.hitpoints += (spell.get_spell()[4]
                                   + round(0.75*self.intelligence, 0))
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif spell.get_spell()[3] == "damage":
                target.get_hit(spell.get_spell()[4]
                               + round(0.75*self.intelligence, 0))
            elif spell.get_spell()[3] == "buff":
                self.armor += (spell.get_spell()[4]
                               + round(0.75*self.intelligence, 0))
            elif spell.get_spell()[3] == "debuff":
                target.get_debuff(spell.get_spell()[4]
                                  + round(0.75*self.intelligence, 0),
                                  spell.get_spell()[5])
            self.manapoints = self.manapoints - spell.get_spell()[1]

    def get_hit(self, dmg: float) -> dict:
        '''
        Calculates the recieved damage (dependent on armor)
        '''
        damage_recieved = int(dmg - (20/(20 + self.armor)))
        self.hitpoints -= damage_recieved
        return {'hitpoints': self.hitpoints, 'damage': damage_recieved}

    def get_debuff(self, amount, duration):
        '''
        Character gets a debuff (affects damage and armor)
        When armor or damage would reach 0, set it to 1
        '''
        self.damage -= amount
        if self.damage <= 0:
            self.damage = 1
        self.armor -= amount
        if self.armor <= 0:
            self.armor = 1

    ###################################################################
    # Inventory operations
    ###################################################################

    def add_item(self, item: items.Item) -> str:
        '''
        Add an item to the inventory
        '''
        if ((self.carry_weight + item.get_item()['weight'])
                > self.max_carry_weight):
            return "Inventory full"
        else:
            if item.__class__.__name__ == 'Weapon':
                self.inventory['weapons'].append(item)
            elif item.__class__.__name__ == 'Armor':
                self.inventory['armor'].append(item)
            elif item.__class__.__name__ == 'Potion':
                self.inventory['potions'].append(item)

            self.carry_weight += item.get_item()['weight']
        return f'Item {item.get_item()["name"]} added to inventory'

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

        return f'Removed item {item.get_item()["name"]}'

    def equip_item(self, item: items.Item) -> str:
        '''
        Equip an item (if it is equippable)
        '''
        if item._is_equippable:
            if item.__class__.__name__ == 'Weapon':
                self.damage = item.get_item()['damage']
                self.equipped_weapon = item
            elif item.__class__.__name__ == "Armor":
                self.armor = item.get_item()['armor']
                self.equipped_armor = item
            return f'Equipped item {item.get_item()["name"]}'
        else:
            return f'Item {item.get_item()["name"]} cannot be equipped'

    def unequip_item(self, item: items.Item) -> str:
        '''
        Unequip an item
        '''
        if self.equipped_weapon == item or self.equipped_armor == item:
            if item.__class__.__name__ == "Weapon":
                self.equipped_weapon = None
            elif item.__class__.__name__ == "armor":
                self.equipped_armor = None
            return f'Unequipped item {item.get_item()["name"]}'
        else:
            return f'Item {item.get_item()["name"]} cannot be unequipped'

    def use_potion(self, item: items.Potion) -> str:
        '''
        Uses a potion and remove it aferwards
        Postions are the only items that can be used
        '''
        if item.__class__.__name__ == 'Potion':
            if item.get_item()['type'] == "health":
                if self.hitpoints == self.max_hitpoints:
                    return 'Already at maximum hitpoints'

                self.hitpoints += item.get_item()['amount']
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif item.get_item()['type'] == "mana":
                if self.manapoints == self.max_manapoints:
                    return 'Already at maximum manapoints'

                self.manapoints += item.get_item()['amount']
                if self.manapoints > self.max_manapoints:
                    self.manapoints = self.max_manapoints
            elif item.get_item()['type'] == "buff":
                # can only have one active buff at a time
                if self.buff_duration:
                    return 'You already have an active buff'

                self.damage = self.damage + item.get_item()['amount']
                self.armor = self.armor + item.get_item()['amount']
                self.buff_duration = item.get_item()['duration']
            self.remove_item(item)
            return f'Used item {item.get_item()["name"]}'
        else:
            return f'Item {item.get_item()["name"]} cannot be used'

    def learn_spell(self, spell: spells.Spell) -> str:
        '''
        Only the player can learn spells
        The player must be at least the same level as the spell
        '''
        if self.level < spell.get_spell()['level']:
            return (f'Need to be at least level {spell.get_spell()["level"]} '
                    f'to learn {spell.get_spell()["name"]}')
        elif spell in self.known_spells:
            return f'Already know {spell.get_spell()["name"]}'
        else:
            self.known_spells.append(spell)
            return f'Learned spell {spell.get_spell()["name"]}'


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
        self.level += 1

        # TODO reimplement levelling of charachter attributes
        self.max_hitpoints = self.max_hitpoints + self.level * 10
        self.max_manapoints = self.max_manapoints + self.level * 5

        # TODO decide if hp and mana are restored on level up
        self.hitpoints = self.max_hitpoints
        self.manapoints = self.max_manapoints

        # if there will be point-buy, then this is obsolete
        self.strength += 1
        self.dexterity += 1
        self.intelligence += 1

        # TODO make this in relation to strength or a fixed value
        self.max_carry_weight = self.max_carry_weight + self.strength * 5

        print('level up')
        return "Level up!"

    def attack(self, target):
        '''
        Attack another character
        If it dies, gain xp proportial to the level difference

        if enemy is same or higher level:
        ((100 * self.level ** 2) - 100 * self.level) * leveldiff + 1 / 7

        if enemy is lower level:
        ((100 * self.level ** 2) - 100 * self.level) * 1 / 7 / leveldiff + 1
        '''
        if self.equipped_weapon.__class__.__name__ == "melee_weapon":
            damage = self.damage + round(0.75 * self.strength, 0)
        elif self.equipped_weapon.__class__.__name__ == "ranged_weapon":
            damage = self.damage + round(0.75*self.dexterity, 0)
        else:
            damage = self.damage

        info = target.get_hit(damage)
        print(f'{self.name} attacks {target.name} for {info["damage"]} damage')

        if info['hitpoints'] <= 0:
            if target.level >= self.level:
                xp_gain = (((100 * (self.level + 1) ** 2)
                           - 100 * (self.level + 1))
                           * (target.level - self.level + 1) / 7)
            else:
                xp_gain = (((100 * (self.level + 1) ** 2)
                           - 100 * (self.level + 1))
                           * 1 / 7 / (self.level - target.level + 1))
            self.gain_xp(round(xp_gain, 2))

    def death(self):
        '''
        Reset part of the level progress
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


''' TEST AREA '''

p = Player("Main Character", 10, 50, 1, 0)
e = Character("Dark Knight", 10, 50, 10)

p.add_item(items.iron_sword)
p.add_item(items.chain_armor)

print(p.equip_item(p.inventory['weapons'][0]))
print(p.equip_item(p.inventory['armor'][0]))

e.equip_item(items.iron_axe)
e.attack(p)

'''
e.equip_item(e.inventory[0])
e.equip_item(e.inventory[1])

p.learn_spell(spells.weak_healing)
p.learn_spell(spells.fireball)
print(p.known_spells)
print(p.known_spells[0].get_spell())

print(p.inventory)
print(e.inventory)

p.add_item(items.short_bow)
print(p.equip_item(p.inventory[3]))

print(p.inventory[3])
print(p.equipped_weapon)
print(p.damage)

p.equip_item(p.inventory[4])
print(e.hitpoints)
print(p.attack(e))
print(e.hitpoints)

e.learn_spell(spells.weak_healing)
e.cast_spell(e.known_spells[0])
print("mana", e.manapoints)
print("hp", e.hitpoints)

p.cast_spell(p.known_spells[1], e)
print(p.manapoints)
print(e.hitpoints)
e.cast_spell(e.known_spells[0])
print(e.hitpoints)

print(p.get_xp(200))
print(p.xp)
print(p.level)
print(p.max_hitpoints, p.max_manapoints)

print(p.get_xp(400))
print(p.xp)
print(p.level)
print(p.max_hitpoints, p.max_manapoints)

print(e.hitpoints)
p.use_item(p.inventory[5])
# __dict__ lists all attributes in a dictionary
print(p.__dict__)
'''
