"""Collection of functions that returns cat stats"""
from common import *
from Cat import Cat

def get_ID(name: str) -> int:
    """
    :param name: unit name
    :return: unit ID if name exists, otherwise -1
    """
    if not name: return -1
    names = opencsv("names.csv", header=True)
    for i in range(len(names)):
        names[i] = [x.lower() for x in names[i]]
        if name in names[i]: return int(names[i][0])
        else: continue
    return -1


def get_backswing(ID: int, form: str, ls: list) -> int:
    """
    :param ID: Unit ID
    :param form: Normal, Evolved, or True form
    :param ls: list of normal/evolved/true form
    :return: total attack frames, which is pre + post attack
    """
    try:
        anim_file = opencsv(f"{data_mines}/ImageDataLocal/{ID:03}_{form}02.maanim", header=True)
    except FileNotFoundError:
        return 44
        # Note: 44 is the default backswing for eggs
    frame = 0
    for i in range(len(anim_file)):
        if len(anim_file[i]) != 4: anim_file[i] = [0, 0, 0, 0]
            # any list of 4 numbers are actual animation data, so this
            # bit basically discards everything that is not 4 numbers
            # then turns it into a dummy list of 4 numbers to be interpreted
        else:
            for j in range(4):
                anim_file[i][j] = int(anim_file[i][j])
        if anim_file[i][0] > frame: frame = anim_file[i][0]
            # frame is simply the largest number of the 4 numbered list, which
            # is the last frame before restarting the attack animation

    # frame + 1 is the entire attack, ls[13] is the foreswing
    return frame + 1 - ls[13]


def get_atkfreq(ls: list) -> int:
    """
    :param ls: normal, evolved, or true data values
    :return: the value given
    """
    # Note: ls[4] is the tba/2
    tba = ls[4] * 2
    if tba != 0:
        try:
            if ls[59] != 0: atkfreq = tba + (ls[62] if ls[60] != 0 else ls[61])
                # if multi-hit
            else: atkfreq = tba + ls[13]
        except IndexError:
            atkfreq = tba + ls[13]
        # if not multi-hit, it's just tba + foreswing
    else: atkfreq = ls[13]
        # if tba is 0, it's foreswing + backswing
    return atkfreq - 1
    # subtract 1 since atkfreq also accounts for the attacking frame
    # which should be instantaneous


