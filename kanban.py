#!/usr/bin/env python3

'''
todo-app that uses a kanban principle

There will be 3 areas:
    - backlog
    - in progress
    - done

Features to add:
- config file
- encryption of saved files
'''

import curses
import json
from datetime import datetime
import sys


''' DEFINE KEYBINDINGS HERE '''
vim = False     # set vim-keybindings

# check config file for custom key bindings first
if vim:
    CMD_LOAD_FILE = 'e'  # edit
    CMD_HELP = 'l'  # list ???
    CMD_UP = 'k'
    CMD_DOWN = 'j'
    CMD_LEFT = 'h'
    CMD_RIGHT = 'l'
    CMD_INSERT = 'i'
    CMD_DELETE = 'd'
    CMD_SAVE = 'w'
    CMD_QUIT = 'q'
else:
    CMD_LOAD_FILE = 'o'
    CMD_HELP = 'h'
    CMD_UP = 'KEY_UP'
    CMD_DOWN = 'KEY_DOWN'
    CMD_LEFT = 'KEY_LEFT'
    CMD_RIGHT = 'KEY_RIGHT'
    CMD_INSERT = 'i'
    CMD_INSERT_BELOW = 'o'
    CMD_INSERT_ABOVE = 'O'
    CMD_DELETE = 'x'
    CMD_SAVE = 's'
    CMD_QUIT = 'q'

#is_window = False

class kanban:
    def __init__(self): #, title):
        #self.title = title
        self.data = {}
        self.backlog = []
        self.inProgress = []
        self.done = []
        self.file_path = '/home/simon/python/curses-test.json'

    # read from JSON file
    def read_file(self):

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)
            self.backlog, self.inProgress, self.done = self.data[
                'backlog'], self.data['inProgress'], self.data['done']

    # write data to JSON file
    def write_file(self):

        self.sort()

        self.data['backlog'], self.data['inProgress'], self.data['done'] = self.backlog, self.inProgress, self.done
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file)

    # add a task to the backlog
    def add_task(self, task, due):

        try:
            datetime.strptime(due, '%d.%m.%Y')
        except ValueError:
            raise ValueError('Date must have format "dd.mm.yyyy"')
        else:
            # maybe remove the for-loop later
            for i in self.backlog:
                if task in i['task']:
                    print('It is advised to choose a distinct name!')
                    break
            self.backlog.append({'task': str(task), 'due': due})

    # move a task from the backlog to inProgress
    # TO INDEX THESE ENTRIES, ADD A NUMBER IN FRONT OF EACH ROW SO THE USER CAN INPUT THIS NUMBER
    def move_progress(self, index):

        self.inProgress.append(self.backlog[index])
        self.backlog.pop(index)

    # move a task from inProgress to the done list
    def move_done(self, index):

        self.done.append(self.inProgress[index])
        self.inProgress.pop(index)

    # sort the tasks by date
    def sort(self):

        self.backlog.sort(key=lambda x: datetime.strptime(x['due'], '%d.%m.%Y'))
        self.inProgress.sort(key=lambda x: datetime.strptime(x['due'], '%d.%m.%Y'))
        self.done.sort(key=lambda x: datetime.strptime(x['due'], '%d.%m.%Y'))

    # show the whole list
    def show(self):

        self.sort()

        # get the list with the most entries
        max = len(self.backlog)
        if len(self.inProgress) > max:
            max = len(self.inProgress)
        if len(self.done) > max:
            max = len(self.done)

        # get the longest string of all lists (default: 'In Progress')
        max_len = 11
        if self.backlog:
            for i in range(len(self.backlog)):
                if len(self.backlog[i]['task']) > max_len:
                    max_len = len(self.backlog[i]['task'])

        if self.inProgress:
            for i in range(len(self.inProgress)):
                if len(self.inProgress[i]['task']) > max_len:
                    max_len = len(self.inProgress[i]['task'])

        if self.done:
            for i in range(len(self.done)):
                if len(self.done[i]['task']) > max_len:
                    max_len = len(self.done[i]['task'])
        
        # start the output
        # print -: 3 * the max_len to cover all cloumns + 6 for the seperators
        print((max_len * 3 + 6)*'-')
        # print spaces minus the len of the headings
        print('BACKLOG', (max_len - 8)* ' ', '| IN PROGRESS' , (max_len - 12)* ' ', '| DONE', (max_len - 3)* ' ')
        print((max_len * 3 + 6)*'-')

        for i in range(max):
            if i >= len(self.backlog):
                p_backlog = '-' + (max_len - 1)* ' '
            else:
                p_backlog = self.backlog[i]['task'] + (max_len - len(self.backlog[i]['task']))* ' '

            if i >= len(self.inProgress):
                p_inProgress = '-' + (max_len - 1)* ' '
            else:
                p_inProgress = self.inProgress[i]['task'] + (max_len - len(self.inProgress[i]['task']))* ' '

            if i >= len(self.done):
                p_done = '-' + (max_len - 1)* ' '
            else:
                p_done = self.done[i]['task'] + (max_len - len(self.done[i]['task']))* ' '

            print(f'{p_backlog} | {p_inProgress} | {p_done}')

        print((max_len * 3 + 6)* '-')


