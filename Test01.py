'''
This file contains several snippets to test different functionalities within python and is only used to look up things.
'''

'''
Test with class properties

class Spam(object):
    def __init__(self, description, value):
        self.description = description
        self.value = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, d):
        if not d:
            raise Exception("description cannot be empty")
        self._description = d


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        if not (v > 0):
            raise Exception("value must be greater than zero")
        self._value = v
'''

'''
#ABC = Abstract Base Class
from abc import ABC, abstractmethod

class parent(ABC):

    @abstractmethod
    def test_method(self):
        pass

class child(parent):
    def test_method(self, text):
        self.text = text

test1 = child()
test1.test_method("HELLO")

print(test1.text)
'''
'''
def print_kwargs(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

print_kwargs(id_1=10, id_2="Hello World")

def add(*args):
    ans = 1
    for elem in args:
        ans = ans * elem
    print(ans)

add(2, 3, 4)
add(1, 4)
add(1, 2, 3, 4, 5)

def mean(*args):
    avg = 0
    for i in args:
        avg += i
    avg /= len(args)
    return avg

print(mean(10, 5, 45, 30))
'''

''' LIST COMPREHENSION AND LAMBDA AND OTHER USEFUL STUFF
squares = [i**2 for i in range(11)]
print(squares)


x = lambda a, b: a * b
print(x(4, 5))

test = lambda x: x > 1
print(test(1)); print(test(1.3))


colors = ["red", "blue", "green", "yellow"]
firetruck, water, leaf, sun, = colors

print(colors, firetruck, water, leaf, sun)


supplies = ['pens', 'staplers', 'flamethrowers', 'binders']

for index, item in enumerate(supplies):
    print(index, ":", item)
'''

''' DECORATORS
class Celsius:

    def __init__(self, temperature = 0):
        self.__temperature = temperature
    
    def to_fahrenheit(self):
        return (self.__temperature * 1.8) + 32

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273.15:
            raise ValueError("Temperature below -273,15.")
        self.__temperature = value


test_object = Celsius(15)
print(test_object.to_fahrenheit())
print(test_object.__dict__)

test_object.__temperature = 45
print(test_object.__temperature)
'''

''' NUMBER GUESSING GAME
import random

secretNumber = random.randint(1, 20)

print("Please guess my number!")

#player has 6 tries
for guesses in range(1, 5):
    guess = int(input("Please make a guess:"))

    if guess < secretNumber:
        print("Your guess is too low!")
    elif guess > secretNumber:
        print("Your guess is too high!")
    else:
        break

if guess == secretNumber:
    print("You found my number in ", guesses, "guesses!")
else:
    print("Sorry, you didnt find the secret number!")
'''

'''
# Rock, Paper, Scissors
import random, sys, time

wins = 0
losses = 0
ties = 0

# game loop
while True:
    print("Wins: {}, Losses: {}, Ties: {}".format(wins, losses, ties))

    # Player input loop
    while True:
    
        keyPress = input("Enter your move: (r)ock, (p)aper, (s)cissors or (q)uit: ")
        if keyPress == "q":
            sys.exit()
        elif keyPress == "r" or keyPress == "p" or keyPress == "s":
            break
        print("Please input either q, r, p or s.")

    if keyPress == "r":
        print("ROCK versus ... ", end="")
    elif keyPress == "p":
        print("PAPER versus ... ", end="")
    elif keyPress == "s":
        print("SCISSORS versus ... ", end="")

    randNumber = random.randint(1, 3)
    if randNumber == 1:
        computerMove = "r"
        print("ROCK")
    elif randNumber == 2:
        computerMove = "p"
        print("PAPER")
    elif randNumber == 3:
        computerMove = "s"
        print("SCISSORS")
    
    if keyPress == computerMove:
        print("It's a tie!")
        ties += 1
    elif keyPress == "r" and computerMove == "p":
        print("You loose!")
        losses += 1
    elif keyPress == "r" and computerMove == "s":
        print("You win!")
        wins += 1
    elif keyPress == "p" and computerMove == "s":
        print("You loose!")
        losses += 1
    elif keyPress == "p" and computerMove == "r":
        print("You win!")
        wins += 1
    elif keyPress == "s" and computerMove == "r":
        print("You loose!")
        losses += 1
    elif keyPress == "s" and computerMove == "p":
        print("You win!")
        wins += 1
'''

'''
import sys, time

intendation = 0
intendateUp = True

try:
    while True:
        
        if intendateUp == True:
            print(' ' * intendation + '+-+-+-+-+')
            intendation += 1
            time.sleep(0.1)

            if intendation == 20:
                intendateUp = False
        else:
            print(' ' * intendation + '+-+-+-+-+')
            intendation -= 1
            time.sleep(0.1)

            if intendation == 0:
                intendateUp = True
except KeyboardInterrupt:
    sys.exit()
'''

'''
# DnD Dice Sim

import random, tkinter as tk
from tkinter import scrolledtext

root = tk.Tk()
root.geometry('700x700')
root.title('DnD Dice Simulator')

def dice4():
    textBox.insert(tk.INSERT, '\nRolling D4: {}'.format(random.randint(1, 4)))

def dice6():
    textBox.insert(tk.INSERT, '\nRolling D6: {}'.format(random.randint(1, 6)))

def dice8():
    textBox.insert(tk.INSERT, '\nRolling D8: {}'.format(random.randint(1, 8)))

def dice10():
    textBox.insert(tk.INSERT, '\nRolling D10: {}'.format(random.randint(1, 10)))

def dice12():
    textBox.insert(tk.INSERT, '\nRolling D12: {}'.format(random.randint(1, 12)))

def dice20():
    textBox.insert(tk.INSERT, '\nRolling D20: {}'.format(random.randint(1, 20)))


btn4 = tk.Button(root, text='D4', command=dice4)
btn4.grid(column=0, row=2)
btn6 = tk.Button(root, text='D6', command=dice6)
btn6.grid(column=1, row=2)
btn8 = tk.Button(root, text='D8', command=dice8)
btn8.grid(column=2, row=2)
btn10 = tk.Button(root, text='D10', command=dice10)
btn10.grid(column=3, row=2)
btn12 = tk.Button(root, text='D12', command=dice12)
btn12.grid(column=4, row=2)
btn20 = tk.Button(root, text='D20', command=dice20)
btn20.grid(column=5, row=2)
textBox = scrolledtext.ScrolledText(root, width=30, height=30)
textBox.insert(tk.INSERT, 'Your Dice rolls appear here')
textBox.grid(column=0, row=3)

root.mainloop()
'''

'''
numbers = [sum(x for x in range(1,11))]
numbers_sum = sum(t for t in numbers)
print(numbers)
print(numbers_sum)
'''

'''
colors = ["red", "blue", "green", "yellow"]
firetruck, water, leaf, sun, = colors

print(colors, firetruck, water, leaf, sun)

numbers = [1, 2]

a = b = 5
print(a, b)
'''

'''
fname = 'Bob'
lname = 'Smith'

print('My name is {} {}.'.format(fname, lname))
print(f'My name is {fname} {lname}.')
'''