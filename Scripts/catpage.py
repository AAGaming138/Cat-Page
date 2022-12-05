"""Program that takes all modules and converts into a page"""
import sys
from Page import *

def ID_input(op: Options, prompt: str = '') -> int:
    """Gets ID input from either console or terminal"""
    if len(sys.argv) == 2:
        if sys.argv[1][0] == '-': quit("Enter an ID/Name.", False)
        inp = sys.argv[1]
    elif len(sys.argv) > 2:
        if sys.argv[1][0] != '-':
            inp = ' '.join(sys.argv[1:])
        else:
            # if there exists a flag
            inp = ' '.join(sys.argv[2:])
            if sys.argv[1] == '-s': op.table = True
            elif sys.argv[1] == '-c': op.catfruit = True
            elif sys.argv[1] == '-w': op.preview = True
            elif sys.argv[1] == '-t': op.talents = True
            elif sys.argv[1] == '-C': op.category = True
            else: quit("Enter a valid flag.", False)
    else:
        inp = input(prompt)
        if inp == '': quit("Enter an ID/Name.", False)
    try:
        ID = int(inp)
    except ValueError:
        inp = inp.lower().strip(" ")
        ID = get_ID(inp)
        if ID == -1: quit("Enter a valid unit ID or name.")
    return ID


def get_page(unit_ID = None, mode = 0) -> str:
    """FIXME: very messy, must clean"""
    op = Options()
    ID = unit_ID if unit_ID is not None else ID_input(op, "Enter unit ID/Name: ")
    page = Page(ID)

    # gets cat object from ID

    if page.ID == -1: return "error1"
    cats = page.getData()
    if len(cats) < 3: return "error4"
    tals = page.tals

    if mode == 1: op.table = True
    elif mode == 2: op.cost = True
    elif mode == 3: op.catfruit = True
    elif mode == 4: op.talents = True
    elif mode == 5: op.category = True
    # output options

    # process the cat.getData() list
    for k in range(len(cats) if len(cats) != 2 else quit(f"{page.names[1]} has no page.")):
        try:
            for n in range(len(cats[0])):
                try:
                    cats[k][n] = int(cats[k][n])
                    if n == 7: cats[k][7] = round((cats[k][7] * 2) / 30, 2)
                except IndexError:
                    continue
        except ValueError:
            continue
    # get attack animation for cat
    anims = [get_atkfreq(cats[0]), get_atkfreq(cats[1]),
             get_atkfreq(cats[2]) if page.tf else 100,
             get_backswing(ID, 'f', cats[0]), get_backswing(ID, 'c', cats[1]),
             get_backswing(ID, 's', cats[2]) if page.tf else 0]
    # 0-2 attack frequency, 3-5 backswing

    # parse cat data list to
    for i in range(3):
        if cats[i][4] == 0: anims[i] = anims[i] + anims[i + 3] + 1
        cats[i][4] = anims[i]
        cats[i][7] = f"{cats[i][7]} ~ {round(cats[i][7] - 8.8, 2) if cats[i][7] > 10.8 else 2} seconds"
        cats[i][12] = "Single Target" if cats[i][12] == 0 else "Area Attack"

    # returns depending on option
    if op.table: return page.getTables(anims)

    elif op.cost: return page.getCost().strip("\n")

    elif op.catfruit:
        if page.getCatfruit(): return page.getCatfruit().strip('\n')
        else: return "error2"

    elif op.talents:
        if tals: return page.getTalent(get_talents(tals, cats[2])).strip('\n')

        # FIXME - Literally not going to understand this a few days from now
        # This is what happens when you write 3 functions that
        # sound exactly the same from left to right:
        # if Cat.getTalents: return
        # Page.getTalent(stats.get_talents(Cat.getTalents, Cat.getData)) etc.

        else: return "error3"

    elif op.category:
        return page.getCategories()

    else: return page.getStart() + page.getTranslation() + page.getCost() + \
                 page.getTables(anims) + page.getCatfruit() + \
                 page.getTalent(get_talents(tals, cats[2])) + page.getEnd() +\
                 page.getCategories()

# TODO: - Simplify the spaghetti
#       - Update ID_input()
#       - Turn this into a class?!?!?!