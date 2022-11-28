"""Main application to generate a GUI"""
from tkinter import *
from catpage import *
import tkinter.ttk as ttk

try:
    import pyperclip
    err = False
except ModuleNotFoundError:
    err = True

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


def on_click(mode):
    """Function that is called once button is clicked"""
    Label(root, text="\t" * 5).grid(row=4,column=1)
    try:
        ID = int(e.get())
    except ValueError:
        ID = get_ID(e.get().lower())
    # gets the ID

    page = get_page(ID, mode)

    if len(page) > 10:
        # i.e. if page is successfully retrieved
        warning = False
        message = ["Page", "Stats", "Cost", "Catfruit", "Talents", "Categories"][mode]
        if not err: pyperclip.copy(page) # automatically copy if module exists
        combo.config(width=520, height=150) # change output box size
        root.geometry("550x280") # increases window size
        combo.delete() # resets output box
        combo.insert(page) # inserts provided output
    else:
        # i.e. if page is unsuccessfully retrieved
        warning = True
        if page == "error1": message = "Enter a valid name or ID!"
        elif page == "error2": message = f"\"{Cat(ID).getNames()[1]}\" has no catfruits"
        elif page == "error3": message = f"\"{Cat(ID).getNames()[1]}\" has no talents"
        elif page == "error4": message = f"\"{Cat(ID).getNames()[1]}\" has no page"
    lab = Label(root, text=message if warning else message + \
          (" copied to clipboard" if not err else " retrieved successfully")
          ,fg="red" if warning else "black")
    # get label
    lab.grid(row=4, column=1)
    # remove label after 3 seconds
    root.after(3000, lab.destroy)


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


# start window
root = Tk()
root.iconbitmap(DIR + "/catIcon.ico")
root.attributes('-alpha', 0.0)
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)
center(root)
root.attributes('-alpha', 1.0)
root.geometry("550x180")
root.resizable(False, False)
root.title('Cat Page')
# end window

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

style = ttk.Style()
style.theme_use('clam')
# end output box

# start radiobuttons
option = IntVar()
option.set(0)
rb = lambda t, v, r, c: Radiobutton(root, text=t, justify="left", anchor="w",
            variable=option, value=v).grid(sticky = W, row=r, column=c, padx=5)
rb("Whole Page", 0, 2, 0)
rb("Stats Only", 1, 3, 0)
rb("Cost Only", 2, 4, 0)
rb("Catfruit Only", 3, 2, 2)
rb("Talents Only", 4, 3, 2)
rb("Category Only", 5, 4, 2)
# end radiobuttons

# start button
myButton = Button(root, text="Get", command=lambda: on_click(option.get()), padx=20)
myButton.grid(row=2, column=1, padx=10, pady=1)
# end button

if __name__ == "__main__":
    '''
    with open("log.txt", "w") as f:
        pass
    '''
    root.mainloop()