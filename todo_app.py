
# ToDo App (prob. CLI-based)

class todo_list:
    def __init__(self, title):
        self.title = title
        self.tasklist = []
    
    def add_task(self, text, is_complete=False):
        self.tasklist.append(task(text, is_complete))
    
    def remove_task(self, index):
        self.tasklist.remove(self.tasklist[index])
    
    def set_complete(self, index):
        self.tasklist[index].is_complete = True
    
    def set_uncomplete(self, index):
        self.tasklist[index].is_complete = False
    
    # removes all completed tasks
    def clean(self):
        # [:] allows to modify the list in place, as you iterate on a slice
        for item in self.tasklist[:]:
            if item.is_complete == True:
                self.tasklist.remove(item)
        #self.tasklist[:] = [x for x in self.tasklist if x.is_complete == False]
    
    def output(self):
        print(self.title)
        for item in self.tasklist:
            if item.is_complete == True:
                print('-', item.text, '|', 'complete')
            else:
                print('-', item.text, '|', 'not complete')

class task:
    def __init__(self, text, is_complete=False):
        self.text = text
        self.is_complete = is_complete

class note:
    def __init__(self, title, text=''):
        self.title = title
        self.text = text
    
    def edit_note(self, text):
        self.text += text
    
    def clear_note(self):
        self.text = ''
    
    def output(self):
        print(self.title)
        print(self.text)




''' Test Area '''

a = note('quotes', 'I came, I saw, I conquered')
a.edit_note('\nI think, therefore I am')
a.output()

b = todo_list('Personal Todo List')
b.add_task('walk the dog')
b.add_task('get groceries')
b.output()