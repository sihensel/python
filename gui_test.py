'''
Simple program to test some functionalities of the tkinter module
'''

# always import libraries with an alias so you know wich is your code and which is the import
import tkinter as tk
from tkinter.ttk import *
from tkinter import scrolledtext
from tkinter import messagebox
#import tkinter.messagebox as Msg # alternative with an alias
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
from tkinter import Menu


# creates the parent window
root = tk.Tk()
root.title("Hello World")
root.geometry("700x600")    # sets the size of the window in pixels

# creates label and assign text and font with size
# padx and pady add padding to any widget to make it look more organized
lbl = tk.Label(root, text = "Hello", font = ("Calibri", 30), padx = 5, pady = 5)
lbl.grid(column = 0, row = 0) # anchor the widget in the grid

def onClick():
    lbl_text = "Hello " + txt.get()
    lbl.configure(text = lbl_text)

# creates a clickable button, assigns a text and sets back and foreground colors
btn = tk.Button(root, text = "Click Me!", bg = "orange", fg = "black", command = onClick)
btn.grid(column = 2, row = 0)

# creates input field (state = "disabled" disables the field)
txt = tk.Entry(root, text = "Enter your name", state = "normal")
txt.grid(column = 1, row = 0)
txt.focus()

# creates a combobox (dropdown), uses the tkinter.ttk import
combo = Combobox(root)
# assign values to the combobox
combo["values"] = (1, 2, 3, 4, 5, "Text")
# select value from the value pool (combo.get() returns teh current value)
combo.current(5)
combo.grid(column = 0, row = 1)

# defines a tkinter variable (BooleanVar() is a tkinter class)
check_state = tk.BooleanVar()
check_state.set(True) # sets the initial status of the checkbox

''' instead of BooleanVar() you can use IntVar() and set it to 0 and 1
ckeck_state = IntVar()
check_state.set(0) # uncheck / False
check_state.set(1) # check / True
'''

# creates a checkbox and assigns the boolean variable to it
check = Checkbutton(root, text = "Checkbox", var = check_state)
check.grid(column = 0, row = 2)

def rad_click():
    rad1.configure(text = "First clicked")

def btn_click():
    # shows a messagebox with the current selected value
    messagebox.showinfo("Message Title", selected.get())
    '''
    messagebox.showwarning("Message Title", selected.get())
    messagebox.showerror("Message Title", selected.get())
    messagebox.askokcancel("Message Title", selected.get())
    messagebox.askquestion("Message Title", selected.get())
    messagebox.askretrycancel("Message Title", selected.get())
    messagebox.askyesno("Message Title", selected.get())
    messagebox.askyesnocancel("Message Title", selected.get())
    '''

# create tkinter variable
selected = tk.IntVar()
#creates radiobuttons, each radio must have its own value, command is as usual
'''rad1 = tk.Radiobutton(root, text = "First", value = 1, command = rad_click)'''
rad1 = tk.Radiobutton(root, text ="First", value = 1, variable = selected)
rad2 = tk.Radiobutton(root, text = "Second", value = 2, variable = selected)
rad3 = tk.Radiobutton(root, text = "Third", value = 3, variable = selected)

btn1 = tk.Button(root, text = "Click Me!", command = btn_click)

rad1.grid(column = 0, row = 3)
rad2.grid(column = 0, row = 4)
rad3.grid(column = 0, row = 5)
btn1.grid(column = 1, row = 3)

# creates a text field(scrolledText) with properties
scr_text = scrolledtext.ScrolledText(root, width = 40, height = 10)
scr_text.insert(tk.INSERT, "Insert your text here")
#scr_text.delete(1.0, tk.END) # method to delete the text from the text area

scr_text.grid(column = 0, row = 6)

txt_var = tk.IntVar()
txt_var.set(4)
#spin = tk.Spinbox(root, from_ = 0, to = 10, width = 5) # sets values from 0 to 10
#spin = tk.Spinbox(root, values = (3, 8, 11), width = 5) # uses predefied values
# creates a spin box which uses a variable for ist default value
spin = tk.Spinbox(root, from_ = 0, to = 10, width = 5, textvariable = txt_var)
spin.grid(column = 0, row = 7)

# defines a black style for the progressbar
style = ttk.Style()
style.theme_use("default")
style.configure("black.Horizontal.TProgressbar", background = "black")

# creates a progressbar with the previously defined style
bar = Progressbar(root, length = 200, style = "black.Horizontal.TProgressbar")
bar["value"] = 50
bar.grid(column = 0, row = 8)

# calls a file dialog to open a file
#file = tk.filedialog.askopenfile() # variable hold the path to the selected file
#files = tk.filedialog.askopenfilenames() # if you have more than one file
#dir = tk.filedialog.askdirectory()
#messagebox.showinfo("Title", file)

# creates a menu
menu = tk.Menu(root)
# creates items as part of the menu
new_item = Menu(menu, tearoff = 0) # tearoff = 0 removes the ability to use the menu in its own window
new_item.add_command(label = "New...")  #command = menu_clicked
new_item.add_separator()
new_item.add_command(label = "Edit")
# add items to the menu
menu.add_cascade(label = "File", menu = new_item)
root.config(menu = menu) # adds the menu as the menu of the root-window

''' adds a Notebook framework
tab_control = ttk.Notebook(root)
# creates tabs for the notebook
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
# assigsn titles to the tabs
tab_control.add(tab1, text = "First")
tab_control.add(tab2, text = "Second")
# creates labels and assigns them to the tabs
lbl1 = tk.Label(tab1, text = Label 1")
lbl1.grid(column = 0, row = 0)
lbl2 = tk.Label(tab2, text = "Label2")
lbl2.grid(column = 0, row = 0)
# assigns the notebook to the root-window
tab_control.pack(expand = 1, fill = "both")
'''
root.mainloop()