''' LABS KEY TESTING AREA '''

obj1 = kanban()
obj1.read_file()
#obj1.add_task('do_sth_else', '03.01.1998')
# obj1.move_progress(1)
# obj1.move_done(0)

obj1.show()
# obj1.write_file()
# print(obj1.data)


def main(stdscr):

    # remove later, this is just so intellisense dsplays the documentation
    #stdscr = curses.initscr()
    tasklist = kanban()
    tasklist.read_file()

    height, width = stdscr.getmaxyx()
    if height < 50 or width < 50:
        print('Your terminal is too small, please resize it.')
        sys.exit()
    
    def initialize():
        stdscr.clear()
        stdscr.refresh()
        stdscr.addstr(0, 0, '---KANBAN PLANNING TOOL---', curses.A_BOLD)
        stdscr.addstr(1, 0, f'Please enter a command (\'{CMD_HELP}\' for help, \'{CMD_QUIT}\' to quit).')
        stdscr.addstr(2, 0, tasklist.backlog[0]['task'])
        stdscr.addstr(height -1, 0,  'STATUS BAR')
        stdscr.refresh()

    def display_help():
        stdscr.addstr(3, 0, f'{CMD_HELP} - add new task')
        stdscr.addstr(4, 0, f'{CMD_DELETE} - delete selected task')
        stdscr.addstr(5, 0, f'{CMD_SAVE} - save kanban list to file')
        stdscr.addstr(6, 0, f'{CMD_QUIT} - quit')
        stdscr.addstr(8, 0, 'Press any key to continue...')
        stdscr.refresh()
        stdscr.getkey()

        initialize()

    
    initialize()
    cmd = None
    # ord() returns the unicode of a caracter
    # chr() returns the caracter matching a unicode
    # stdscr.getch() returns the unicode of a pressed character
    while (cmd != 'q'):
        cmd = stdscr.getkey()

        if cmd == CMD_HELP:
            display_help()

        elif cmd == CMD_RIGHT:
            pass
        else:
            continue
    sys.exit()


if __name__ == '__main__':
    curses.wrapper(main)

# -----------------------------------------
# MAKE THIS EOF LATER !!!

'''
# initialize screen
stdscr = curses.initscr()

# set tui parameters
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

'''

'''
def initialize():

    stdscr.clear()
    stdscr.addstr(0, 0, '---KANBAN PLANNING TOOL---', curses.A_BOLD)
    stdscr.addstr(
        1, 0, f'Please enter a command (\'{CMD_HELP}\' for help, \'{CMD_QUIT}\' to quit).')
    #stdscr.addstr(height -1, 0,  'STATUS BAR')
    stdscr.refresh()

    wait_input()


def wait_input():
    cmd = None
    # ord() returns the unicode of a caracter
    # chr() returns the caracter matching a unicode
    # stdscr.getch() returns the unicode of a pressed character
    while (cmd != 'q'):
        cmd = stdscr.getkey()

        if cmd == CMD_HELP:
            display_help()
        elif cmd == 'b':
            generate_board()
        elif cmd == CMD_RIGHT:
            display_help()
        elif cmd == 'g':
            gen_kanban()
        else:
            continue

    quit_program()


def display_help():

    # if a window is displayed, clear the screen first
    if is_window:
        stdscr.clear()
        initialize()

    stdscr.addstr(3, 0, f'{CMD_HELP} - add new task')
    stdscr.addstr(4, 0, f'{CMD_DELETE} - delete selected task')
    stdscr.addstr(5, 0, f'{CMD_SAVE} - save kanban list to file')
    stdscr.addstr(6, 0, f'{CMD_QUIT} - quit')
    stdscr.addstr(8, 0, 'Press a key to continue...')
    stdscr.refresh()
    stdscr.getkey()

    # remove later
    initialize()


def quit_program():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(False)

    curses.endwin()
    sys.exit()


def generate_board():
    global is_window

    if is_window:
        stdscr.clear()
        initialize()   # remove later

    board = curses.newwin(50, 100, 3, 0)
    board.addstr(0, 0, 'Hello from 0,0')
    board.addstr(4, 4, 'Hello from 4,4')
    board.addstr(5, 5, 'Hello from 5,15 with a long string')
    board.refresh()

    is_window = True


def gen_kanban():
    global is_window

    if is_window:
        stdscr.clear()
        initialize()   # remove later

    board = curses.newwin(50, 100, 3, 0)    # (rows, cols, start-y, start-x)
    board.addstr(0, 0, 'BACKLOG | IN PROGRESS | DONE')
    board.addstr(1, 0, 10 * '-')
    board.refresh()

    for i in range(0, len(testlist)):
        board.addstr(i + 2, 0, f'{testlist[i]["task"]} | - | - ')
        board.refresh()

    board.refresh()

    is_window = True


def main():
    pass

#if __name__ == '__main__':
#    curses.wrapper(main)
'''
