'''
characters module
includes the player and all NPCs (including enemies)
'''

# game modules
import items
import spells
import text

# python modules
import time

from sys import exit

# Class for all characters (player, enemies and NPCs)
class character:
    def __init__(self, name, maxhp, maxmp, race=None, _class=None, dmg=1, arm=0, is_enemy=False):
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
        # classes are not implemented yet, will be warrior/knight, archer/ranger and wizard/mage to begin with
        # classes affect stats and levelup stats
        self.race = race
        self._class = _class
        
        self.strength = self.level
        self.dexterity = self.level
        self.intelligence = self.level

        self.inventory = ['weapon', [], 'armor', [], 'potion', []]
        self.carry_weight = 0.0
        # there needs to be some dependency to  the "max_carry_weight" value (level or strength)
        self.max_carry_weight = 50.0
        self.known_spells = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_arrow = None

        self.is_enemy = is_enemy

    def set_level(self, lvl):
        self.level = lvl
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
        print("You have {} points. How would you like to spend them?".format(points))
        pass
        # input()

    # !!! STILL NEEDS TO BE IMPLEMENTED PROPERLY !!!
    # when the character dies
    def death(self):
            print("{} is dead".format(self.name))
            del self
            return self.xp  # xp should be dependant on the level of the killed character

    # attack another creature
    def attack(self, target, add_damage=0):
        damage = 0
        if self.equipped_weapon.__class__.__name__ == "melee_weapon":
            damage = self.damage + round(0.75 * self.strength, 0) + add_damage
        elif self.equipped_weapon.__class__.__name__ == "ranged_weapon":
            if self.equipped_arrow == None:
                return "No arrows equipped"
            else:
                damage = self.damage + self.equipped_arrow.get_item()[3] + round(0.75*self.dexterity, 0) + add_damage
        else:
            damage = self.damage + add_damage
        target.get_hit(damage)
    
    def cast_spell(self, spell, target=None):
        if spell.get_spell()[1] > self.manapoints:
            return "Not enough mana"
        else:
            if spell.get_spell()[3] == "healing":
                self.hitpoints = self.hitpoints + spell.get_spell()[4] + round(0.75*self.intelligence, 0)
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif spell.get_spell()[3] == "damage":
                target.get_hit(spell.get_spell()[4] + round(0.75*self.intelligence, 0))
            elif spell.get_spell()[3] == "buff":
                self.armor = self.armor + spell.get_spell()[4] + round(0.75*self.intelligence, 0)
            elif spell.get_spell()[3] == "debuff":
                target.get_debuff(spell.get_spell()[4] + round(0.75*self.intelligence, 0), spell.get_spell()[5])
            self.manapoints = self.manapoints - spell.get_spell()[1]

    # calculates the recieved damage (dependant on armor)
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

    # adds an item to the inventory
    def add_item(self, item_to_add):
        if (self.carry_weight + item_to_add.get_item()[1]) > self.max_carry_weight:
            return "Inventory full"
        else:
            if item_to_add.__class__.__name__ == 'weapon':
                self.inventory[1].append(item_to_add)
            elif item_to_add.__class__.__name__ == 'armor':
                self.inventory[3].append(item_to_add)
            elif item_to_add.__class__.__name__ == 'potion':
                self.inventory[5].append(item_to_add)

            #self.inventory.append(item_to_add)
            self.max_carry_weight += item_to_add.get_item()[1]

    # removes an item from the inventory (but only the first instance, not all of it)
    # items that are currenty equipped will get unequipped first
    def remove_item(self, item_to_remove):
        for item in self.inventory:
            if item == item_to_remove:
                if item_to_remove == self.equipped_weapon or item_to_remove == self.equipped_armor:
                    self.unequip_item(item_to_remove)
                self.inventory.remove(item)

    # uses an item (if the item is usable)
    def use_item(self, item_to_use):
        if item_to_use.is_usable == True:
            if item_to_use.get_potion()[4] == "health":
                self.hitpoints += item_to_use.get_item()[3]
                if self.hitpoints > self.max_hitpoints:
                    self.hitpoints = self.max_hitpoints
            elif item_to_use.get_potion()[4] == "mana":
                self.manapoints += item_to_use.get_item()[3]
                if self.manapoints > self.max_manapoints:
                    self.manapoints = self.max_manapoints
            elif item_to_use.get_potion()[4] == "buff":
                self.damage = self.damage + item_to_use.get_potion()[3]
                self.armor = self.armor + item_to_use.get_potion()[3]
            elif item_to_use.get_potion()[4] == "poison":
                # !!! THIS NEEDS TO BE REDONE, MORE DYNAMIC AND WITHOUT A STATIC ENEMY !!!
                #self.attack(e, item_to_use.get_potion()[3])
                pass
            self.remove_item(item_to_use)
            return "Item successfully used!"
        else:
            return "This item cannot be used!"

    # equips an item (if the item can be equipped)
    def equip_item(self, item_to_equip):
        if item_to_equip.is_equippable == True:
            if item_to_equip.get_item()[4] == "melee" or item_to_equip.get_item()[4] == "ranged":
                self.damage = item_to_equip.get_item()[3]
                self.equipped_weapon = item_to_equip
            elif item_to_equip.__class__.__name__ == "armor":
                self.armor = item_to_equip.get_item()[3]
                self.equipped_armor = item_to_equip
            elif item_to_equip.__class__.__name__ == "arrow":
                self.equipped_arrow = item_to_equip
            return "Item successfully equipped!"
        else:
            return "This item cannot be equipped!"

    # unequips an item
    def unequip_item(self, item_to_unequip):
        if self.equipped_weapon == item_to_unequip or self.equipped_armor == item_to_unequip:
            if item_to_unequip.__class__.__name__ == "weapon":
                self.damage = 1
                self.equipped_weapon = None
            elif item_to_unequip.__class__.__name__ == "armor":
                self.armor = 0
                self.equipped_armor = None
            return "Item successfully unequipped"
        else:
            return "This item cannot be unequipped"
    
    def learn_spell(self, spell_to_learn):
        if self.level < spell_to_learn.get_spell()[6]:
            return "You need to be at least level {} to learn this spell.".format(spell_to_learn.get_spell()[6])
        elif spell_to_learn in self.known_spells:
            return "Spell already known"
        else:
            # there is no limit for known spells per level yet (maybe there never will, as it can be regulated by the number of spells available)
            self.known_spells.append(spell_to_learn)




