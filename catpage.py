"""Main program that takes all modules and converts into a page"""
import sys
from pagecontents import *
import pyperclip

@logfunc
def ID_input(prompt: str = '') -> int:
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
            if sys.argv[1] == '-s': Options.table = True
            elif sys.argv[1] == '-c': Options.catfruit = True
            elif sys.argv[1] == '-w': Options.wiki = True
            elif sys.argv[1] == '-t': Options.talents = True
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

@logfunc
def main(unit_ID = 0) -> str:
    """FIXME: very messy, must clean"""
    ID = unit_ID if unit_ID else ID_input("Enter unit ID/Name: ")
    cat = Cat(ID)
    cats = cat.getData()
    rarity = cat.getRarity()
    names = cat.getNames()
    gacha = cat.getGacha()
    drops = cat.isDrop()
    talents = cat.getTalents()
    for k in range(len(cats) if len(cats) != 2 else quit(f"{names[1]} has no page.")):
        try:
            for n in range(len(cats[0])):
                try:
                    cats[k][n] = int(cats[k][n])
                    if n == 7: cats[k][7] = round((cats[k][7] * 2) / 30, 2)
                except IndexError:
                    continue
        except ValueError:
            continue
    anims = [get_atkfreq(cats[0]), get_atkfreq(cats[1]),
             get_atkfreq(cats[2]) if cat.trueForm else 100,
             get_backswing(ID, 'f', cats[0]), get_backswing(ID, 'c', cats[1]),
             get_backswing(ID, 's', cats[2]) if cat.trueForm else 0]

    # 0-2 attack frequency, 3-5 backswing
    for i in range(3):
        if cats[i][4] == 0: anims[i] = anims[i] + anims[i + 3] + 1
        cats[i][4] = anims[i]
        cats[i][7] = f"{cats[i][7]} ~ {round(cats[i][7] - 8.8, 2) if cats[i][7] > 10.8 else 2} seconds"
        cats[i][12] = "Single Target" if cats[i][12] == 0 else "Area Attack"
    if Options.table: return get_tables(cats, anims, names, rarity)
    elif Options.catfruit:
        if get_catfruit(rarity[8]): return get_catfruit(rarity[8]).strip('\n')
        else: quit(f"{names[1]} has no catfruit evolution.")
    elif Options.talents:
        if talents: return get_talent(get_talents(talents, cats[2])).strip('\n')
        else: quit(f"{names[1]} has no talents.")
    else: return get_start(ID, rarity, names, cats, gacha, drops) \
           + get_translation(ID, rarity, names, cat.getDesc()) + get_cost(cats, cat.catRarity) \
           + get_tables(cats, anims, names, rarity) + get_catfruit(rarity[8])\
           + get_talent(get_talents(talents, cats[2])) \
           + get_end(ID, rarity[7]) + get_categories(cats, rarity, gacha, drops, names, talents)


if __name__ == "__main__":
    with open("log.txt", "w") as f:
        pass
    pyperclip.copy(main())
    print(pyperclip.paste())
    # print(main())