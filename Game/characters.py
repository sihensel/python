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
                 race=None, _class=None, dmg=1, arm=0, is_enemy=False):
        # set hitpoints and mana to max when initializing a new character
        self.name = name
        self.max_hitpoints = maxhp
        self.max_manapoints = maxmp
        self.hitpoints = maxhp
        self.manapoints = maxmp
        self.damage = dmg
        self.armor = arm

        self.level = 1
        self.xp = 0
        # classes are not implemented yet
        # classes affect stats and levelup stats
        self.race = race
        self._class = _class

        self.strength = self.level
        self.dexterity = self.level
        self.intelligence = self.level

        self.inventory = {'weapons': [], 'armor': [], 'potions': []}
        self.carry_weight = 0.0
        # max_carry_weight should depend on level or strength
        self.max_carry_weight = 50.0
        self.known_spells = []
        self.equipped_weapon = None
        self.equipped_armor = None

        self.is_enemy = is_enemy

    def set_level(self, lvl):
        self.level = lvl

        # change this behaviour
        self.strength = lvl
        self.dexterity = lvl
        self.intelligence = lvl

    # !!! STILL NEEDS TO BE IMPLEMENTED PROPERLY !!!
    # something in the likes of these
    def set_stats(self):
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
        # let it be 1 points for now, but can be more later
        points = int(self.level/10 + 1)
        print(f"You have {points} points. How would you like to spend them?")
        pass
        # input()

    # !!! STILL NEEDS TO BE IMPLEMENTED PROPERLY !!!
    # when the character dies
    def death(self):
        print(f"{self.name} is dead")
        return self.xp  # xp should be proportional to the killed target

    # attack another creature
    def attack(self, target, add_damage=0):
        damage = 0
        if self.equipped_weapon.__class__.__name__ == "melee_weapon":
            damage = self.damage + round(0.75 * self.strength, 0) + add_damage
        elif self.equipped_weapon.__class__.__name__ == "ranged_weapon":
            damage = self.damage + round(0.75*self.dexterity, 0) + add_damage
        else:
            damage = self.damage + add_damage
        target.get_hit(damage)

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

    # calculates the recieved damage (dependent on armor)
    def get_hit(self, dmg):
        self.hitpoints -= int(dmg - (20/(20 + self.armor)))
        if self.hitpoints <= 0:
            self.death()

    # character gets a debuff (currently only for attack and armor)
    def get_debuff(self, amount, duration):
        self.damage = self.damage - amount
        if self.damage < 0:
            self.damage = 0
        self.armor = self.armor - amount
        if self.armor < 0:
            self.armor = 0
        '''
        if effect == "attack":
            self.damage = self.damage - amount
            if self.damage < 0:
                self.damage = 0
        elif effect == "armor":
            self.armor = self.armor - amount
            if self.armor < 0:
                self.armor = 0
        '''

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

    # TODO rethink how potions work and which parameters they have
    def use_item(self, item: items.Potion) -> str:
        '''
        Uses an item and removes it aferwards
        Only potions are usable (for now)
        '''
        if item._is_usable:
            if item.get_potion()['type'] == "health":
                self.hitpoints += item.get_item()['amount']
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif item.get_potion()['type'] == "mana":
                self.manapoints += item.get_item()['amount']
                if self.manapoints > self.max_manapoints:
                    self.manapoints = self.max_manapoints
            elif item.get_potion()['type'] == "buff":
                self.damage = self.damage + item.get_potion()['amount']
                self.armor = self.armor + item.get_potion()['amount']
            self.remove_item(item)
            return f'Used item {item.get_item()["name"]}'
        else:
            return f'Item {item.get_item()["name"]} cannot be used'

    def learn_spell(self, spell: spells.Spell):
        if self.level < spell.get_spell()['level']:
            return (f'Need to be at least level {spell.get_spell()["level"]}'
                    + 'to learn {spell.get_spell()["name"]}')
        elif spell in self.known_spells:
            return f'Already know {spell.get_spell()["name"]}'
        else:
            # there is no limit for known spells per level yet
            # this can be regulated by the number of spells available
            # or setting a max no. of spells that can be learnt
            self.known_spells.append(spell)
        return f'Learned spell {spell.get_spell()["name"]}'


class Player(Character):
    def __init__(self, name, maxhp, maxmp,
                 race=None, _class=None, dmg=1, arm=0, is_enemy=False):
        super().__init__(name, maxhp, maxmp, race, _class, dmg, arm)

    def get_xp(self, amount):
        '''
        only the player can get xp

        level formula: 100*level**2 - 100*level
        lvl 1   0
        lvl 2   200
        lvl 3   600
        lvl 4   1200, etc.
        '''
        self.xp += amount
        if self.xp >= (100 * ((self.level+1)**2) - (100*(self.level+1))):
            print(self.level_up())
        # show the xp gained before level up
        return "{} xp recieved!".format(amount)

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

        return "Level up!"

    def death(self):
        '''
        # reset level progress
        self.xp = (100 * (self.level**2) - (100*self.level))
        '''
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

p = Player("Main Character", 100, 50, 1, 0)
# e = Character("Dark Knight", 80, 50, 10)

p.add_item(items.iron_sword)
p.add_item(items.chain_armor)
p.add_item(items.small_health_potion)
p.add_item(items.iron_axe)

print(p.inventory)

p.show_intentory()

print(p.learn_spell(spells.weak_healing))
print(p.learn_spell(spells.weak_healing))

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
p.add_item(items.poison)
p.use_item(p.inventory[5])
# __dict__ lists all attributes in a dictionary
print(p.__dict__)
'''