class player(character):
    def __init__(self, name, maxhp, maxmp, race=None, _class=None, dmg=1, arm=0, is_enemy=False):
        super().__init__(name, maxhp, maxmp, race, _class, dmg, arm)

    # only the player can get xp
    '''
    level formula: 100*level**2 - 100*level
    lvl 1   0
    lvl 2   200
    lvl 3   600
    lvl 4   1200
    and so on
    '''

    # grants the character xp for level progression
    # sources can be: killing an NPC (including enemies) or completing quests
    # only needed if there will be parties available
    def get_xp(self, amount):
        self.xp += amount
        if self.xp >= (100 * ((self.level+1)**2) - (100*(self.level+1))):
            # can maybe resolved better, in order that the xp alert appears before the level-up alert, but works for now
            print(self.level_up())
        return "{} xp recieved!".format(amount)
    
    def level_up(self):
        self.level += 1
        # the levelling of the character attributes still must be implemented properly
        self.max_hitpoints = self.max_hitpoints + self.level * 10
        self.max_manapoints = self.max_manapoints + self.level * 5
        # still needs to be decided if hp and mana will be restored upon levelup
        self.hitpoints = self.max_hitpoints
        self.manapoints = self.max_manapoints
        # if there will be point-buy, then this is obsolete
        self.strength += 1
        self.dexterity += 1
        self.intelligence += 1
        # either dependant on strength or a fixed value
        self.max_carry_weight = self.max_carry_weight + self.strength * 5

        return "Level up!"
    
    def death(self):
        # either respawn at a ckeckpoint and reset xp progress OR
        # load last savegame
        '''
        # reset level progress
        self.xp = (100 * (self.level**2) - (100*self.level))

        return "You died! Respawn?
        '''
        return "You died! Load last save?"
    
    def show_intentory(self):
        print('---WEAPONS---')
        for item in self.inventory[1]:
            print(item.get_item())
        
        print('---ARMOR---')
        for item in self.inventory[3]:
            print(item.get_item())
        
        print('---POTIONS---')
        for item in self.inventory[5]:
            print(item.get_item())
    


''' TEST AREA '''


p = player("Main Character", 100, 50, 1, 0)
e = character("Dark Knight", 80, 50, 10)

p.add_item(items.iron_sword)
p.add_item(items.chain_armor)
p.add_item(items.small_health_potion)
p.add_item(items.iron_axe)

print(p.inventory)

p.show_intentory()



'''
e.add_item(items.iron_axe)
e.add_item(items.plate_armor)
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

p.add_item(items.stone_arrow)
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

'''
# Game Loop
while True:
    # Main Menu
    while True:
        print(text.menu['main menu'])
        keyPress = input()
        if keyPress == 's' or keyPress == 'S':
            break
        else:
            exit()
    
    # Character Creation
    # Name
    while True:
        global playerName
        print(text.menu['name'])
        playerName = input()
        break

    # Race
    while True:
        global playerRace

        print(text.menu['race'])
        keyPress = input()

        if keyPress == 'h' or keyPress == 'H':
            playerRace = 'Human'
            break
        elif keyPress == 'e' or keyPress == 'E':
            playerRace = 'Elf'
            break
        elif keyPress == 'd' or keyPress == 'D':
            playerRace = 'Dwarf'
            break
        elif keyPress == 'o' or keyPress == 'O':
            playerRace = 'Orc'
            break
        else:
            print('Please input a valid character')
    
    # Class
    while True:
        global playerClass

        print(text.menu['class'])
        keyPress = input()

        if keyPress == 'w' or keyPress == 'W':
            playerClass = 'Warrior'
            break
        elif keyPress == 'r' or keyPress == 'R':
            playerClass = 'Rogue'
            break
        elif keyPress == 'm' or keyPress == 'M':
            playerClass = 'Mage'
            break
        else:
            print('Please input a valid character')

    while True:
        print(text.menu['confirm'], playerRace, playerClass, 'named', playerName + '?')
        print(text.menu['continue'])
        keyPress = input()
        if keyPress == 'y' or keyPress == 'Y':
            break
        else:
            exit()  # needs to be replaced later

    # create the player instance
    playerCharacter = player(playerName, 100, 50, playerRace, playerClass)
    print(playerCharacter.__dict__['name'], playerCharacter.race, playerCharacter._class)

    # Start the story
    print(text.prologue['intro'])

'''