def get_abilities(ls: list, mode: int) -> str:
    """
    :param ls: form list
    :param mode: 0 for Cat Stats, 1 for Calcstatstable, 2 for Performance
    :return: string of list of abilities
    """
    try:
        ls[107] = int(re.sub('[^0-9]', '', str(ls[107])))
        # why ponos why
    except IndexError:
        pass

    def list_has(index: int) -> bool:
        """Checks if list contains a valid index"""
        try:
            int(ls[index])
        except (IndexError, ValueError):
            return False
        else:
            return ls[index] != 0

    def LD_range() -> str:
        """Checks for different LD ranges"""
        if list_has(44) and list_has(99) and not list_has(102):
            if ls[101] > 0:
                return f" on 1st hit, {ls[100]:,}~{ls[100] + ls[101]:,} on 2nd hit"
            else:
                return f" on 1st hit, {ls[100] + ls[101]:,}~{ls[100]:,} on 2nd hit"
            # long distance multiple range hits
        elif list_has(44) and list_has(99) and list_has(102):
            if ls[104] > 0:
                return f" on 1st hit, {ls[100]:,}~{ls[100] + ls[101]:,} on 2nd hit, {ls[103]:,}~" \
                       f"{ls[103] + ls[104]:,} at 3rd hit"
            else:
                return f" on 1st hit, {ls[100] + ls[101]:,}~{ls[100]:,} on 2nd hit, {ls[103] + ls[104]:,}~" \
                       f"{ls[103]:,} at 3rd hit"
            # omni strike multiple range hits
        else:
            return ''

    def multab() -> str:
        """Checks for abilities on different hits during multi-hit"""
        if list_has(64) and not (list_has(63) or list_has(65)): return " on 2nd hit"
        elif list_has(65) and not (list_has(63) or list_has(64)): return " on 3rd hit"
        elif list_has(64) and list_has(65) and not list_has(63): return " on 2nd and 3rd hits"
        elif list_has(59) and list_has(63) and not (list_has(64) or list_has(65)): return " on 1st hit"
        else: return ""

    sec = lambda i: round(ls[i] / 30, 2)
    ftrait = ''
    traits = []
    abilities = []
    immunities = []
    addt = lambda t: traits.append(f"[[:Category:{t} Enemies|{t}]]")
    if list_has(10): addt("Red")
    if list_has(16): addt("Floating")
    if list_has(17): addt("Black")
    if list_has(18): addt("Metal")
    if list_has(19): addt("Traitless")
    if list_has(20): addt("Angel")
    if list_has(21): addt("Alien")
    if list_has(22): addt("Zombie")
    if list_has(78): addt("Relic")
    if list_has(96): addt("Aku")
    # for all the traits

    if len(traits) == 1:
        ftrait = traits[0]
    elif 1 < len(traits) < 9:
        traits[-1] = f"and {traits[-1]}"
        ftrait = f"{', 'if len(traits) > 2 else ' '}".join(traits)
    elif len(traits) == 9:
        if ls[18] == 0: ftrait = "non-[[:Category:Metal Enemies|Metal]]"
        elif ls[19] == 0: ftrait = "traited"
    else:
        ftrait = "all"
    # self-explanatory

    addim = lambda im: \
        immunities.append(f"[[Special Abilities#Immune to {im}|{'Immune to ' if len(immunities) == 0 else ''}{im}]]")
    # Note: addim does not work with Evade Surge and Warp Blocker or if mode is 2
    abil = lambda ab, dis = '': f"[[Special Abilities#{ab}|{ab if not dis else dis}]]"
    # Note: if the display link is the same as actual link, then print rest of link
    pl = lambda ind: 's' if ls[ind] != 30 else ''
    # Note: this is for pluralising 'second' specifically
    if mode == 0:
        if list_has(59): abilities.append(f"{abil('Multi-Hit')} ({ls[3] * 17:,} at {ls[13]}f <sup>{sec(13)}s</sup>,"
            f" {ls[59] * 17:,} at {ls[61]}f <sup>{sec(61)}s</sup>"
            f"{f', {ls[60] * 17:,} at {ls[62]}f <sup>{sec(62)}s</sup>' if ls[60] != 0 else ''})")
        if list_has(44) and ls[45] > 0:
            abilities.append(f"{abil('Long Distance')} (Effective range: {ls[44]:,}~{ls[44] + ls[45]:,}{LD_range()})")
        elif list_has(44) and ls[45] <= 0:
            abilities.append(f"{abil('Omni Strike')} (Effective range: {ls[44] + ls[45]:,}~{ls[44]:,}{LD_range()})")
        if list_has(23): abilities.append(f"{abil('Strong Against', 'Strong')} against {ftrait} enemies "
                                          f"(Deals 1.5x damage, only takes 1/2 damage)")
        if list_has(24): abilities.append(
            f"{ls[24]}% chance to {abil('Knockback', 'knockback')} {ftrait} enemies{multab()}")
        if list_has(25): abilities.append( f"{ls[25]}% chance to {abil('Freeze', 'freeze')} {ftrait} enemies for "
                                           f"{ls[26]}f <sub>{sec(26)} second{pl(26)}</sub>{multab()}")
        if list_has(27): abilities.append(f"{ls[27]}% chance to {abil('Slow', 'slow')} {ftrait} enemies for {ls[28]}f "
            f"<sub>{sec(28)} second{pl(28)}</sub>{multab()}")
        if list_has(29): abilities.append(f"{abil('Resistant')} to {ftrait} enemies")
        if list_has(30): abilities.append(f"Deals {abil('Massive Damage', 'massive damage')} to {ftrait} enemies")
        if list_has(31): abilities.append(f"{ls[31]}% chance to perform a {abil('Critical', 'critical hit')}{multab()}")
        if list_has(32): abilities.append(f"{abil('Attacks Only', 'Attacks only')} {ftrait} enemies")
        if list_has(33): abilities.append(
            f"{abil('Extra Money', 'Double money')} gained when defeating enemies{multab()}")
        if list_has(34): abilities.append(abil('Base Destroyer'))
        if list_has(35): abilities.append(
            f"{ls[35]}% chance to create a level {ls[36]} [["
            f"{'Wave Attack' if len(ls) < 95 or ls[94] != 1 else 'Wave Attack#Mini-Wave|Mini-Wave'}]]{multab()}")
        if list_has(37): abilities.append(
            f"{ls[37]}% chance to {abil('Weaken', 'weaken')} {ftrait} enemies to {ls[39]}% for {ls[38]}f"
            f" <sub>{sec(38)} second{pl(38)}</sub>{multab()}")
        if list_has(40): abilities.append(f"{abil('Strengthen', 'Strengthens')} by {ls[41]}% at {ls[40]}% health")
        if list_has(42): abilities.append(f"{ls[42]}% chance to {abil('Survive', 'survive')} a lethal strike")
        if list_has(43): abilities.append(abil('Metal'))
        if list_has(47): abilities.append(abil('Wave Shield'))
        # 'regular' abilities
        if list_has(46): addim("Waves")
        if list_has(48): addim("Knockback")
        if list_has(49): addim("Freeze")
        if list_has(50): addim("Slow")
        if list_has(51): addim("Weaken")
        # immunities
        if list_has(52): abilities.append(
            f"{abil('Zombie Killer')} (stops [[:Category:Zombie Enemies|Zombies]] from reviving)")
        if list_has(53): abilities.append(f"{abil('Witch Killer')} (Deals 5x damage to "
                                         f"[[:Category:Witch Enemies|Witches]], only takes 1/10 damage)")
        if list_has(70): abilities.append(
            f"{ls[70]}% chance to {abil('Barrier Breaker', 'break')} {abil('Barrier', 'barriers')}{multab()}")
        if list_has(75): immunities.append(
            f"[[Special Abilities#Warp Blocker|{'Immune to ' if len(immunities) == 0 else ''}Warp]]")
        if list_has(77): abilities.append(f"{abil('Eva Angel Killer')} (Deals 5x damage "
                                         "to [[:Category:Eva Angel Enemies|Eva Angels]], only takes 1/5 damage)")
        if list_has(79): addim("Curse")
        if list_has(80): abilities.append(f"{abil('Insanely Tough', 'Insanely tough')} against {ftrait} enemies")
        if list_has(81): abilities.append(f"Deals {abil('Insane Damage', 'insane damage')} to {ftrait} enemies")
        if list_has(82): abilities.append(f"{ls[82]}% chance to land a {abil('Savage Blow', 'savage blow')}, dealing "
                                          f"3x damage to non-[[:Category:Metal Enemies|Metal]] enemies{multab()}")
        if list_has(84): abilities.append(
            f"{ls[84]}% chance to {abil('Dodge Attack', 'dodge attacks')} from {ftrait} enemies for "
            f"{ls[85]}f <sub>{sec(85)} second{pl(85)}</sub>")
        if list_has(86): abilities.append(
            f"{ls[86]}% chance to create a level {ls[89]} [[Surge Attack]] between {int(ls[87] / 4):,} and "
            f"{int(ls[87] / 4) + int(ls[88] / 4):,} range{multab()}")
        if list_has(90): addim("Toxic")
        if list_has(91): immunities.append(
            f"[[Special Abilities#Evade Surge|{'Immune to ' if len(immunities) == 0 else ''}Surge]]")
        if list_has(92): abilities.append(
            f"{ls[92]}% chance to {abil('Curse', 'curse')} {ftrait} enemies for {ls[93]}f <sub>"
            f"{sec(93)} second{pl(93)}</sub>{multab()}")
        if list_has(95): abilities.append(
            f"{ls[95]}% chance to instantly {abil('Shield Piercing', 'pierce')} {abil('Shield', 'shields')}{multab()}")
        if list_has(97): abilities.append(f"{abil('Colossus Slayer',)} (Deals 1.6x damage to "
            f"[[:Category:Colossal Enemies|Colossal]] enemies, only takes 0.7x damage)")
        if list_has(98): abilities.append(f"{abil('Soulstrike')}")
        if list_has(105): abilities.append(
            f"{abil('Behemoth Slayer')} ({ls[106]}% chance to dodge "
            f"[[:Category:Behemoth Enemies|Behemoth]] enemies' attacks for {ls[107]}f <sub>"
            f"{sec(107)} second{pl(107)}</sub>)")

    elif mode == 1:
        if list_has(59): abilities.append(
                f"{abil('Multi-Hit', 'Multi-Hit')} ({ls[3]:,} at {ls[13]}f, {ls[59]:,} at {ls[61]}f"
                f"{f', {ls[60]:,} at {ls[62]}f' if ls[60] else ''})")
        if list_has(44) and ls[45] > 0:
            abilities.append(
                f"{abil('Long Distance', 'Long Distance')} "
                f"(Effective range: {ls[44]:,}~{ls[44] + ls[45]:,}{LD_range()})")
        elif list_has(44) and ls[45] <= 0:
            abilities.append(
                f"{abil('Omni Strike', 'Omni Strike')} (Effective range: "
                f"{ls[44] + ls[45]:,}~{ls[44]:,}{LD_range()})")
        if list_has(23): abilities.append(f"{abil('Strong Against', 'Strong')} against {ftrait} enemies")
        if list_has(24): abilities.append(f"{abil('Knockback', 'Knockbacks')} {ftrait} enemies{multab()} ({ls[24]}%)")
        if list_has(25): abilities.append(
            f"{abil('Freeze', 'Freezes')} {ftrait} enemies for {ls[26]}f{multab()} ({ls[25]}%)")
        if list_has(27): abilities.append(
            f"{abil('Slow', 'Slows')} {ftrait} enemies for {ls[28]}f{multab()} ({ls[27]}%)")
        if list_has(29): abilities.append(f"{abil('Resistant')} to {ftrait} enemies")
        if list_has(30): abilities.append(f"Deals {abil('Massive Damage', 'massive damage')} to {ftrait} enemies")
        if list_has(31): abilities.append(f"{abil('Critical', 'Critical hit')}{multab()} ({ls[31]}%)")
        if list_has(32): abilities.append(f"{abil('Attacks Only', 'Attacks only')} {ftrait} enemies")
        if list_has(33): abilities.append(f"{abil('Extra Money', 'Extra money')} when defeating enemies{multab()}")
        if list_has(34): abilities.append(f"{abil('Base Destroyer', 'Base destroyer')}")
        if list_has(35): abilities.append(f"Creates a level {ls[36]} [[Special Abilities#"
            f"{'Wave Attack|Wave' if len(ls) < 95 or ls[94] != 1 else 'Mini-Wave|Mini-Wave'}]]{multab()} ({ls[35]}%)")
        if list_has(37): abilities.append(
            f"{abil('Weaken', 'Weakens')} {ftrait} enemies to {ls[39]}% for {ls[38]}f{multab()} ({ls[37]}%)")
        if list_has(40): abilities.append(f"{abil('Strengthen', 'Strengthens')} by {ls[41]}% at {ls[40]}% health")
        if list_has(42): abilities.append(f"{abil('Survive', 'Survives')} a lethal strike ({ls[42]}%)")
        if list_has(43): abilities.append(abil('Metal'))
        if list_has(47): abilities.append(abil('Wave Shield'))
        if list_has(46): addim("Waves")
        if list_has(48): addim("Knockback")
        if list_has(49): addim("Freeze")
        if list_has(50): addim("Slow")
        if list_has(51): addim("Weaken")
        if list_has(52): abilities.append(abil('Zombie Killer'))
        if list_has(53): abilities.append(abil('Witch Killer'))
        if list_has(70): abilities.append(f"{abil('Barrier Breaker')} ({ls[70]}%)")
        if list_has(75): immunities.append(
                f"[[Special Abilities#Warp Blocker|Warp{' Blocker' if len(immunities) == 0 else ''}]]")
        if list_has(77): abilities.append(f"{abil('Eva Angel Killer', 'Eva Angel Killer')}")
        if list_has(79): addim("Curse")
        if list_has(80): abilities.append(f"{abil('Insanely Tough', 'Insanely tough')} against {ftrait} enemies")
        if list_has(81): abilities.append(f"Deals {abil('Insane Damage', 'insane damage')} to {ftrait} enemies")
        if list_has(82): abilities.append(f"{abil('Savage Blow', 'Savage Blow')}{multab()} ({ls[82]}%)")
        if list_has(84): abilities.append(
                f"{abil('Dodge Attack', 'Dodges')} {ftrait} enemies' attacks for {ls[85]}f ({ls[84]}%)")
        if list_has(86): abilities.append(
                f"Creates a level {ls[89]} {abil('Surge Attacks', 'Surge Attack')} between {int(ls[87] / 4):,}"
                f" and {int(ls[87] / 4) + int(ls[88] / 4):,} range{multab()} ({ls[86]}%)")
        if list_has(90): addim("Toxic")
        if list_has(91): immunities.append(
                f"[[Special Abilities#Evade Surge|{'Evade ' if len(immunities) == 0 else ''}Surge]]")
        if list_has(92): abilities.append(
                f"{abil('Curse', 'Curses')} {ftrait} enemies for {ls[93]}f{multab()} ({ls[92]}%)")
        if list_has(95): abilities.append(f"{abil('Shield Piercing', 'Shield Piercer')}{multab()} ({ls[95]}%)")
        if list_has(97): abilities.append(f"{abil('Colossus Slayer')}")
        if list_has(98): abilities.append(f"{abil('Soulstrike')}")
        if list_has(105): abilities.append(
                f"{abil('Behemoth Slayer')} (Dodges [[:Category:Behemoth Enemies|Behemoth]]"
                f" enemies' attacks for {ls[107]}f ({ls[106]}%))")

    elif mode == 2:
        pro = "'''+''' "
        con = "'''-''' "
        if list_has(23): abilities.append(
            f"{pro}{abil('Strong Against', 'Strong')} against {ftrait} enemies")
        if list_has(24): abilities.append(
            f"{pro}{ls[24]}% chance to {abil('Knockback', 'knockback')} {ftrait} enemies{multab()}")
        if list_has(25): abilities.append(
            f"{pro}{ls[25]}% chance to {abil('Freeze', 'freeze')} {ftrait} enemies "
            f"for {sec(26)} second{pl(26)}{multab()}")
        if list_has(27): abilities.append(
            f"{pro}{ls[27]}% chance to {abil('Slow', 'slow')} {ftrait} enemies for "
            f"{sec(28)} second{pl(28)}{multab()}")
        if list_has(29): abilities.append(f"{pro}{abil('Resistant')} to {ftrait} enemies")
        if list_has(30): abilities.append(f"{pro}Deals {abil('Massive Damage', 'massive damage')} to {ftrait} enemies")
        if list_has(31): abilities.append(
            f"{pro}{ls[31]}% chance to perform a {abil('Critical', 'critical hit')}{multab()}")
        if list_has(32): abilities.append(f"{con}{abil('Attacks Only', 'Attacks only')} {ftrait} enemies")
        if list_has(33): abilities.append(
            f"{pro}{abil('Extra Money', 'Double money')} gained when defeating enemies{multab()}")
        if list_has(34): abilities.append(f"{pro}{abil('Base Destroyer', 'Base destroyer')}")
        if list_has(35): abilities.append(
            f"{pro}{ls[35]}% chance to create a level {ls[36]} [["
            f"{'Wave Attack' if len(ls) < 95 or ls[94] != 1 else 'Wave Attack#Mini-Wave|Mini-Wave'}]]{multab()}")
        if list_has(37): abilities.append(
            f"{pro}{ls[37]}% chance to {abil('Weaken', 'weaken')} {ftrait} enemies to {ls[39]}% for "
            f"{sec(38)} second{pl(38)}{multab()}")
        if list_has(40): abilities.append(
            f"{pro}{abil('Strengthen', 'Strengthens')} by {ls[41]}% at {ls[40]}% health")
        if list_has(42): abilities.append(
            f"{pro}{ls[42]}% chance to {abil('Survive', 'survive')} a lethal strike")
        if list_has(43): abilities.append(f"{pro}{abil('Metal')}")
        if list_has(47): abilities.append(f"{pro}{abil('Wave Shield')}")
        if list_has(44) and ls[45] > 0:
            abilities.append(
                f"{pro}{abil('Long Distance')}"
                f" (Effective range: {ls[44]:,}~{ls[44] + ls[45]:,}{LD_range()})")
        elif list_has(44) and ls[45] <= 0:
            abilities.append(
                f"{pro}{abil('Omni Strike')}"
                f" (Effective range: {ls[44] + ls[45]:,}~{ls[44]:,}{LD_range()})")
        paddim = lambda im: \
            immunities.append(f"{pro if len(immunities) == 0 else ''}[[Special Abilities#Immune to {im}"
                              f"|{'Immune to ' if len(immunities) == 0 else ''}{im}]]")
        if list_has(46): paddim("Waves")
        if list_has(48): paddim("Knockback")
        if list_has(49): paddim("Freeze")
        if list_has(50): paddim("Slow")
        if list_has(51): paddim("Weaken")
        if list_has(52): abilities.append(f"{pro}{abil('Zombie Killer')}")
        if list_has(53): abilities.append(f"{pro}{abil('Witch Killer')}")
        if list_has(70): abilities.append(
            f"{pro}{ls[70]}% chance to {abil('Barrier Breaker', 'break')} "
            f"{abil('Barrier', 'barriers')}{multab()}")
        if list_has(75): immunities.append(
            f"{pro if len(immunities) == 0 else ''}[[Special Abilities#Warp Blocker"
            f"|{'Immune to ' if len(immunities) == 0 else ''}Warp]]")
        if list_has(77): abilities.append(f"{pro}{abil('Eva Angel Killer')}")
        if list_has(79): paddim("Curse")
        if list_has(80): abilities.append(
            f"{pro}{abil('Insanely Tough', 'Insanely tough')} against {ftrait} enemies")
        if list_has(81): abilities.append(
            f"{pro}Deals {abil('Insane Damage', 'insane damage')} to {ftrait} enemies")
        if list_has(82): abilities.append(
            f"{pro}{ls[82]}% chance to land a {abil('Savage Blow', 'savage blow')}{multab()}")
        if list_has(84): abilities.append(
            f"{pro}{ls[84]}% chance to {abil('Dodge Attack', 'dodge attacks')} from {ftrait} "
            f"enemies for {sec(85)} second{pl(85)}")
        if list_has(86): abilities.append(
            f"{pro}{ls[86]}% chance to create a level {ls[89]} [[Surge Attack]] between {int(ls[87] / 4):,} and "
            f"{int(ls[87] / 4) + int(ls[88] / 4):,} range{multab()}")
        if list_has(90): paddim("Toxic")
        if list_has(91): immunities.append(
            f"{pro if len(immunities) == 0 else ''}[[Special Abilities#Evade Surge"
            f"|{'Immune to ' if len(immunities) == 0 else ''}Surge]]")
        if list_has(92): abilities.append(
            f"{pro}{ls[92]}% chance to {abil('Curse', 'curse')} {ftrait} enemies for "
            f"{sec(93)} second{pl(93)}{multab()}")
        if list_has(95): abilities.append(
            f"{pro}{ls[95]}% chance to instantly {abil('Shield Piercing', 'pierce')} "
            f"{abil('Shield', 'shields')}{multab()}")
        if list_has(97): abilities.append(f"{pro}{abil('Colossus Slayer')}")
        if list_has(98): abilities.append(f"{abil('Soulstrike')}")
        if list_has(105): abilities.append(f"{pro}{abil('Behemoth Slayer')}")

    if len(immunities) == 1:
        abilities.append(f"{immunities[0]}")
    elif len(immunities) > 1:
        immunities[-1] = f"and {immunities[-1]}"
        abilities.append(f"{', ' if len(immunities) > 2 else ' '}".join(immunities))
    if mode == 2 and list_has(59): abilities.append(
        f"{pro if ls[3] > ls[59] else con}{abil('Multi-Hit')}")
    # deals with potentially a list of immunities
    # example: Immune to knockback, Weaken, Warp, and Curse

    if len(abilities) != 0:
        return re.sub('\.0(?![0-9])', '', '<br>\n'.join(abilities)) if mode != 2 else abilities
        # turn the list into text
    else:
        return "-" if mode != 2 else ''


