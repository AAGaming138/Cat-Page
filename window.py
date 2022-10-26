from tkinter import *
from catpage import *
import pyperclip

def on_click(mode):
    Label(root, text="\t" * 5).grid(row=4,column=1)
    try:
        ID = int(e.get())
    except ValueError:
        ID = get_ID(e.get().lower())
    page = main(ID, mode)
    if len(page) > 10:
        warning = False
        if mode == 0: message = "Page"
        elif mode == 1: message = "Stats"
        elif mode == 2: message = "Catfruit"
        elif mode == 3: message = "Talents"
        elif mode == 4: message = "Preview"
        elif mode == 5: message = "Categories"
        pyperclip.copy(page)
    else:
        warning = True
        if page == "error1": message = "Enter a valid name or ID!"
        elif page == "error2": message = f"\"{Cat(ID).getNames()[1]}\" has no catfruits"
        elif page == "error3": message = f"\"{Cat(ID).getNames()[1]}\" has no talents"
        elif page == "error4": message = f"\"{Cat(ID).getNames()[1]}\" has no page"
    lab = Label(root, text=message if warning else message + " copied to clipboard",
                fg="red" if warning else "black")
    lab.grid(row=4, column=1)
    root.after(3000, lab.destroy)


def temp_text(a):
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
root.geometry("550x140")
root.resizable(False, False)
root.title('Cat Page')
# end window

# start input field
e = Entry(root, width=50, border=3)
e.grid(row=0, column=1, padx=10, pady=10)
e.insert(0, "Enter cat name or ID")
e.bind("<FocusIn>", temp_text)
# end input field

# start radiobuttons
option = IntVar()
option.set(0)
rb = lambda t, v, r, c: Radiobutton(root, text=t, justify="left", anchor="w",
            variable=option, value=v).grid(sticky = W, row=r, column=c, padx=5)
rb("Whole Page", 0, 2, 0)
rb("Stats Only", 1, 3, 0)
rb("Catfruit Only", 2, 4, 0)
rb("Talents Only", 3, 2, 2)
rb("Preview Only", 4, 3, 2)
rb("Category Only", 5, 4, 2)
# end radiobuttons

# start button
myButton = Button(root, text="Get", command=lambda: on_click(option.get()), padx=20)
myButton.grid(row=2, column=1, padx=10, pady=1)
# end button

root.mainloop()








