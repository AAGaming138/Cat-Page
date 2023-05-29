"""Collection of functions that returns unit stats"""
from common import *

class UnitTypeError(Exception):
    """
    Error caused by trying to call Cat type in Enemy context,
    or vice versa
    """
    def __init__(self, is_enemy: bool):
        if is_enemy: error = "Cat type cannot be converted to Enemy type!"
        else: error = "Enemy type cannot be converted to Cat type!"
        super().__init__(error)


class StatsCommon:
    """Functions which are shared between Cats and Enemies"""
    def __init__(self, is_enemy: bool = False):
        self.is_enemy = is_enemy


    def get_ID(self, name: str) -> int:
        """
        :param name: unit name
        :return: unit ID if name exists, otherwise -1
        """
        if not name:
            return -1
        names = opencsv(DIR +
                        f"/{'enemy' if self.is_enemy else 'cat'}Names.csv",
                        header=True)
        for i in range(len(names)):
            names[i] = [x.lower() for x in names[i]]
            if name in names[i]:
                return int(names[i][0])
            else: continue
        return -1


    def get_traits(self, ls: list, link: bool = False):
        """Enemy units only; determines the trait(s) of an Enemy"""
        if not self.is_enemy:
            raise UnitTypeError(self.is_enemy)
        
        def list_has(index: int) -> bool:
            """Checks if list contains a valid index"""
            try:
                int(ls[index])
            except (IndexError, ValueError):
                return False
            else:
                return int(ls[index]) != 0

        traits = []
        addt = lambda t, alt = "": traits.append(
            f"[[:Category:{alt if alt else t} Enemies|"
            f"{alt if alt else t}]]" if link else t)
        if list_has(10): addt("Red")
        if list_has(14): addt("Black")
        if list_has(15): addt("Metal")
        if list_has(16): addt("Traitless")
        if list_has(17): addt("Angel")
        if list_has(18) and not list_has(69): addt("Alien")
        if list_has(19): addt("Zombie")
        if list_has(48): addt("Witch")
        if list_has(49): addt("Typeless")
        if list_has(69) and list_has(18): addt("StarredAlien", "Starred Alien")
        if list_has(71): addt("Eva Angel")
        if list_has(72): addt("Relic")
        if list_has(93): addt("Aku")
        if list_has(13): addt("Floating")
        if list_has(94): addt("Colossal")
        if list_has(101): addt("Behemoth")
        return "/".join(traits)


    def get_atkanim(self, ID: int, form: str, ls: list) -> tuple:
        """
        :param ID: unit ID
        :param form: normal, evolved, or true form
        :param ls: normal, evolved, or true data values
        :return: backswing, attack frequency tuple
        """
        nums = 12 if self.is_enemy else 13

        # START BACKSWING
        fi = f"{ID:03}_{'e' if self.is_enemy or form == '' else form}02.maanim"

        try:
            anim_file = opencsv(f"{data_mines}/ImageDataLocal/{fi}", header=True)
        except FileNotFoundError:
            return 100, 0 if self.is_enemy else 44, 471

        frame = 0
        for i in range(len(anim_file)):
            if len(anim_file[i]) != 4:
                anim_file[i] = [0, 0, 0, 0]
                # any list of 4 numbers are actual animation data, so this
                # bit basically discards everything that is not 4 numbers
                # then turns it into a dummy list of 4 numbers to be interpreted
            else:
                for j in range(4):
                    anim_file[i][j] = int(anim_file[i][j])
            if anim_file[i][0] > frame:
                frame = anim_file[i][0]
            # frame is simply the largest number of the 4 numbered list,
            # which is the last frame before restarting the attack animation

        # frame + 1 is the entire attack, ls[12/13] is the foreswing
        backswing = frame + 1 - ls[nums]
        # END BACKSWING

        # START ATTACK FREQUENCY
        mult = range(55, 59) if self.is_enemy else range(59, 63)

        # Note: ls[4] is the tba/2
        tba = ls[4] * 2
        if tba != 0:
            try:
                if ls[mult[0]] != 0:
                    atkfreq = tba + \
                              (ls[mult[3]] if ls[mult[1]] != 0 else ls[mult[2]])
                    # if multi-hit
                else:
                    raise IndexError
            except IndexError:
                atkfreq = tba + ls[nums]
            # if not multi-hit, it's just tba + foreswing
        else:
            atkfreq = ls[nums] + backswing + 1
            # if tba is 0, it's foreswing + backswing
        return backswing, atkfreq - 1
        # subtract 1 since atkfreq also accounts for the attacking frame
        # which should be instantaneous


    def get_abilities(self, ls: list, mode: int) -> str:
        """
        :param ls: form list
        :param mode: 0 for Cat Stats, 1 for Calcstatstable, 2 for Performance
        :return: string of list of abilities
        """
        nums = [[44, 59, 63, 64, 65, 99, 100, 101, 102, 103, 104],
                [35, 55, 59, 60, 61, 95, 96, 97, 98, 99, 100]]
        num = nums[1] if self.is_enemy else nums[0]
        try:
            ls[-1] = int(re.sub('[^0-9]', '', str(ls[-1])))
            # why ponos why
        except (ValueError, UnicodeDecodeError):
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
            if list_has(num[0]) and list_has(num[5]) and not list_has(num[8]):
                if ls[num[7]] > 0:
                    return f" on 1st hit, {ls[num[6]]:,}~" \
                           f"{ls[num[6]] + ls[num[7]]:,} on 2nd hit"
                else:
                    return f" on 1st hit, {ls[num[6]] + ls[num[7]]:,}~" \
                           f"{ls[num[6]]:,} on 2nd hit"
                # long distance multiple range hits
            elif list_has(num[0]) and list_has(num[5]) and list_has(num[8]):
                if ls[num[10]] > 0:
                    return f" on 1st hit, {ls[num[6]]:,}~" \
                           f"{ls[num[6]] + ls[num[7]]:,} on 2nd hit" \
                           f", {ls[num[9]]:,}~" \
                           f"{ls[num[9]] + ls[num[10]]:,} on 3rd hit"
                else:
                    return f" on 1st hit, {ls[num[6]] + ls[num[7]]:,}~" \
                           f"{ls[num[6]]:,} on 2nd hit," \
                           f" {ls[num[9]] + ls[num[10]]:,}~" \
                           f"{ls[num[9]]:,} on 3rd hit"
                # omni strike multiple range hits
            else:
                return ''

        def multab() -> str:
            """Checks for abilities on different hits during multi-hit"""
            if list_has(num[3]) and not (list_has(num[2]) or list_has(num[4])):
                return " on 2nd hit"
            elif list_has(num[4]) and not (list_has(num[2]) or list_has(num[3])):
                return " on 3rd hit"
            elif list_has(num[3]) and list_has(num[4]) and not list_has(num[2]):
                return " on 2nd and 3rd hits"
            elif list_has(num[1]) and list_has(num[2]) and \
                    not (list_has(num[3]) or list_has(num[4])):
                return " on 1st hit"
            else:
                return ""

        sec = lambda i: round(ls[i] / 30, 2)
        abilities = []
        immunities = []

        addim = lambda im: \
            immunities.append(
                f"[[Special Abilities#Immune to {im}|"
                f"{'Immune to ' if len(immunities) == 0 else ''}{im}]]")
        # Note: addim does not work with Evade Surge and
        #       Warp Blocker or if mode is 2
        abil = lambda ab, dis='': \
            f"[[Special Abilities#{ab}|{ab if not dis else dis}]]"
        # Note: if the display link is the same as actual link,
        #       then print rest of link
        pl = lambda ind, threshold = 30: 's' if ls[ind] != threshold else ''

        if self.is_enemy:
            if list_has(52):
                abilities.append("Attacks once,"
                                 " then disappears from the battlefield")
            if list_has(55):
                temp = f', {ls[56]:,} at {ls[58]}f <sup>{sec(58)}s</sup>' \
                       if ls[56] != 0 else ''
                abilities.append(f"{abil('Multi-Hit')} ({ls[3]:,} at {ls[12]}f"
                                 f" <sup>{sec(12)}s</sup>, {ls[55]:,} at "
                                 f"{ls[57]}f <sup>{sec(57)}s</sup>{temp})")
            if list_has(35) and ls[36] > 0:
                abilities.append(f"{abil('Long Distance')} (Effective range:"
                                 f" {ls[35]:,}~{ls[35] + ls[36]:,}"
                                 f"{LD_range()})")
            elif list_has(35) and ls[36] <= 0:
                abilities.append(f"{abil('Omni Strike')}"
                                 f" (Effective range: {ls[35] + ls[36]:,}~"
                                 f"{ls[35]:,}{LD_range()})")
            if list_has(20):
                abilities.append(
                f"{ls[20]}% chance to {abil('Knockback', 'knockback')}"
                f" Cat Units{multab()}")
            if list_has(21):
                abilities.append(f"{ls[21]}% chance to {abil('Freeze', 'freeze')}"
                                 f" Cat Units for {ls[22]:,}f <sub>{sec(22)} "
                                 f"second{pl(22)}</sub>{multab()}")
            if list_has(23):
                abilities.append(f"{ls[23]}% chance to {abil('Slow', 'slow')}"
                                 f" Cat Units for {ls[24]:,}f <sub>{sec(24)}"
                                 f" second{pl(24)}</sub>{multab()}")
            if list_has(25):
                abilities.append(f"{ls[25]}% chance to perform a"
                                 f" {abil('Critical', 'critical hit')}"
                                 f"{multab()}")
            if list_has(26):
                abilities.append(f"{abil('Base Destroyer')}"
                                 f" (deals 4x damage to the [[Cat Base]])")
            if list_has(27):
                temp = 'Wave Attack' if len(ls) < 87 or ls[86] != 1 else \
                       'Wave Attack#Mini-Wave|Mini-Wave'
                abilities.append(f"{ls[27]}% chance to create a level"
                                 f" {ls[28]} [[{temp}]]{multab()}")
            if list_has(29):
                abilities.append(f"{ls[29]}% chance to {abil('Weaken', 'weaken')}"
                                 f" Cat Units to {ls[31]}% for {ls[30]:,}f <sub>"
                                 f"{sec(30)} second{pl(30)}</sub>{multab()}")
            if list_has(32):
                abilities.append(f"{abil('Strengthen', 'Strengthens')} by "
                                 f"{ls[33]}% at {ls[32]}% health")
            if list_has(34):
                abilities.append(f"{ls[34]}% chance to "
                                 f"{abil('Survive', 'survive')} a lethal strike")
            # 'regular' abilities
            if list_has(37): addim("Waves")
            if list_has(39): addim("Knockback")
            if list_has(40): addim("Freeze")
            if list_has(41): addim("Slow")
            if list_has(42): addim("Weaken")
            # immunities

            if list_has(43):
                temp = f'{ls[43]} time{pl(43, 1)} 'if ls[43]!=-1 else 'unlimited'
                abilities.append(f"[[Special Abilities#Burrow|Burrows]] under"
                                 f"ground {int(ls[44] / 4):,} when a Cat enters"
                                 f" its range ({temp})")
            if list_has(45):
                temp = f'{ls[45]} time{pl(45, 1)} 'if ls[45]!=-1 else 'unlimited'
                abilities.append(f"[[Special Abilities#Revive|Revives]] with "
                                 f"{ls[47]}% HP after being dead for {ls[46]:,}f"
                                 f" <sub>{sec(46)} second{pl(46)}</sub> ({temp})")
            if list_has(64):
                abilities.append(f"[[Barrier]] (Limit: {ls[64]:,})")
            if list_has(65):
                temp = f"{'back' if ls[67] > 0 else 'forward'} by" \
                       f" {abs(int(ls[67] / 4)):,}"
                abilities.append(f"{ls[65]}% chance to [[Special Abilities#Warp"
                                 f"|warp]] Cat Units {temp} range for {ls[66]:,}"
                                 f"f <sub>{sec(66)} second{pl(66)}</sub>{multab()}")
            if list_has(73):
                abilities.append(f"{ls[73]}% chance to {abil('Curse', 'curse')}"
                                 f" Cat Units for {ls[74]:,}f <sub>"
                                 f"{sec(74)} second{pl(74)}</sub>{multab()}")
            if list_has(75):
                abilities.append(f"{ls[75]}% chance to perform a "
                                 f"{abil('Savage Blow', 'savage blow')} dealing "
                                 f"3x damage{multab()}")
            if list_has(77):
                abilities.append(f"{ls[77]}% chance to "
                                 f"{abil('Dodge Attack', 'dodge attacks')} from"
                                 f" Cat Units for {ls[78]}f <sub>{sec(78)}"
                                 f" second{pl(78)}</sub>")
            if list_has(79):
                abilities.append(f"{ls[79]}% chance to perform a [[Special"
                                 f" Abilities#Toxic|Toxic]] attack (takes "
                                 f"{ls[80]}% of Cat Units' maximum health){multab()}")
            if list_has(81):
                abilities.append(f"{ls[81]}% chance to create a level {ls[84]}"
                                 f" [[Surge Attack]] between {int(ls[82] / 4):,}"
                                 f" and {int(ls[82] / 4) + int(ls[83] / 4):,}"
                                 f" range{multab()}")
            if list_has(85):
                immunities.append(f"[[Special Abilities#Evade Surge|"
                                  f"{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"Surge]]")
            if list_has(87):
                abilities.append(f"[[Shield]] (initial HP: {ls[87]:,}; "
                                 f"regenerates with {ls[88]}% HP)")
            if list_has(89):
                abilities.append(f"{ls[89]}% chance to create a level {ls[92]}"
                                 f" [[Surge Attack]] between {int(ls[90] / 4):,}"
                                 f" and {int(ls[90] / 4) + int(ls[91] / 4):,}"
                                 f" range upon death")
        else:
            ftrait = ''
            traits = []

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

        if mode == 0:
            if list_has(58):
                abilities.append(f"Attacks once,"
                                 f" then disappears from the battlefield")
            if list_has(59):
                temp = f', {ls[60] * 17:,} at {ls[62]}f <sup>{sec(62)}s</sup>' \
                       if ls[60] != 0 else ''
                abilities.append(f"{abil('Multi-Hit')} ({ls[3] * 17:,} at"
                                 f" {ls[13]}f <sup>{sec(13)}s</sup>, {ls[59] * 17:,}"
                                 f" at {ls[61]}f <sup>{sec(61)}s</sup>{temp})")
            if list_has(44) and ls[45] > 0:
                abilities.append(f"{abil('Long Distance')} (Effective range:"
                                 f" {ls[44]:,}~{ls[44] + ls[45]:,}{LD_range()})")
            elif list_has(44) and ls[45] <= 0:
                abilities.append(f"{abil('Omni Strike')} (Effective range:"
                                 f" {ls[44] + ls[45]:,}~{ls[44]:,}{LD_range()})")
            if list_has(23):
                abilities.append(f"{abil('Strong Against', 'Strong')} against"
                                 f" {ftrait} enemies (Deals 1.5x damage,"
                                 f" only takes 1/2 damage)")
            if list_has(24):
                abilities.append(f"{ls[24]}% chance to"
                                 f" {abil('Knockback', 'knockback')} {ftrait}"
                                 f" enemies{multab()}")
            if list_has(25):
                abilities.append( f"{ls[25]}% chance to {abil('Freeze', 'freeze')}"
                                  f" {ftrait} enemies for {ls[26]}f <sub>"
                                  f"{sec(26)} second{pl(26)}</sub>{multab()}")
            if list_has(27):
                abilities.append(f"{ls[27]}% chance to {abil('Slow', 'slow')} "
                                 f"{ftrait} enemies for {ls[28]}f <sub>{sec(28)}"
                                 f" second{pl(28)}</sub>{multab()}")
            if list_has(29):
                abilities.append(f"{abil('Resistant')} to {ftrait} enemies")
            if list_has(30):
                abilities.append(f"Deals {abil('Massive Damage', 'massive damage')}"
                                 f" to {ftrait} enemies")
            if list_has(31):
                abilities.append(f"{ls[31]}% chance to perform a "
                                 f"{abil('Critical', 'critical hit')}{multab()}")
            if list_has(32):
                abilities.append(f"{abil('Attacks Only', 'Attacks only')} "
                                 f"{ftrait} enemies")
            if list_has(33):
                abilities.append(f"{abil('Extra Money', 'Double money')} gained"
                                 f" when defeating enemies{multab()}")
            if list_has(34):
                abilities.append(abil('Base Destroyer'))
            if list_has(35):
                temp = 'Wave Attack' if len(ls) < 95 or ls[94] != 1 else \
                       'Wave Attack#Mini-Wave|Mini-Wave'
                abilities.append(f"{ls[35]}% chance to create a level"
                                 f" {ls[36]} [[{temp}]]{multab()}")
            if list_has(37):
                abilities.append(f"{ls[37]}% chance to {abil('Weaken', 'weaken')}"
                                 f" {ftrait} enemies to {ls[39]}% for {ls[38]}f"
                                 f" <sub>{sec(38)} second{pl(38)}</sub>{multab()}")
            if list_has(40):
                abilities.append(f"{abil('Strengthen', 'Strengthens')}"
                                 f" by {ls[41]}% at {ls[40]}% health")
            if list_has(42):
                abilities.append(f"{ls[42]}% chance to "
                                 f"{abil('Survive', 'survive')} a lethal strike")
            if list_has(43):
                abilities.append(f"{abil('Metal')} (Only takes 1 damage from"
                                 f" non-[[Critical Hit|Critical]]"
                                 f" or [[Toxic]] attacks)")
            if list_has(47):
                abilities.append(abil('Wave Shield'))
            # 'regular' abilities
            if list_has(46): addim("Waves")
            if list_has(48): addim("Knockback")
            if list_has(49): addim("Freeze")
            if list_has(50): addim("Slow")
            if list_has(51): addim("Weaken")
            # immunities
            if list_has(52):
                abilities.append(f"{abil('Zombie Killer')} (stops [[:Category:"
                                 f"Zombie Enemies|Zombies]] from reviving)")
            if list_has(53):
                abilities.append(f"{abil('Witch Killer')} (Deals 5x damage to "
                                 f"[[:Category:Witch Enemies|Witches]],"
                                 f" only takes 1/10 damage)")
            if list_has(56):
                abilities.append(f"Immune to Boss Shockwave")
            if list_has(70):
                abilities.append(f"{ls[70]}% chance to "
                                 f"{abil('Barrier Breaker', 'break')} "
                                 f"{abil('Barrier', 'barriers')}{multab()}")
            if list_has(75):
                immunities.append(f"[[Special Abilities#Warp Blocker|"
                                  f"{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"Warp]]")
            if list_has(77):
                abilities.append(f"{abil('Eva Angel Killer')} (Deals 5x damage "
                                 "to [[:Category:Eva Angel Enemies|Eva Angels]],"
                                 " only takes 1/5 damage)")
            if list_has(79): addim("Curse")
            if list_has(80):
                abilities.append(f"{abil('Insanely Tough', 'Insanely tough')}"
                                 f" against {ftrait} enemies")
            if list_has(81):
                abilities.append(f"Deals {abil('Insane Damage', 'insane damage')}"
                                 f" to {ftrait} enemies")
            if list_has(82):
                abilities.append(f"{ls[82]}% chance to land a "
                                 f"{abil('Savage Blow', 'savage blow')},"
                                 f" dealing 3x damage to non-[[:Category:Metal"
                                 f" Enemies|Metal]] enemies{multab()}")
            if list_has(84):
                abilities.append(f"{ls[84]}% chance to "
                                 f"{abil('Dodge Attack', 'dodge attacks')} from"
                                 f" {ftrait} enemies for {ls[85]}f <sub>"
                                 f"{sec(85)} second{pl(85)}</sub>")
            if list_has(86):
                temp = "" if len(ls) < 109 or ls[108] != 1\
                    else "#Mini-Surge|Mini-Surge"
                abilities.append(f"{ls[86]}% chance to create a level {ls[89]}"
                                 f" [[Surge Attack{temp}]] between "
                                 f"{int(ls[87] / 4):,}"
                                 f" and {int(ls[87] / 4) + int(ls[88] / 4):,}"
                                 f" range{multab()}")
            if list_has(90): addim("Toxic")
            if list_has(91):
                immunities.append(f"[[Special Abilities#Evade Surge|"
                                  f"{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"Surge]]")
            if list_has(92):
                abilities.append(f"{ls[92]}% chance to {abil('Curse', 'curse')}"
                                 f" {ftrait} enemies for {ls[93]}f <sub>"
                                 f"{sec(93)} second{pl(93)}</sub>{multab()}")
            if list_has(95):
                abilities.append(f"{ls[95]}% chance to instantly "
                                 f"{abil('Shield Piercing', 'pierce')} "
                                 f"{abil('Shield', 'shields')}{multab()}")
            if list_has(97):
                abilities.append(f"{abil('Colossus Slayer',)} (Deals 1.6x damage"
                                 f" to [[:Category:Colossal Enemies|Colossal]]"
                                 f" enemies, only takes 0.7x damage)")
            if list_has(98):
                abilities.append(f"{abil('Soulstrike')}")
            if list_has(105):
                abilities.append(f"{abil('Behemoth Slayer')} ({ls[106]}% chance"
                                 f" to dodge [[:Category:Behemoth Enemies|"
                                 f"Behemoth]] enemies' attacks for {ls[107]}f "
                                 f"<sub>{sec(107)} second{pl(107)}</sub>)")

        elif mode == 1:
            if list_has(58):
                abilities.append(f"Attacks once,"
                                 f" then disappears from the battlefield")
            if list_has(59):
                abilities.append(f"{abil('Multi-Hit', 'Multi-Hit')}"
                                 f" ({ls[3]:,} at {ls[13]}f, {ls[59]:,} at "
                                 f"{ls[61]}f"
                                 f"{f', {ls[60]:,} at {ls[62]}f' if ls[60] else ''})")
            if list_has(44) and ls[45] > 0:
                abilities.append(f"{abil('Long Distance', 'Long Distance')} "
                                 f"(Effective range: {ls[44]:,}~"
                                 f"{ls[44] + ls[45]:,}{LD_range()})")
            elif list_has(44) and ls[45] <= 0:
                abilities.append(f"{abil('Omni Strike', 'Omni Strike')} "
                                 f"(Effective range: {ls[44] + ls[45]:,}~"
                                 f"{ls[44]:,}{LD_range()})")
            if list_has(23):
                abilities.append(f"{abil('Strong Against', 'Strong')}"
                                 f" against {ftrait} enemies")
            if list_has(24):
                abilities.append(f"{abil('Knockback', 'Knockbacks')}"
                                 f" {ftrait} enemies{multab()} ({ls[24]}%)")
            if list_has(25):
                abilities.append(f"{abil('Freeze', 'Freezes')} {ftrait} enemies"
                                 f" for {ls[26]}f{multab()} ({ls[25]}%)")
            if list_has(27):
                abilities.append(f"{abil('Slow', 'Slows')} {ftrait} enemies for"
                                 f" {ls[28]}f{multab()} ({ls[27]}%)")
            if list_has(29):
                abilities.append(f"{abil('Resistant')} to {ftrait} enemies")
            if list_has(30):
                abilities.append(f"Deals {abil('Massive Damage', 'massive damage')}"
                                 f" to {ftrait} enemies")
            if list_has(31):
                abilities.append(f"{abil('Critical', 'Critical hit')}{multab()}"
                                 f" ({ls[31]}%)")
            if list_has(32):
                abilities.append(f"{abil('Attacks Only', 'Attacks only')}"
                                 f" {ftrait} enemies")
            if list_has(33):
                abilities.append(f"{abil('Extra Money', 'Extra money')}"
                                 f" when defeating enemies{multab()}")
            if list_has(34):
                abilities.append(f"{abil('Base Destroyer', 'Base destroyer')}")
            if list_has(35):
                temp = 'Wave Attack|Wave' if len(ls) < 95 or ls[94] != 1 else \
                       'Mini-Wave|Mini-Wave'
                abilities.append(f"Creates a level {ls[36]} [[Special Abilities"
                                 f"#{temp}]]{multab()} ({ls[35]}%)")
            if list_has(37):
                abilities.append(
                f"{abil('Weaken', 'Weakens')} {ftrait} enemies to {ls[39]}% for"
                f" {ls[38]}f{multab()} ({ls[37]}%)")
            if list_has(40):
                abilities.append(f"{abil('Strengthen', 'Strengthens')} by"
                                 f" {ls[41]}% at {ls[40]}% health")
            if list_has(42):
                abilities.append(f"{abil('Survive', 'Survives')}"
                                 f" a lethal strike ({ls[42]}%)")
            if list_has(43):
                abilities.append(f"{abil('Metal')} (Only takes 1 damage from"
                                 f" non-[[Critical Hit|Critical]]"
                                 f" or [[Toxic]] attacks)")
            if list_has(47): abilities.append(abil('Wave Shield'))
            if list_has(46): addim("Waves")
            if list_has(48): addim("Knockback")
            if list_has(49): addim("Freeze")
            if list_has(50): addim("Slow")
            if list_has(51): addim("Weaken")
            if list_has(52):
                abilities.append(abil('Zombie Killer'))
            if list_has(53):
                abilities.append(abil('Witch Killer'))
            if list_has(56):
                abilities.append(f"Immune to Boss Shockwave")
            if list_has(70):
                abilities.append(f"{abil('Barrier Breaker')} ({ls[70]}%)")
            if list_has(77):
                abilities.append(f"{abil('Eva Angel Killer', 'Eva Angel Killer')}")
            if list_has(79): addim("Curse")
            if list_has(80):
                abilities.append(f"{abil('Insanely Tough', 'Insanely tough')}"
                                 f" against {ftrait} enemies")
            if list_has(81):
                abilities.append(f"Deals {abil('Insane Damage', 'insane damage')}"
                                 f" to {ftrait} enemies")
            if list_has(82):
                abilities.append(f"{abil('Savage Blow', 'Savage Blow')}"
                                 f"{multab()} ({ls[82]}%)")
            if list_has(84):
                abilities.append(f"{abil('Dodge Attack', 'Dodges')} {ftrait}"
                                 f" enemies' attacks for {ls[85]}f ({ls[84]}%)")
            if list_has(86):
                temp = abil('Surge Attacks',
                            'Surge Attack') if len(ls) < 109 or ls[108] != 1 else \
                       '[[Surge Attack#Mini-Surge|Mini-Surge]]'
                abilities.append(f"Creates a level {ls[89]} {temp} between "
                                 f"{int(ls[87] / 4):,} and "
                                 f"{int(ls[87] / 4) + int(ls[88] / 4):,} "
                                 f"range{multab()} ({ls[86]}%)")
            if list_has(90): addim("Toxic")
            if list_has(91):
                immunities.append(f"[[Special Abilities#Evade Surge|"
                                  f"{'Evade ' if len(immunities) == 0 else ''}"
                                  f"Surge]]")
            if list_has(75):
                immunities.append(f"[[Special Abilities#Warp Blocker|Warp"
                                  f"{' Blocker' if len(immunities) == 0 else ''}"
                                  f"]]")
            if list_has(92):
                abilities.append(
                    f"{abil('Curse', 'Curses')} {ftrait} enemies for"
                    f" {ls[93]}f{multab()} ({ls[92]}%)")
            if list_has(95):
                abilities.append(f"{abil('Shield Piercing', 'Shield Piercer')}"
                                 f"{multab()} ({ls[95]}%)")
            if list_has(97):
                abilities.append(f"{abil('Colossus Slayer')}")
            if list_has(98):
                abilities.append(f"{abil('Soulstrike')}")
            if list_has(105):
                abilities.append(f"{abil('Behemoth Slayer')} (Dodges [[:"
                                 f"Category:Behemoth Enemies|Behemoth]]"
                                 f" enemies' attacks for {ls[107]}f"
                                 f" ({ls[106]}%))")

        elif mode == 2:
            pro = "'''+''' "
            con = "'''-''' "
            if list_has(23):
                abilities.append(f"{pro}{abil('Strong Against', 'Strong')}"
                                 f" against {ftrait} enemies")
            if list_has(24):
                abilities.append(f"{pro}{ls[24]}% chance to "
                                 f"{abil('Knockback', 'knockback')}"
                                 f" {ftrait} enemies{multab()}")
            if list_has(25):
                abilities.append(f"{pro}{ls[25]}% chance to "
                                 f"{abil('Freeze', 'freeze')} {ftrait} enemies "
                                 f"for {sec(26)} second{pl(26)}{multab()}")
            if list_has(27):
                abilities.append(f"{pro}{ls[27]}% chance to "
                                 f"{abil('Slow', 'slow')} {ftrait} enemies for "
                                 f"{sec(28)} second{pl(28)}{multab()}")
            if list_has(29):
                abilities.append(f"{pro}{abil('Resistant')} to {ftrait} enemies")
            if list_has(30):
                abilities.append(f"{pro}Deals "
                                 f"{abil('Massive Damage', 'massive damage')} "
                                 f"to {ftrait} enemies")
            if list_has(31):
                abilities.append(f"{pro}{ls[31]}% chance to perform a "
                                 f"{abil('Critical', 'critical hit')}{multab()}")
            if list_has(32):
                abilities.append(f"{con}{abil('Attacks Only', 'Attacks only')}"
                                 f" {ftrait} enemies")
            if list_has(33):
                abilities.append(f"{pro}{abil('Extra Money', 'Double money')}"
                                 f" gained when defeating enemies{multab()}")
            if list_has(34):
                abilities.append(f"{pro}{abil('Base Destroyer', 'Base destroyer')}")
            if list_has(35):
                temp = 'Wave Attack' if len(ls) < 95 or ls[94] != 1 else \
                       'Wave Attack#Mini-Wave|Mini-Wave'
                abilities.append(f"{pro}{ls[35]}% chance to create a level "
                                 f"{ls[36]} [[{temp}]]{multab()}")
            if list_has(37):
                abilities.append(f"{pro}{ls[37]}% chance to "
                                 f"{abil('Weaken', 'weaken')} {ftrait} enemies"
                                 f" to {ls[39]}% for {sec(38)}"
                                 f" second{pl(38)}{multab()}")
            if list_has(40):
                abilities.append(f"{pro}{abil('Strengthen', 'Strengthens')}"
                                 f" by {ls[41]}% at {ls[40]}% health")
            if list_has(42):
                abilities.append(f"{pro}{ls[42]}% chance to "
                                 f"{abil('Survive', 'survive')} a lethal strike")
            if list_has(43):
                abilities.append(f"{pro}{abil('Metal')}")
            if list_has(47):
                abilities.append(f"{pro}{abil('Wave Shield')}")
            if list_has(44) and ls[45] > 0:
                abilities.append(f"{pro}{abil('Long Distance')} (Effective"
                                 f" range: {ls[44]:,}~"
                                 f"{ls[44] + ls[45]:,}{LD_range()})")
            elif list_has(44) and ls[45] <= 0:
                abilities.append(f"{pro}{abil('Omni Strike')}"
                                 f" (Effective range: {ls[44] + ls[45]:,}"
                                 f"~{ls[44]:,}{LD_range()})")
            paddim = lambda im: \
                immunities.append(f"{pro if len(immunities) == 0 else ''}"
                                  f"[[Special Abilities#Immune to {im}"
                                  f"|{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"{im}]]")
            if list_has(46): paddim("Waves")
            if list_has(48): paddim("Knockback")
            if list_has(49): paddim("Freeze")
            if list_has(50): paddim("Slow")
            if list_has(51): paddim("Weaken")
            if list_has(52):
                abilities.append(f"{pro}{abil('Zombie Killer')}")
            if list_has(53):
                abilities.append(f"{pro}{abil('Witch Killer')}")
            if list_has(58):
                abilities.append(f"{con}Dies after attacking once")
            if list_has(70):
                abilities.append(
                f"{pro}{ls[70]}% chance to {abil('Barrier Breaker', 'break')} "
                f"{abil('Barrier', 'barriers')}{multab()}")
            if list_has(75):
                immunities.append(f"{pro if len(immunities) == 0 else ''}"
                                  f"[[Special Abilities#Warp Blocker"
                                  f"|{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"Warp]]")
            if list_has(77):
                abilities.append(f"{pro}{abil('Eva Angel Killer')}")
            if list_has(79): paddim("Curse")
            if list_has(80):
                abilities.append(
                f"{pro}{abil('Insanely Tough', 'Insanely tough')}"
                f" against {ftrait} enemies")
            if list_has(81):
                abilities.append(f"{pro}Deals "
                                 f"{abil('Insane Damage', 'insane damage')} "
                                 f"to {ftrait} enemies")
            if list_has(82):
                abilities.append(f"{pro}{ls[82]}% chance to land a "
                                 f"{abil('Savage Blow', 'savage blow')}{multab()}")
            if list_has(84):
                abilities.append(f"{pro}{ls[84]}% chance to "
                                 f"{abil('Dodge Attack', 'dodge attacks')} from"
                                 f" {ftrait} enemies for {sec(85)} second{pl(85)}")
            if list_has(86):
                temp = "" if len(ls) < 109 or ls[108] != 1 \
                    else "#Mini-Surge|Mini-Surge"
                abilities.append(f"{pro}{ls[86]}% chance to create a level "
                                 f"{ls[89]} [[Surge Attack{temp}]] between "
                                 f"{int(ls[87] / 4):,} and "
                                 f"{int(ls[87] / 4) + int(ls[88] / 4):,} range"
                                 f"{multab()}")
            if list_has(90): paddim("Toxic")
            if list_has(91):
                immunities.append(f"{pro if len(immunities) == 0 else ''}"
                                  f"[[Special Abilities#Evade Surge|"
                                  f"{'Immune to ' if len(immunities) == 0 else ''}"
                                  f"Surge]]")
            if list_has(92):
                abilities.append(f"{pro}{ls[92]}% chance to "
                                 f"{abil('Curse', 'curse')} {ftrait} enemies for "
                                 f"{sec(93)} second{pl(93)}{multab()}")
            if list_has(95):
                abilities.append(f"{pro}{ls[95]}% chance to instantly "
                                 f"{abil('Shield Piercing', 'pierce')} "
                                 f"{abil('Shield', 'shields')}{multab()}")
            if list_has(97):
                abilities.append(f"{pro}{abil('Colossus Slayer')}")
            if list_has(98):
                abilities.append(f"{abil('Soulstrike')}")
            if list_has(105):
                abilities.append(f"{pro}{abil('Behemoth Slayer')}")
            if list_has(56):
                abilities.append(f"{pro}Immune to Boss Shockwave")

        if len(immunities) == 1:
            abilities.append(f"{immunities[0]}")
        elif len(immunities) > 1:
            immunities[-1] = f"and {immunities[-1]}"
            abilities.append(
                f"{', ' if len(immunities) > 2 else ' '}".join(immunities))
        if mode == 2 and list_has(59):
            abilities.append(
            f"{pro if ls[3] > ls[59] else con}{abil('Multi-Hit')}")
        # deals with potentially a list of immunities
        # example: Immune to knockback, Weaken, Warp, and Curse

        if len(abilities) != 0:
            return re.sub('\.0(?![0-9])', '',
                          '<br>\n'.join(abilities)) if mode != 2 else abilities
            # turn the list into text
        else:
            return "-" if mode != 2 else ''


    def get_talents(self, talent_ls: list, cat_ls: list) -> tuple:
        """Cat units only; Gets talents for cat units"""

        if self.is_enemy:
            raise UnitTypeError(self.is_enemy)
        if not talent_ls: return ()

        def link(ability: str, type: str = 'default'):
            if type == 'default': l = ability
            elif type == 'res': l = "Resist"
            elif type == 'stat': l = "Stat Enhancements"
            elif type == 'tar':
                return f"'''Target [[:Category:{ability} Enemies|{ability}]]'''"
            else: l = type
            return f"'''[[Special Abilities#{l}|{ability}]]'''"

        nor = 0 # number of normal talents
        ult = 0 # number of ultra talents
        for i in range(len(talent_ls)):
            if talent_ls[i][0][0] != 0:
                if talent_ls[i][0][-1] != 1:
                    nor += 1
                else:
                    ult += 1

        talents = {
            1:  link("Weaken"),
            2:  link("Freeze"),
            3:  link("Slow"),
            5:  link("Strong Against"),
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
            36: link("Metal", "tar"),
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
            59: link("Soulstrike"),
            60: link("Curse"),
            61: link("Attack Frequency Up", "stat"),
            62: link("Mini-Wave", "Wave Attack"),
            63: link("Colossus Slayer"),
            64: link("Behemoth Slayer"),
            65: link("Mini-Surge", "Surge Attacks")
        }
        def make_talent():
            """Generator that gives formatted talents"""

            for x in range(nor + ult):
                t = talent_ls[x][0]
                info = ' '
                frame = lambda value:\
                    f"{value}f <sup>{round(value/30, 2)}s</sup>"
                # format: xxf <sup>xx.xxs</sup>
                to_int = lambda num: \
                    int(num) if int(num) == num else round(num, 2)
                # turns into int if int otherwise round to 2 decimal places
                gap = lambda m: to_int((t[m+1] - t[m])/(t[1] - 1))
                # (max lvl stats - first lvl stats) / (max lvl - first lvl)
                start_perc = lambda s: f" {t[s]}%, improves by " \
                    if gap(s) != t[s] else " "
                # start improvement, increases by gap
                start_time = lambda s: \
                    f" {frame(t[s])}, improves by {frame(gap(s))}" \
                        if gap(s) != t[s] else " "
                # same thing but for time instead of %
                maximum = lambda h, mode = '%':\
                    f" per level up to {t[h]}{'%' if mode == '%' else mode} "
                #
                def is_dupe(index: int):
                    try:
                        cat_ls[index]
                    except IndexError:
                        return False
                    else:
                        return bool(cat_ls[index])

                if t[0] == 1 and is_dupe(37):
                    info = f": Increases weaken duration by{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 1 and not is_dupe(37):
                    info = f": Adds a {t[2]}% chance to weaken enemies to" \
                           f" {100 - t[7]}% for{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 2 and is_dupe(25):
                    info = f": Increases freeze duration by {frame(t[4])}" \
                           f"{start_time(4)}{maximum(5, 'f')}<sup>" \
                           f"{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 2 and not is_dupe(25):
                    info = f": Adds a {t[2]}% chance to freeze for{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 3 and is_dupe(27):
                    info = f": Increases slow duration by{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 3 and not is_dupe(27):
                    info = f": Adds a {t[2]}% chance to slow for{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 5:
                    info = f": Becomes strong against targeted trait."
                elif t[0] == 8 and is_dupe(24):
                    info = f": Increases knockback chance by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 8 and not is_dupe(24):
                    info = f": Adds a {t[2]}% chance to knockback," \
                           f" improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 10 and is_dupe(40):
                    info = f": Upgrades strengthen attack" \
                           f" power by{start_perc(4)}{gap(4)}%{maximum(5)}"
                elif t[0] == 10 and not is_dupe(40):
                    info = f": Adds {t[4]}% attack power at {100 - t[2]}%" \
                           f" health, increases by {gap(4)}%{maximum(5)}"
                elif t[0] == 11 and is_dupe(42):
                    info = f": Upgrades chance to survive lethal strikes by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 11 and not is_dupe(42):
                    info = f": Adds a {t[2]}% chance to survive a lethal" \
                           f" strike, improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 13 and is_dupe(31):
                    info = f": Upgrades critical hit chance by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 13 and not is_dupe(31):
                    info = f": Adds a {t[2]}% chance to perform a critical hit "
                elif t[0] == 15 and is_dupe(70):
                    info = f": Upgrades chance to break barriers by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 15 and not is_dupe(70):
                    info = f": Adds a {t[2]}% chance to break barriers," \
                           f" improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 17 and is_dupe(35):
                    info = f": Upgrades chance to perform wave attacks by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 17 and not is_dupe(35):
                    info = f": Adds a {t[2]}% chance to perform a level {t[4]}" \
                           f" wave attack, improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 18:
                    info = f": Reduces weaken duration by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 19:
                    info = f": Reduces freeze duration by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 20:
                    info = f": Reduces slow duration by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 21:
                    info = f": Reduces knockback push by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 22:
                    info = f": Reduces wave damage by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 25:
                    info = f": Reduces cost by {t[2]}/{int(t[2] * 1.5)}/" \
                           f"{t[2] * 2}¢ per level " \
                           f"up to {t[3]:,}/{int(t[3] * 1.5):,}/{t[3] * 2:,}¢ "
                elif t[0] == 26:
                    info = f": Reduces recharge time by {frame(t[2])}," \
                           f" improves by {frame(gap(2))}" \
                           f" per level up to {frame(t[3])} "
                elif t[0] == 27:
                    info = f": Upgrades movement speed by {t[2]}" \
                           f" per level up to {t[3]} "
                elif t[0] == 30:
                    info = f": Reduces curse duration by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 31:
                    info = f": Upgrades attack power by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 32:
                    info = f": Upgrades health by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 50 and is_dupe(82):
                    info = f": Upgrades chance of savage blows by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 50 and not is_dupe(82):
                    info = f": Adds a {t[2]}% chance to perform a savage blow," \
                           f" improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 51 and is_dupe(84):
                    info = f": Increases dodge duration by{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 51 and not is_dupe(84):
                    info = f": Adds a {t[2]}% chance to dodge attacks for" \
                           f"{start_time(4)}{maximum(5, 'f')}<sup>" \
                           f"{round(t[5]/30, 2)}s</sup> "
                elif t[0] == 52:
                    info = f": Reduces toxic damage by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 54:
                    info = f": Reduces surge damage by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 56 and is_dupe(86):
                    info = f": Upgrades chance of surge attacks by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 56 and not is_dupe(86):
                    info = f": Adds a {t[2]}% chance to create a" \
                           f" level {t[4]} surge attack between " \
                           f"{int(t[6]/4):,}~{int((t[6] + t[8])/4):,} range," \
                           f" improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 58 and is_dupe(95):
                    info = f": Upgrades chance to pierce shields by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 58 and not is_dupe(95):
                    info = f": Adds a {t[2]}% chance to pierce shields," \
                           f" improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 60 and is_dupe(92):
                    info = f": Increases curse duration by{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5] / 30, 2)}s</sup> "
                elif t[0] == 60 and not is_dupe(92):
                    info = f": Adds a {t[2]}% chance to curse for{start_time(4)}" \
                           f"{maximum(5, 'f')}<sup>{round(t[5] / 30, 2)}s</sup> "
                elif t[0] == 61:
                    info = f": Decreases time between attacks by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 62 and is_dupe(94):
                    info = f": Upgrades chance to perform mini-waves by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 62 and not is_dupe(94):
                    info = f": Adds a {t[2]}% chance to perform a level {t[4]}" \
                           f" mini-wave, improves by {gap(2)}%{maximum(3)}"
                elif t[0] == 65 and is_dupe(108):
                    info = f": Upgrades chance of mini-surge by" \
                           f"{start_perc(2)}{gap(2)}%{maximum(3)}"
                elif t[0] == 65 and not is_dupe(108):
                    info = f": Adds a {t[2]}% chance to create a" \
                           f" level {t[4]} mini-surge between " \
                           f"{int(t[6]/4):,}~{int((t[6] + t[8])/4):,} range," \
                           f" improves by {gap(2)}%{maximum(3)}"

                yield talents[t[0]] + info + \
                      f"({'Total ' if talent_ls[x][1][1] else ''}" \
                      f"Cost: {talent_ls[x][1][0]} NP)"

        return [i for i in make_talent()], nor, ult
        # talents in list form, number of normal tals, number of ultra tals

# TODO: - Check some of make_talent() and some of get_abilities()