"""Main application to generate a GUI"""

from EnemyPage import EnemyPage
from tkinter import *
from MakeCatPage import *
import tkinter.ttk as ttk

try:
    import pyperclip
    err = False
except ModuleNotFoundError:
    err = True


class Buttons(ttk.Frame):
    """Class that generates the radio buttons of unit"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = []


    def add_button(self, label, value, row, col, state = 1):
        """Adds button to buttons list and frame"""
        rb = Radiobutton(self, text=label, justify="left",
                         borderwidth=2, anchor="w", variable=option,
                         value=value, state=(NORMAL if state else DISABLED))
        rb.grid(sticky=W, row=row, column=col, padx=5)
        self.buttons.append(rb)


    def get_cat_buttons_LEFT(self):
        """Adds left cat buttons"""
        self.add_button("Whole Page", 0, 2, 0)
        self.add_button("Stats Only", 1, 3, 0)
        self.add_button("Cost Only", 2, 4, 0)


    def get_cat_buttons_RIGHT(self):
        """Adds right cat buttons"""
        self.add_button("Catfruit Only", 3, 2, 2)
        self.add_button("Talents Only", 4, 3, 2)
        self.add_button("Category Only", 5, 4, 2)


    def get_enemy_buttons_LEFT(self):
        """Adds left enemy buttons"""
        self.add_button("Whole Page", 6, 2, 0, 0)
        self.add_button("Stats Only", 7, 3, 0)
        self.add_button("Desc Only", 8, 4, 0, 0)


    def get_enemy_buttons_RIGHT(self):
        """Adds left enemy buttons"""
        self.add_button("Encounters", 9, 2, 2, 0)
        self.add_button("Category Only", 10, 3, 2, 0)


    def remove_buttons(self):
        """Removes all buttons"""
        for button in self.buttons:
            button.grid_forget()


class TextScrollCombo(ttk.Frame):
    """Class that generates a scrollable textbox"""
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

    # ensure a consistent GUI size
        self.grid_propagate(False)
    # implement stretchability
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = Text(self)
        self.txt.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    # create a Scrollbar and associate it with txt
        scrollb = ttk.Scrollbar(self, command=self.txt.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        self.txt['yscrollcommand'] = scrollb.set

    def insert(self, text):
        """insert() method from Text class"""
        self.txt.insert(END, text)

    def delete(self):
        """delete() method from Text class"""
        self.txt.delete('1.0', END)


def on_click(mode, che):
    """Function that is called once button is clicked"""
    Label(root, text="\t" * 5).grid(row=4,column=1)

    try:
        ID = int(e.get())
    except ValueError:
        ID = StatsCommon(enemy_mode.get()).get_ID(e.get().lower())
    # gets the ID

    if enemy_mode.get():
        enem = EnemyPage(ID)
        page = enem.getTables()
        if not err: pyperclip.copy(page)
        # automatically copy if module exists
        combo.config(width=520, height=150)
        # change output box size
        root.geometry("550x280")
        # increases window size
        combo.delete()
        # resets output box
        combo.insert(page)
        # inserts provided output
    else:
        if che == 0:
            try:
                page = MakeCatPage(ID, mode).get_page()
                # i.e. if page is successfully retrieved
                warning = False
                message = ["Page", "Stats", "Cost", "Catfruit",
                           "Talents", "Categories"][mode]
                if not err: pyperclip.copy(page)
                # automatically copy if module exists
                combo.config(width=520, height=150)
                # change output box size
                root.geometry("550x280")
                # increases window size
                combo.delete()
                # resets output box
                combo.insert(page)
                # inserts provided output
            except NoDataError as error:
                # i.e. if page is unsuccessfully retrieved
                warning = True
                message = error
            lab = Label(root, text=message if warning else message + \
                   (" copied to clipboard" if not err else " retrieved successfully"),
                        fg="red" if warning else "black")
            # get label
            lab.grid(row=4, column=1)
            # remove label after 3 seconds
            root.after(3000, lab.destroy)

        else:
            for i in range(len(Cat(0).catNames)):
                try:
                    MakeCatPage(i, mode).get_page()
                except NoDataError:
                    combo.insert(f"Error occurred for unit {i:03}")


def change_focus(event):
    """Removes focus from input field"""
    event.widget.focus_set()

def temp_text(a):
    """Removes temporary text once input field is clicked"""
    e.delete(0, "end")

def center(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def cat_options():
    """Changes program to cat mode"""
    enemy_mode.set(False)
    root.title('Cat Page')
    root.iconbitmap(DIR + "/catIcon.ico")
    num.set(num.get() + 1)

    option.set(0) # default selection
    e.delete(0, 'end') # remove prompt
    e.select_clear()
    e.insert(0, "Enter cat name or ID") # add prompt
    e.bind("<FocusIn>", temp_text) # delete text upon click

    if num.get() > 1:
        filemenu.add_command(label="Enemy Page", command=enemy_options)
    try:
        filemenu.delete("Cat Page")
    except TclError:
        pass

    radiobuttons_LEFT.remove_buttons()
    radiobuttons_RIGHT.remove_buttons()
    radiobuttons_LEFT.get_cat_buttons_LEFT()
    radiobuttons_RIGHT.get_cat_buttons_RIGHT()


def enemy_options():
    """Changes program to enemy mode"""
    enemy_mode.set(True)
    root.title('Enemy Page')

    option.set(7) # default selection
    root.iconbitmap(DIR + "/dogeIcon.ico") # change icon

    e.delete(0, 'end')
    e.select_clear()
    e.insert(0, "Enter enemy name or ID") # change input prompt

    e.bind("<FocusIn>", temp_text)

    filemenu.add_command(label="Cat Page", command=cat_options)
    filemenu.delete("Enemy Page")

    radiobuttons_LEFT.remove_buttons()
    radiobuttons_RIGHT.remove_buttons()
    radiobuttons_LEFT.get_enemy_buttons_LEFT()
    radiobuttons_RIGHT.get_enemy_buttons_RIGHT()


def vista_theme():
    style.theme_use('vista')

def winnative_theme():
    style.theme_use('winnative')

def xpnative_theme():
    style.theme_use('xpnative')


# start window
root = Tk()
root.iconbitmap(DIR + "/catIcon.ico")
root.attributes('-alpha', 0.0)
center(root)
root.attributes('-alpha', 1.0)
root.geometry("550x200")
root.resizable(False, False)
root.title('Cat Page')
# end window

# start menu
enemy_mode = BooleanVar()
enemy_mode.set(False)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
thememenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Enemy Page", command=enemy_options)

menubar.add_cascade(label="Themes", menu=thememenu)
thememenu.add_command(label="Vista", command=vista_theme)
thememenu.add_command(label="Winnative", command=winnative_theme)
thememenu.add_command(label="Xpnative", command=xpnative_theme)
root.config(menu=menubar)
# end menu

# start input field
e = Entry(root, width=50, border=3)
e.grid(row=0, column=1, padx=10, pady=10)
e.insert(0, "Enter cat name or ID")
e.bind("<FocusIn>", temp_text)
# end input field

# start output box
combo = TextScrollCombo(root)
combo.insert("Output appears here")
combo.grid(row=5, column=0, columnspan=3)
combo.config(width=315, height=45)

combo.txt.config(undo=True)
combo.txt.config(borderwidth=3, relief="sunken")

# end output box

# start cat page
option = IntVar()
option.set(0)

radiobuttons_LEFT = Buttons(root)
radiobuttons_RIGHT = Buttons(root)
radiobuttons_LEFT.grid(row=2, column=0, rowspan=3)
radiobuttons_RIGHT.grid(row=2, column=2, rowspan=3)

style = ttk.Style()
style.theme_use('winnative')

num = IntVar()
num.set(0)

cat_options()
# end cat page

# start checkboxes
check = IntVar()
check.set(0)
'''
debugger = Checkbutton(root, text="Debug mode", variable=check, offvalue=0, onvalue=1)
debugger.grid(sticky=W, row=5, column=2, padx=5)
'''
# end checkboxes

# start button
myButton = Button(root, text="Get",
                  command=lambda: on_click(option.get(), check.get()), padx=20)
myButton.grid(row=2, column=1, padx=10, pady=1)
# end button

if __name__ == "__main__":
    '''
    with open("log.txt", "w") as f:
        pass
    '''
    root.bind_all('<Button>', change_focus)
    root.mainloop()