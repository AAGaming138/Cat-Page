"""Main application to generate a GUI"""

from tkinter import *
from MakePage import *
from WikiReader import *
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
                         anchor="w", variable=option,
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
        self.add_button("Whole Page", 6, 2, 0)
        self.add_button("Stats Only", 7, 3, 0)
        self.add_button("Desc Only", 8, 4, 0)


    def get_enemy_buttons_RIGHT(self):
        """Adds left enemy buttons"""
        self.add_button("Encounters", 9, 2, 2)
        self.add_button("Category Only", 10, 3, 2)
        checkbox = Checkbutton(self, text="Increment", justify="left",
                               anchor="w", variable=check,
                               onvalue=2, offvalue=0)
        checkbox.grid(sticky=W, row=4, column=2, padx=4)
        toolTip = ToolTip(checkbox)

        def enter(event):
            toolTip.showtip('Adds 2 to the enemy ID, as\n'
                            'shown on the Enemy Release Order.\n'
                            'Incompatible with name search.')
        def leave(event):
            toolTip.hidetip()

        checkbox.bind('<Enter>', enter)
        checkbox.bind('<Leave>', leave)

        self.buttons.append(checkbox)


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


class ToolTip(object):
    '''
    https://stackoverflow.com/questions/20399243
    '''
    def __init__(self, widget):
        self.text = None
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 57
        y += cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def show_page(p):
    """Displays page to output box"""
    if not err: pyperclip.copy(p)
    # automatically copy if module exists
    combo.config(width=520, height=150)
    # change output box size
    root.geometry("550x280")
    # increases window size
    combo.delete()
    # resets output box
    combo.insert(p)
    # inserts provided output


def conf_text(t, fg = "black"):
    lab = Label(root, text=t, fg=fg)
    # get label
    lab.grid(row=4, column=1)
    # remove label after 3 seconds
    root.after(3000, lab.destroy)


def on_click(mode, che):
    """Function that is called once button is clicked"""
    Label(root, text="\t" * 5).grid(row=4,column=1)

    if enemy_mode.get():
        try:
            try:
                ID = int(e.get().strip())
            except ValueError:
                if check.get():
                    raise NoDataError("Increment", '')
                else:
                    ID = StatsCommon(True).get_ID(e.get().strip())
            warning = False
            page = MakeEnemyPage(ID - check.get(), mode).get_page()
            message = ["Page", "Stats", "Description", "Encounters",
                       "Categories"][mode - 6]
            show_page(page)
        except NoDataError as error:
            warning = True
            message = error
    else:
        try:
            ID = int(e.get().strip())
        except ValueError:
            ID = StatsCommon().get_ID(e.get().strip())
        try:
            page = MakeCatPage(ID, mode).get_page()
            warning = False
            message = ["Page", "Stats", "Cost", "Catfruit",
                       "Talents", "Categories"][mode]
            show_page(page)

        except NoDataError as error:
            # i.e. if page is unsuccessfully retrieved
            warning = True
            message = error

    conf_text(message if warning else message + \
           (" copied to clipboard" if not err else " retrieved successfully"),
              fg="red" if warning else "black")


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


def ent(default):
    e.delete(0, 'end') # remove prompt
    e.select_clear()
    e.insert(0, default) # add prompt
    e.bind("<FocusIn>", temp_text) # delete text upon click


def cat_options():
    """Changes program to cat mode"""
    with open("mode.txt", "w") as f1:
        f1.write("CAT")
    enemy_mode.set(False)
    root.title('Cat Page')
    num.set(num.get() + 1)

    option.set(0) # default selection
    root.iconbitmap(DIR + "/catIcon.ico")

    ent("Enter cat name or ID")

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
    with open("mode.txt", "w") as f2:
        f2.write("ENEMY")
    enemy_mode.set(True)
    root.title('Enemy Page')
    num.set(num.get() + 1)

    option.set(6) # default selection
    root.iconbitmap(DIR + "/dogeIcon.ico") # change icon

    ent("Enter enemy name or ID")

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


def update_names():
    cat_name = WikiReader("Module:Cats/names.csv")
    enemy_name = WikiReader("Module:Enemies.csv")
    cat_name.readNames()
    conf_text(enemy_name.readNames())


def update_stage_names():
    stage_names = WikiReader("User:TheWWRNerdGuy/data/StageNames.csv")
    conf_text(stage_names.readStageNames())


# start window
root = Tk()
with open("mode.txt", "r") as f:
    m = f.read()
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
updatemenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="Mode", menu=filemenu)
filemenu.add_command(label="Enemy Page", command=enemy_options)

menubar.add_cascade(label="Themes", menu=thememenu)
thememenu.add_command(label="Vista", command=vista_theme)
thememenu.add_command(label="Winnative", command=winnative_theme)
thememenu.add_command(label="Xpnative", command=xpnative_theme)

menubar.add_cascade(label="Update", menu=updatemenu)
updatemenu.add_command(label="Update Names", command=update_names)
updatemenu.add_command(label="Update Stage Names", command=update_stage_names)

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

# start checkboxes
check = IntVar()
check.set(0)
# end checkboxes

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

if m == "CAT": cat_options()
else: enemy_options()
# end cat page

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