def get_talents(talent_ls: list, cat_ls: list) -> list:
    """Gets talents"""
    if not talent_ls: return []
    def link(ability: str, type: str = 'default'):
        if type == 'default': l = ability
        elif type == 'res': l = "Resist"
        elif type == 'stat': l = "Stat Enhancements"
        elif type == 'tar': return f"'''Target [[:Category:{ability} Enemies|{ability}]]'''"
        else: l = type
        return f"'''[[Special Abilities#{l}|{ability}]]'''"

    talents = {
        1:  link("Weaken"),
        2:  link("Freeze"),
        3:  link("Slow"),
        6:  link("Tough Vs", "Resistant"),
        7:  link("Massive Damage"),
        8:  link("Knockback"),
        10: link("Attack Up", "Strengthen"),
        11: link("Survives", "Survive"),
        13: link("Critical"),
        14: link("Zombie Killer"),
        15: link("Barrier Breaker"),
        16: link("Money Up", "Extra Money"),
        17: link("Wave Attack"),
        18: link("Resist Weaken", "res"),
        19: link("Resist Freeze", "res"),
        20: link("Resist Slow", "res"),
        21: link("Resist Knockback", "res"),
        22: link("Resist Wave", "res"),
        25: link("Cost Down", "stat"),
        26: link("Recover Speed Up", "stat"),
        27: link("Move Speed Up", "stat"),
        29: link("Curse Immunity", "Immune to Curse"),
        30: link("Resist Curse", "res"),
        31: link("Attack Buff", "stat"),
        32: link("Defense Buff", "stat"),
        35: link("Black", "tar"),
        37: link("Angel", "tar"),
        38: link("Alien", "tar"),
        39: link("Zombie", "tar"),
        40: link("Relic", "tar"),
        44: link("Immune to Weaken"),
        45: link("Immune to Freeze"),
        46: link("Immune to Slow"),
        47: link("Immune to Knockback"),
        48: link("Immune to Waves"),
        49: link("Warp Blocker"),
        50: link("Savage Blow"),
        51: link("Dodge Attack"),
        52: link("Resist Toxic", "res"),
        53: link("Immune to Toxic"),
        54: link("Resist Surge", "res"),
        55: link("Immune to Surge", "Evade Surge"),
        56: link("Surge Attack", "Surge Attacks"),
        57: link("Aku", "tar"),
        58: link("Shield Piercing"),
        59: link("Soulstrike")
    }
    def make_talent(x: int):
        t = talent_ls[x][0]
        info = ' '
        to_int = lambda num: int(num) if int(num) == num else round(num, 2)
        gap = lambda m: to_int((t[m+1] - t[m])/(t[1] - 1))
        start = lambda s, mode = 0: f" {t[s]}{'%' if mode == 0 else mode}, improves by " if gap(s) != t[s] else " "
        maximum = lambda h, mode = '%': f" per level up to {t[h]}{'%' if mode == '%' else mode} "
        frame = lambda value: f"{value}f <sup>{round(value/30, 2)}s</sup>"

        def is_dupe(index: int):
            try:
                cat_ls[index]
            except IndexError:
                return False
            else:
                return bool(cat_ls[index])
        if t[0] == 1 and is_dupe(37): info = f": Increases weaken duration by {frame(t[4])}" \
                                          f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 1 and not is_dupe(37): info = f": Adds a {t[2]}% chance to weaken by {t[6]}% for {frame(t[4])}" \
                                                  f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 2 and is_dupe(25): info = f": Increases freeze duration by {frame(t[4])}" \
                                          f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 2 and not is_dupe(25): info = f": Adds a {t[2]}% chance to freeze for {frame(t[4])}" \
                                                  f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 3 and is_dupe(27): info = f": Increases slow duration by {frame(t[4])}" \
                                          f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 3 and not is_dupe(27): info = f": Adds a {t[2]}% chance to slow for {frame(t[4])}" \
                                                  f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 8 and is_dupe(24): info = f": Increases knockback chance by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 8 and not is_dupe(24): info = f": Adds a {t[2]}% chance to knockback, improves by {gap(2)}%" \
                                                  f"{maximum(3)}"
        elif t[0] == 10 and is_dupe(40): info = f": Upgrades strengthen attack power by{start(4)}{gap(4)}%{maximum(5)}"
        elif t[0] == 10 and not is_dupe(40):
            info = f": Adds {t[4]}% attack power at {100 - t[2]}% health, increases by {gap(4)}%{maximum(5)}"
        elif t[0] == 11 and is_dupe(42): info = f": Upgrades chance to survive lethal strikes by{start(2)}" \
                                               f"{gap(2)}%{maximum(3)}"
        elif t[0] == 11 and not is_dupe(42): info = f": Adds a {t[2]}% chance to survive a lethal strike, improves by" \
                                            f" {gap(2)}%{maximum(3)}"
        elif t[0] == 13 and is_dupe(31): info = f": Upgrades critical hit chance by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 13 and not is_dupe(31): info = f": Adds a {t[2]}% chance to perform a critical hit "
        elif t[0] == 15 and is_dupe(70):
            info = f": Upgrades chance to break barriers by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 15 and not is_dupe(70):
            info = f": Adds a {t[2]}% chance to break barriers, improves by {gap(2)}%{maximum(3)}"
        elif t[0] == 17 and is_dupe(35):
            info = f": Upgrades chance to perform wave attacks by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 17 and not is_dupe(35):
            info = f": Adds a {t[2]}% chance to perform a level {t[4]} wave attack, improves by {gap(2)}%{maximum(3)}"
        elif t[0] == 18: info = f": Reduces weaken duration by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 19: info = f": Reduces freeze duration by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 20: info = f": Reduces slow duration by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 21: info = f": Reduces knockback push by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 22: info = f": Reduces wave damage by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 25: info = f": Reduces cost by {t[2]}/{int(t[2] * 1.5)}/{t[2] * 2}¢ per level " \
                                f"up to {t[3]:,}/{int(t[3] * 1.5):,}/{t[3] * 2:,}¢ "
        elif t[0] == 26: info = f": Reduces recharge time by {frame(t[2])}, improves by {frame(gap(2))}" \
                                f" per level up to {frame(t[3])} "
        elif t[0] == 27: info = f": Upgrades movement speed by {t[2]} per level up to {t[3]} "
        elif t[0] == 30: info = f": Reduces curse duration by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 31: info = f": Upgrades attack power by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 32: info = f": Upgrades health by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 50 and is_dupe(82):
            info = f": Upgrades chance of savage blows by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 50 and not is_dupe(82):
            info = f": Adds a {t[2]}% chance to perform a savage blow, improves by {gap(2)}%{maximum(3)}"
        elif t[0] == 51 and is_dupe(84):
            info = f": Increases dodge duration by {frame(t[4])}" \
                   f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 51 and not is_dupe(84):
            info = f": Adds a {t[2]}% chance to dodge attacks for {frame(t[4])}, improves by {gap(4)}f " \
                   f"<sup>{round(t[4]/30, 2)}s</sup>{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
        elif t[0] == 52: info = f": Reduces toxic damage by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 54: info = f": Reduces surge damage by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 56 and is_dupe(86):
            info = f": Upgrades chance of surge attacks by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 56 and not is_dupe(86):
            info = f": Adds a {t[2]}% chance to create a level {t[4]} surge attack between " \
                   f"{int(t[6]/4):,}~{int((t[6] + t[8])/4):,} range, improves by {gap(2)}%{maximum(3)}"
        elif t[0] == 58 and is_dupe(95):
            info = f": Upgrades chance to pierce shields by{start(2)}{gap(2)}%{maximum(3)}"
        elif t[0] == 58 and not is_dupe(95):
            info = f": Adds a {t[2]}% chance to pierce shields, improves by {gap(2)}%{maximum(3)}"
        return talents[t[0]] + info + f"({'Total ' if talent_ls[x][1][1] else ''}Cost: {talent_ls[x][1][0]} NP)"

    return [make_talent(i) for i in range(6 if talent_ls[5][0][0] else 5)]