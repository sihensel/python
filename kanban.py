#!/usr/bin/env python3

'''
todo-app that uses the kanban principle

currrently not using curses.wrapper(), the corresponding parts are commented out

Features to add:
- config file
- encryption of saved files
'''

import sys
import traceback
import json
from datetime import datetime

# windows:
# python -m pip install windows-curses
import curses


''' DEFINE KEYBINDINGS HERE '''
vim = False     # set vim-keybindings

# check config file for custom key bindings first
if vim:
    # redo this
    CMD_LOAD_FILE = 'e'  # edit
    CMD_HELP = 'l'  # list ???
    CMD_UP = 'k'
    CMD_DOWN = 'j'
    CMD_LEFT = 'h'
    CMD_RIGHT = 'l'
    CMD_INSERT = 'i'
    CMD_DELETE = 'x'
    CMD_SAVE = 'w'
    CMD_QUIT = 'q'
else:
    CMD_QUIT = 'q'
    CMD_READ = 'r'
    CMD_WRITE = 'w'
    #CMD_UP = 'KEY_UP'
    #CMD_DOWN = 'KEY_DOWN'
    #CMD_LEFT = 'KEY_LEFT'
    #CMD_RIGHT = 'KEY_RIGHT'
    CMD_ADD = 'a'
    CMD_DELETE = 'd'
    CMD_SAVE = 's'

#is_window = False

class kanban:
    def __init__(self): #, title):
        #self.title = title
        self.data = {}
        self.backlog = []
        self.inProgress = []
        self.done = []
        self.file_path = 'curses-test.json'
        self.vim = False


    # read from JSON file
    def read_file(self, filepath='curses-test.json'):

        with open(filepath, 'r') as file:
            self.data = json.load(file)
            self.backlog = self.data['backlog']
            self.inProgress = self.data['inProgress']
            self.done = self.data['done']
            self.vim = self.data['vim']
        
    # write data to JSON file
    def write_file(self):
        # sort first
        self.sort()

        self.data['backlog'] = self.backlog
        self.data['inProgress'] = self.inProgress
        self.data['done'] = self.done
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

# ------------------ CURSES ----------------------

    def main(self):
        #curses.wrapper(self.set_screen)
        #curses.wrapper(self.init_screen)

        self.stdscr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

        try:
            self.init_screen()
        except:
            # exception handler here
            traceback.print_exc()
        finally:
            self.stdscr.keypad(False)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            #sys.exit()

    def init_screen(self):  #, stdscr):

        #self.stdscr = stdscr

        self.height, self.width = self.stdscr.getmaxyx()

        # draw screen
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, '---KANBAN PLANNING TOOL---', curses.A_BOLD)
        #self.stdscr.addstr(1, 0, f'Please enter a command (\'{CMD_HELP}\' for help, \'{CMD_QUIT}\' to quit).')
        self.stdscr.addstr(0, 1, f'height: {self.height}, width: {self.width}')
        self.stdscr.addstr(self.height -1, 0, f'({CMD_QUIT})uit | ({CMD_READ})ead file | ({CMD_WRITE})rite to file | ({CMD_ADD})dd task | ({CMD_DELETE})elete task')
        self.stdscr.refresh()
#        self.stdscr.getkey()

        cmd = None
        while cmd not in ['q', 'Q']:
            cmd = self.stdscr.getkey()
            
            if cmd == CMD_READ:
                self.read_file()
            elif cmd == 't':
                self.new_show()
            #else:
            #    continue

    def display_help(self):#, stdscr):
        # display help permanently later
        
        self.stdscr.addstr(3, 0, f'{CMD_HELP} - add new task')
        self.stdscr.addstr(4, 0, f'{CMD_DELETE} - delete selected task')
        self.stdscr.addstr(5, 0, f'{CMD_SAVE} - save kanban list to file')
        self.stdscr.addstr(6, 0, f'{CMD_QUIT} - quit')
        self.stdscr.addstr(8, 0, 'Press any key to continue...')
        self.stdscr.refresh()
        self.stdscr.getkey()

        self.init_screen()
        #curses.wrapper(self.init_screen)

    def new_show(self):
        # make size of board dependent on longest list later
        self.board = curses.newwin(25, 75, 3, 0)
        self.board.border()
        #self.board.addstr(0, 0, self.backlog[0]['task'])   # don't forget to read file first!
        self.board.addstr(1, 2, 'BACKLOG | IN PROGRESS | DONE')
        self.board.refresh()



''' LABS KEY TESTING AREA '''

if __name__ == '__main__':

    # curses.wrapper(main)

    testlist = kanban()
    testlist.main()
    print(testlist.data)
    #print(testlist.backlog)
    #print(testlist.inProgress)
    #print(testlist.done)

# -----------------------------------------
# MAKE THIS EOF LATER !!!


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
