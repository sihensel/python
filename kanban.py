'''
todo-app that uses a kanban principle

There will be 3 areas:
    - backlog
    - in progress
    - done

Features to add:
- config file
- load from file and save changes (json/clear text)
- encryption of saved files?
'''

import curses
import sys

'''
def main(stdscr):
    pass

curses.wrapper(main)
'''

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

is_window = False

testlist = [{'task': 'GPM M3', 'due': '18.02.2021'}, {'task': 'ReWe Bericht', 'due': '20.02.2021'}]

# initialize screen
stdscr = curses.initscr()

# set tui parameters
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

height, width = stdscr.getmaxyx()
if height < 50 or width < 50:
    quit()


def initialize():

    global height, width
    stdscr.clear()
    stdscr.addstr(0, 0, '---KANBAN PLANNING TOOL---', curses.A_BOLD)
    stdscr.addstr(1, 0, f'Please enter a command (\'{CMD_HELP}\' for help, \'{CMD_QUIT}\' to quit).')
    stdscr.addstr(height -1, 0,  'STATUS BAR')
    stdscr.refresh()

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


#Start program
initialize()

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


# maybe not use classes, only functions
# maybe implement a buffer system like vim
class kanban:
    def __init__(self, title):
        
        self.backlog = []
        self.inProgress = []
        self.done = []
        
        self.title = title

    # add a task to the backlog
    def add_task(self, task, due):
        self.backlog.append({'task': task, 'due': due})


    # mark a task as in progress
    def move_progress(self, index):
        self.inProgress.append(self.backlog[index])
        self.backlog.pop(index)


    # mark a task as done and move it to the done list
    def move_done(self, index):
        self.done.append(self.inProgress[index])
        self.inProgress.pop(index)


    # sort the tasks taks by date
    def sort(self):
        sorted_list = sorted(self.backlog, key=lambda k: k['due'])
        self.backlog = sorted_list

        sorted_list = sorted(self.inProgress, key=lambda k: k['due'])
        self.inProgress = sorted_list

        sorted_list = sorted(self.done, key=lambda k: k['due'])
        self.done = sorted_list

    # show the whole list
    def show(self):

        self.sort()

        max = len(self.backlog)
        if len(self.inProgress) > max:
            max = len(self.inProgress)
        if len(self.done) > max:
            max = len(self.done)
        
        max_len = 11
        if self.backlog:        # if that returns true, the list  exists and contains items
            for i in range(0, len(self.backlog)):
                if len(self.backlog[i]['task']) > max_len:
                    max_len = len(self.backlog[i]['task'])
                
        if self.inProgress:
            for i in range(0, len(self.inProgress)):
                if len(self.inProgress[i]['task']) > max_len:
                    max_len = len(self.inProgress[i]['task'])

        if self.done:
            for i in range(0, len(self.done)):
                if len(self.done[i]['task']) > max_len:
                    max_len = len(self.done[i]['task'])

        print('BACKLOG' + (max_len - 7) * ' ', '| IN PROGRESS' + (max_len - 11) * ' ',  '| DONE' + (max_len - 4) * ' ')
        print((max_len * 3 + 6) * '-')
        for i in range(0, max):
            if i >= len(self.backlog):
                p_backlog = '-' + (max_len - 1) * ' '
            else:
                p_backlog = self.backlog[i]['task'] + (max_len - len(self.backlog[i]['task'])) * ' '
            
            if i >= len(self.inProgress):
                p_inProgress = '-' + (max_len - 1) * ' '
            else:
                p_inProgress = self.inProgress[i]['task'] + (max_len - len(self.inProgress[i]['task'])) * ' '

            if i >= len(self.done):
                p_done = '-' + (max_len - 1) * ' '
            else:
                p_done = self.done[i]['task'] + (max_len - len(self.done[i]['task'])) * ' '

            print(f'{p_backlog} | {p_inProgress} | {p_done}')
        
        print((max_len * 3 + 6) * '-')
        

''' LABS KEY TESTING AREA '''
'''
list1 = kanban('ToDo List 1')

list1.add_task('SK Kolloquium', '09.02.2021')
list1.add_task('Rewe Kolloquium', '02.02.2021')
list1.add_task('GPM M3', '07.02.2021')

list1.show()

print(' ')

list1.move_progress(0)
list1.move_progress(1)
list1.move_done(1)
list1.show()
'''