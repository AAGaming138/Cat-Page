"""Program that receives input and writes the contents of a page"""
from common import *
from StatsCommon import StatsCommon
from Cat import Cat

class CatPage(Cat):
    """
    Inherits from Cat class.

    Attributes:
    ID:         int     # Unit ID
    ls:         list    # Ability and stats list
    r:          tuple   # Rarity, max level, catfruit, version tuple
    tf:         bool    # Does unit have true form
    names:      list    # Names list
    gacha:       str    # Gacha banner (if part of one)
    drop:       bool    # Is unit a drop item (from stage)
    desc:       list    # JP description + names
    tals:       list    # Talents list
    """

    def __init__(self, ID: int):
        super().__init__(ID)
        if self.ID == -1:
            return
        self.stats = StatsCommon()
        self.tf = self.trueForm
        self.r = self.getRarity()
        self.names = self.getNames(ID)
        self.ls = self.getData()
        if len(self.ls) < 3:
            return
        self.gacha = self.getGacha()
        self.drop = self.isDrop()
        self.desc = self.getDesc()
        self.en_desc = self.stats.get_en_desc(self.ID)
        self.tals = self.getTalents()

        match self.r[0]:
            case "Normal": self.rps = [60]
            case "Special": self.rps = [60]
            case "Rare": self.rps = [70, 90]
            case "Super Rare": self.rps = [60, 80]
            case "Uber Rare": self.rps = [60, 80]

        if self.names[1] == "Bahamut Cat": self.rps = [30]
        if self.isCrazed: self.rps = [20]


    def getStart(self) -> str:
        """
        Gets the start of the page: intro templates, intro,
        cat appearance, performance, pros/cons, job, strategy/usage
        """
        # this just prevents the parameters being too long
        bold = lambda x: f"'''{x}'''"
        def get_perf():
            """Gets performance section"""

            abils = [self.stats.get_abilities(self.ls[k], 2) for k in
                     range(3 if self.tf else 2)]
            perf = list(dict.fromkeys([ability for form in
                                       abils for ability in form]))

            def move(element) -> None:
                """Moves element to the back of the list"""
                for x in perf:
                    if element in x:
                        perf.sort(key=x.__eq__)

            for p in range(len(perf)):
                has = lambda index: perf[p] in abils[index]
                try:
                    if has(0) and not (has(1) or has(2)):
                        perf[p] += f' {bold("[Normal]")}'
                    if self.tf and has(2):
                        if not (has(0) or has(1)):
                            perf[p] += f' {bold("[True]")}'
                        elif not has(0) and has(1):
                            perf[p] += f' {bold("[Evolved/True]")}'
                    elif has(1) and not has(0):
                        perf[p] += f' {bold("[Evolved]")}'
                    else:
                        continue
                except IndexError:
                    pass

            move('[True]')
            move('Immune to')
            move(f'{bold("-")} ')
            perf = '<br>\n'.join(perf) + ('\n\n' if perf else '')
            # WTF this is such a disaster :skull:
            # oh well at least this works for some units
            return round2(perf)

        if self.r[8]:
            for i in range(5):
                if i + 167 in self.r[8]:
                    item = "[[Catfruit#Behemoth Stones|Behemoth Stones]]"
                    break
                if i == 4: item = "[[Catfruit]]"
        if self.gacha or self.r[0] == 'Uber Rare':
            if self.gacha is None: self.gacha = "[TODO]"
            cond = f'obtained by playing the [[Cat Capsule#Rare Cat Capsule|' \
                   f'Rare Cat Capsule]]' \
                   f'{f" during the {self.gacha}" if self.r[0] == "Uber Rare" else ""}'

        elif self.drop: cond = f'unlocked when beating [Stage]'
        else: cond = "obtained by [TODO]"

        def image(num: int) -> str:
            """Takes image ID and converts into wikitext"""
            if self.isEgg and num == 1:
                im = f"M 000.png"
            elif self.r[7] == current_ver:
                im = f"placeholder.png"
            else:
                im = f'{self.ID:03} {num}.png'

            return f"|image{num} = " + im + "\n"


        limited = "{{LimitedContent}}\n{{Stub}}\n" if self.r[7] == current_ver else ''

        start = f"{bold(self.names[1])} is a{'n' if self.r[0] == 'Uber Rare' else ''}" \
                f" [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]] that can be {cond}" + \
                (f'. It was added in [[Version {self.r[7]} Update|'
                f'Version {self.r[7]}]]' if self.r[7] != '5.1' else '') + ".\n\n"

        catapp = f"{'{{'}Cat Appearance\n" \
                 f"|Cat Unit Number = {self.ID}\n" \
                 f"|cat category = [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]]" \
                 f"{' ([[:Category:Legend Cats|Legend]])' if self.isLegend else ''}\n" \
                 f"|Normal Form name = {self.names[1]}\n" \
                 f'|Evolved Form name = {self.names[2]}' \
                 f'{f"{br}|True Form name = {self.names[3]}" if self.tf else ""}\n' \
                 f"{image(1)}{image(2)}" \
                 f"{f'{image(3)}' if self.tf else ''}" + "}}\n\n"

        true_evol = f"\n\nEvolves into {bold(self.names[3])} at level 30 using " \
                    f"{item} and XP." if self.r[8] else ''

        evol = f"==Evolution==\n" \
               f"Evolves into {bold(self.names[2])} at level 10." \
               f"{true_evol}\n\n" \
               f"==Performance==\n" \
               f"{get_perf()}" + \
                    f"===Pros===\n*?\n\n" \
                    f"===Cons===\n*?\n" + \
               "{{Job|Classification = N/A}}\n\n" \
               "==Strategy/Usage==\n-\n\n"

        return limited + start + catapp + evol


    def getTranslation(self) -> str:
        """
        Method that writes the translation template
        """
        # if egg, use default egg image otherwise use its respective image
        image = lambda id, num: \
            f'|image{num} = Uni{self.ID:03} {id}00.png\n'\
                if not self.isEgg or num != 1 else f'|image{num} =' \
                                                   f' Uni000 m00.png\n'


        return "==Description==\n{{Translation\n" + \
                f"|Cat Unit Number = {self.ID}\n" \
                f"|cat category = [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]]\n" \
                f"|Normal Form name = {self.names[1]}\n" \
                f"{image('f', 1)}" \
                f"|cat_endesc1 = {self.en_desc[1]}\n" \
                f"|Evolved Form name = {self.names[2]}\n" \
                f"{image('c', 2)}" \
                f"|cat_endesc2 = {self.en_desc[2]}\n" + \
                (f'|Third Form name = {self.names[3]}\n'
                 f"{image('s', 3)}"
                 f'|cat_endesc3 = {self.en_desc[3]}\n' if self.tf else '') + \
                f"|Normal Form name (JP) = {self.desc[0]} (?, ?)\n" \
                f"|cat_jpscript1 = {self.desc[3]}\n" \
                f"|cat_jpdesc1 = ?\n" \
                f"|Evolved Form name (JP) = {self.desc[1]} (?, ?)\n" \
                f"|cat_jpscript2 = {self.desc[4]}\n" \
                f"|cat_jpdesc2 = ?" + \
                (f'{br}|Third Form name (JP) = {self.desc[2]} (?, ?)\n'
                 f'|cat_jpscript3 = {self.desc[5]}\n'
                 f'|cat_jpdesc3 = ?' if self.tf else '') + "\n}}\n\n"


    def getCost(self) -> str:
        """
        Method that writes the in-game cost and XP costs
        """
        # level 1 xp upgrade costs
        defaults = {
            "2000": 'EX1',
            "3500": 'EX2',
            "2500": 'EX3',
            "5600": 'EX4',
            "5740": 'EX5',
            "8000": 'RR',
            "8200": 'SR',
            "9800": 'temp', # Uber Rare/Legend Rare/Legend Cats
        }
        form1, form2 = '', ''
        # for cost
        cost = [i[6] for i in self.ls]
        compare = lambda a, b: cost[a] == cost[b]
        if not compare(0, 1) and compare(1, 2):
            form1, form2 = 'Normal', f'Evolved{"/True" if self.tf else ""}'
        elif compare(0, 1) and not compare(1, 2):
            form1, form2 = 'Normal/Evolved', 'True'
        # I have not seen a case where all 3 forms have different costs, so...
        if not form2:
            costs = f"*Chapter 1: {cost[0]:,}¢\n" \
                    f"*Chapter 2: {int(cost[0] * 1.5):,}¢\n" \
                    f"*Chapter 3: {cost[0] * 2:,}¢\n"
        else:
            costs = f"==={form1} Form===\n" \
                    f"*Chapter 1: {cost[0]:,}¢\n" \
                    f"*Chapter 2: {int(cost[0] * 1.5):,}¢\n" \
                    f"*Chapter 3: {cost[0] * 2:,}¢\n\n" \
                    f"==={form2} Form===\n" \
                    f"*Chapter 1: {cost[2]:,}¢\n" \
                    f"*Chapter 2: {int(cost[2] * 1.5):,}¢\n" \
                    f"*Chapter 3: {cost[2] * 2:,}¢\n"

        # for XP upgrade template
        if self.catRarity[3] in defaults:
            if self.catRarity[3] == "9800":
                if not self.isLegend:
                    upgrade = "UR" if self.catRarity[13] == '4' else "LR"
                else: upgrade = "EXL"
            else:
                upgrade = defaults[self.catRarity[3]]
        else:
            last = commarise(int(self.catRarity[2]) * 2)
            upgrade = f"MIX\n|{commarise(int(self.catRarity[1]))}\n" + \
                      '\n'.join([f"|{commarise(int(self.catRarity[i + 3]))}"
                                 for i in range(9)]) + f'\n|{last}\n' \
                                                       f'|max = {self.r[1]}\n'
        # this gives a mix of XP as given in the rarity list
        return "==Cost==\n" + costs + f"{'{{'}Upgrade Cost|{upgrade}{'}}'}\n\n"


    def getTables(self, a: list) -> str:
        """Gets the standard/detailed stat tables of the cat"""
        tables = []
        n = self.r[0] == "Normal" # is cat a Normal Cat

        def comparison(lis: list, key: int, other: str = '') -> list:
            """A super compact version of the old compare function"""
            stats = {
                0: ("HP Initial",),
                1: ("Knockback",),
                2: ("Movement Speed",),
                3: ("AP Initial",),
                4: ("Attack Frequency",),
                5: ("Attack Range",),
                6: ("Ch1", "Ch2", "Ch3"),
                7: ("Recharge Time",),
                8: ("DPS Initial",),
                12: ("Target",)
            }
            if key not in stats: return [''] * 2
            if other == 'an':
                stats[1] = "Attack Animation",
            elif other == 'd':
                stats[0] = "DPS Initial",
            elif other == 'pre_d':
                stats[0] = "DPS Initial Precise",
            s = lambda x, y: commarise((x / 2 + 1) * lis[y + 1][key]
                                       if key == 6 else lis[y + 1][key])

            return ["" if lis[j][key] == lis[j + 1][key] else
                    ''.join([f"\n|{stats[key][i]} "
                             f"{'Evolved' if j == 0 else 'True'} = {s(i, j)}"
                             for i in range(3 if key == 6 else 1)])
                    for j in range(2)]

        def mult(ls: list, a_ls: list, form: int) -> list:
            """
            :param ls: ability list
            :param a_ls: animation list, contains atk freq and backswing
            :param form: stat to target
            :return: multi hit stats
            """
            try:
                if ls[59] != 0 and ls[60] == 0:
                    stat = [ls[3] + ls[59],
                            f"{a_ls[form]-ls[13] - a_ls[form+3]}f + {ls[13]}f + "
                            f"{ls[61]-ls[13]}f + {a_ls[form+3]-(ls[61]-ls[13])}f",
                            a_ls[form + 3] - (ls[61] - ls[13])]
                    # for 2 hits

                elif ls[59] != 0 and ls[60] != 0:
                    stat = [ls[3] + ls[59] + ls[60],
                            f"{a_ls[form] - ls[13] - a_ls[form + 3]}f +"
                            f" {ls[13]}f + {ls[61] - ls[13]}f"
                            f" + {ls[62] - ls[61]}f + "
                            f"{a_ls[form + 3] - (ls[62] - ls[13])}f",
                            a_ls[form + 3] - (ls[62] - ls[13])]
                    # for 3 hits

                else:
                    raise IndexError
                    # for only 1 hit

            except (IndexError, TypeError):
                stat = [ls[3],
                        f"{a_ls[form] - ls[13] - a_ls[form + 3]}f + "
                        f"{ls[13]}f + {a_ls[form + 3]}f",
                        a_ls[form + 3]]
                # for only 1 hit, try except because some files
                # have long lists while others do not
            return stat
            # format: stat = [total attack damage,
            #                 formatted animation,
            #                 actual backswing]

        c = self.ls.copy()
        repeated = [comparison(c, i) for i in range(13)]

        atks = [mult(c[i], a, i) for i in range(3)]
        anim = comparison(atks, 1, other="an")
        # for attack animation

        dps_list = [[math.floor(atks[i][0]/(a[i]/30))] for i in range(3)]
        # list of initial DPS
        preDPS_list = [[f'{"{{"}#expr:{atks[j][0]}/'
                        f'({a[j]}/30){"}}"}'] for j in range(3)]
        # list of formatted precise DPS

        repeatedDPS = comparison(dps_list, 0, other="d")
        repeatedpreDPS = comparison(preDPS_list, 0, other="pre_d")
        # for DPS

        def calcStats(initial: int, level: int):
            if level <= self.rps[0]:
                return math.floor(2.5 * round(initial * ((level + 4) / 5)))
            else:
                if len(self.rps) == 1 or level <= self.rps[1]:
                    return math.floor(2.5 *
                                      round(initial *
                                            ((self.rps[0] + 4) / 5 +
                                             (level - self.rps[0])/ 10)))
                else:
                    return math.floor(2.5 *
                                      round(initial *
                                            ((self.rps[0] + 4) / 5 +
                                             (self.rps[1] - self.rps[0]) / 10 +
                                             (level - self.rps[1]) / 20)))
        max_lvl = self.r[1] + self.r[2]

        left = '<' # '&lt;'
        pipe = '|' # '&#124;'
        # this is pretty much impossible to read at this point but w/e
        table_ls = []

        form_max = f'{self.r[1]}{f"+{self.r[2]}" if self.r[2] != 0 else ""}'

        statslevels = "" if not n else f"\n|1st stats Level = {form_max}" + \
                                       f"\n|2nd stats Level = {form_max}" + \
            (f"\n|3rd stats Level = {form_max}" if self.tf else "")


        for i in range(3 if self.tf else 2):
            ind = ['normal', 'evolved', 'third'][i]

            c[i][4] = a[i]
            c[i][7] = f"{c[i][7]} ~ " \
                         f"{round(c[i][7] - 8.8, 2) if c[i][7] > 10.8 else 2}" \
                         f" seconds"
            c[i][12] = "Single Target" if c[i][12] == 0 else "Area Attack"

            DPS = round((atks[i][0] if i == 0 else
                         calcStats(atks[i][0], max_lvl if n else 30)) / (a[i] / 30), 2)
            atk = f"{atks[i][0] if i == 0 else calcStats(atks[i][0], max_lvl if n else 30):,}"
            hp = f"{c[i][0] if i == 0 else calcStats(c[i][0], max_lvl if n else 30):,}"

            table_ls.append(f'|{ind.capitalize()} Form name = {self.names[i + 1]}\n'
                f'|Hp {ind} = {hp} HP\n'
                f'|Atk Power {ind} = {atk} damage<br>({DPS:,} DPS)\n'
                f'|Atk Range {ind} = {c[i][5]:,}\n'
                f'|Attack Frequency {ind} = '
                            f'{a[i]:,}f <sub>{round(a[i] / 30, 2)} seconds</sub>\n'
                f'|Movement Speed {ind} = {c[i][2]}\n'
                f'|Knockback {ind} = {c[i][1]} time{"s" if c[i][1] > 1 else ""}\n'
                f'|Attack Animation {ind} = '
                            f'{c[i][13]}f <sup>{round(c[i][13] / 30, 2)}s</sup>'
                f'<br>({atks[i][2]}f <sup>'
                            f'{round(atks[i][2] / 30, 2)}s</sup> backswing)\n'
                f'|Recharging Time {ind} = {c[i][7]}\n' +
                (f"|Hp normal Lv.MAX = {calcStats(c[i][0], max_lvl if n else 30):,} HP\n"
                 f"|Atk Power normal Lv.MAX = "
                 f"{calcStats(atks[0][0], max_lvl if n else 30):,} damage<br>"
                 f"({round(calcStats(atks[0][0], max_lvl if n else 30) / (a[i] / 30), 2):,}"
                 f" DPS){br}" if i == 0 else "") +
                f'|Attack type {ind} = {c[i][12]}\n'
                f'|Special Ability {ind} = {self.stats.get_abilities(c[i], 0)}')

        tables.append(f"==Stats==\n"
                      f"<tabber>\n"
                      f"Standard=\n"
                      f"{'{{'}Cat Stats\n" +
                      '\n'.join(table_ls) +
                      f'\n|Lv.MAX = Lv.{form_max}' +
                      f'{statslevels}'
                      f'\n{"}}"}')

        tables.append(f'{pipe}-|Detailed=\n{"{{"}Calcstatstable{self.r[4]}\n'
            f'|Max Natural Level = {self.r[1]}{self.r[5]}\n'
            f'|Basic Form Name = {self.names[1]}\n'
            f'|HP Initial Normal = '
                      f'{c[0][0]:,}\n'
            f'|AP Initial Normal = {atks[0][0]:,}\n'
            f'|DPS Initial Normal = {round(atks[0][0] / a[0] * 30)}\n'
            f'|DPS Initial Precise Normal = '
                      f'{"{{"}#expr:{(atks[0][0])}/({a[0]}/30){"}}"}\n'
            f'|HP Normal lvl 10 = {calcStats(c[0][0], 10):,}\n'
            f'|AP Normal lvl 10 = {calcStats(atks[0][0], 10):,}\n'
            f'|DPS Normal lvl 10 = '
                      f'{round(calcStats(atks[0][0], 10) / a[0] * 30):,}\n'
            f'|HP Normal lvl.MAX = {calcStats(c[0][0], max_lvl):,}\n'
            f'|AP Normal lvl.MAX = {calcStats(atks[0][0], max_lvl):,}\n'
            f'|DPS Normal lvl.MAX = '
                      f'{round(calcStats(atks[0][0], max_lvl) / a[0] * 30):,}\n'
            f'|Attack Frequency Normal = {a[0]}\n'
            f'|Attack Animation Normal = {atks[0][1]}\n'
            f'|Attack Range Normal = {c[0][5]:,}\n'
            f'|Target Normal = {c[0][12]}\n'
            f'|Recharge Time Normal = {c[0][7]}\n'
            f'|Knockback Normal = {c[0][1]}\n'
            f'|Movement Speed Normal = {c[0][2]}\n'
            f'|Ch1 Normal = {c[0][6]:,}\n'
            f'|Ch2 Normal = {int(c[0][6] * 1.5):,}\n'
            f'|Ch3 Normal = {c[0][6] * 2:,}\n'
            f'|Special Ability Normal = {self.stats.get_abilities(c[0], 1)}\n'
            f'|Evolved Form Name = {self.names[2]}{repeated[0][0]}'
            f'{repeated[3][0]}{repeatedDPS[0]}{repeatedpreDPS[0]}\n'
            f'|HP Evolved lvl 20 = {calcStats(c[1][0], 20):,}\n'
            f'|AP Evolved lvl 20 = {calcStats(atks[1][0], 20):,}\n'
            f'|DPS Evolved lvl 20 = '
                      f'{round(calcStats(atks[1][0], 20) / a[1] * 30):,}\n'
            f'|HP Evolved lvl.MAX = {calcStats(c[1][0], max_lvl):,}\n'
            f'|AP Evolved lvl.MAX = {calcStats(atks[1][0], max_lvl):,}\n'
            f'|DPS Evolved lvl.MAX = '
                      f'{round(calcStats(atks[1][0], max_lvl) / a[1] * 30):,}'
            f'{repeated[4][0]}{anim[0]}{repeated[5][0]}'
            f'{repeated[12][0]}{repeated[7][0]}'
            f'{repeated[1][0]}{repeated[2][0]}{repeated[6][0]}\n'
            f'|Special Ability Evolved = {self.stats.get_abilities(c[1], 1)}\n' + \
            (f'{"}}"}\n{left}/tabber>' if not self.tf else
            f'|True Form Name = {self.names[3]}{repeated[0][1]}'
            f'{repeated[3][1]}{repeatedDPS[1]}{repeatedpreDPS[1]}\n'
            f'|HP True lvl 30 = {calcStats(c[2][0], 30):,}\n'
            f'|AP True lvl 30 = {calcStats(atks[2][0], 30):,}\n'
            f'|DPS True lvl 30 = '
            f'{round(calcStats(atks[2][0], 30) / a[2] * 30):,}\n'
            f'|HP True lvl.MAX = {calcStats(c[2][0], max_lvl):,}\n'
            f'|AP True lvl.MAX = {calcStats(atks[2][0], max_lvl):,}\n'
            f'|DPS True lvl.MAX = '
            f'{round(calcStats(atks[2][0], max_lvl) / a[2] * 30):,}'
            f'{repeated[4][1]}{anim[1]}{repeated[5][1]}'
            f'{repeated[12][1]}{repeated[7][1]}{repeated[1][1]}'
            f'{repeated[2][1]}{repeated[6][1]}\n'
            f'|Special Ability True = {self.stats.get_abilities(c[2], 1)}\n'
            f'{"}}"}\n{left}/tabber>'))

        return round2('\n\n'.join(tables))


    def getCatfruit(self) -> str:
        """
        Method that writes the catfruit section
        """
        cfList = self.r[8]
        if not cfList: return ''
        else:
            catfruits = {
            30:     "PurpleSeed",
            31:     "RedSeed",
            32:     "BlueSeed",
            33:     "GreenSeed",
            34:     "YellowSeed",
            35:     "PurpleFruit",
            36:     "RedFruit",
            37:     "BlueFruit",
            38:     "GreenFruit",
            39:     "YellowFruit",
            40:     "RainbowFruit",
            41:     "AncientSeed",
            42:     "AncientFruit",
            43:     "RainbowSeed",
            44:     "GoldenFruit",
            160:    "AkuSeed",
            161:    "AkuFruit",
            164:    "GoldenSeed",
            167:    "PurpleStone",
            168:    "RedStone",
            169:    "BlueStone",
            170:    "GreenStone",
            171:    "YellowStone",
            179:    "PurpleGem",
            180:    "RedGem",
            181:    "BlueGem",
            182:    "GreenGem",
            183:    "YellowGem",
            184:    "RainbowStone"
            }

        fruits = [catfruits[cfList[i]] for i in
                  range(len(cfList)) if cfList[i] != 0 and i % 2 == 1]
        # list of catfruits
        quant = [cfList[j] for j in
                 range(len(cfList)) if cfList[j] != 0 and j % 2 == 0]
        # list of xp + quantities of catfruit
        catfruit = [f"|Catfruit{k + 1} = {fruits[k]}" for k in
                    range(len(fruits))]
        quantity = [f"|Quantity Catfruit{l + 1} = x{quant[l + 1]}" for l in
                    range(len(fruits))]
        return "\n\n==Catfruit Evolution==\n{{Catfruit Evolution\n" +\
               '\n'.join(catfruit) + '\n' \
               + '\n'.join(quantity) + f"\n|Quantity XP = {quant[0]:,}" + "\n}}"


    @staticmethod
    def getTalent(talents: tuple) -> str:
        """Writes the talents section"""
        if not talents:
            return ''
        else:
            t_ls, nor, ult = talents
            # talent list, no. normal talents, no. ultra talents
            txt = f"\n\n===Ultra Talents===\n" \
                  f"*{f'{br}*'.join(t_ls[nor:len(t_ls)])}" if ult != 0 else ""

            return round2(f"\n\n==Talents==\n"
                            f"*{f'{br}*'.join(t_ls[0:nor])}{txt}")


    def getEnd(self) -> str:
        """
        Method that writes the appearance, gallery, reference,
        and previous/next page links
        """
        ver = self.r[7]
        names = opencsv(DIR + "/catNames.tsv", header=True, delim="\t")

        prev_cat = f"[[{names[self.ID - 1][4]}|&lt;&lt; {names[self.ID - 1][1]}" \
                   f"]]" if names[self.ID - 1][1] != "N/A" else "&lt;&lt; N/A"

        next_cat = f"[[{names[self.ID + 1][4]}|{names[self.ID + 1][1]} &gt;&gt;" \
                   f"]]" if names[self.ID + 1][1] != "N/A" else "N/A &gt;&gt;"

        image = lambda: f"000 m00" if self.isEgg else f"{self.ID:03} f00"
        appearance = f"\n\n==Appearance==\n*Normal Form: ?\n*Evolved Form: " \
                     f"?{f'{br}*True Form: ?' if self.tf else ''}\n\n" + \
                     "{{Gallery|Uni" + f"{image()}" + "}}" + "\n\n"

        reference = f'==Reference==\n' \
                    f'*https://battlecats-db.com/unit/{self.ID + 1:03}.html\n\n'

        try:
            collab = "{{" + \
                     re.compile('(?<=\[\[)(.*)(?= Collab)'
                                ).findall(self.gacha)[0] + \
                     "}}\n"
        except (IndexError, TypeError):
            collab = ""

        end = f'----\n<p style="text-align:center;">' \
              f'[[Cat Release Order|Units Release Order]]:</p>\n\n' + \
              f"<p style=\"text-align:center;\">'''" \
              f"{prev_cat} | {next_cat}" \
              f"'''</p>\n----\n\n{collab}" \
              "{{Cats}}\n"

        return appearance + reference + end


    def getCategories(self, ts) -> str:
        """
        Method that writes the categories
        """
        l = [[i for i in self.ls[j]] for j in range(3)]
        # mutable piece of f****** s*** ***k
        for ls in l:
            if type(ls[-1]) != int: ls.pop(-1)
        for obj in l:
            try:
                if obj[12] == "Single Target":
                    obj[8] = 1 # flag for single/area attacks
                    obj[12] = 0
                if obj[45] < 0: obj[45] = 0 # flag for omni strike
                if obj[35] != 0 and (len(obj) < 95 or obj[94] != 1): obj[36] = 0
                # flag for mini-wave
                if obj[86] != 0 and (len(obj) < 109 or obj[108] != 1): obj[87] = 0
                # flag for mini-wave
            except IndexError:
                continue
        lis = [[i for i in range(len(l[j])) if
                l[j][i] not in [-1, 0]] for j in range(3)]
        # lis is a list of lists of indices where data is not 0
        # if there is only a single line,
        # there is no need for another list comprehension

        data = list(set([item for sublist in lis for item in sublist]))
        data.sort()
        addcat = lambda ca: categories.append([ca])
        categories = [["Cat Units", f"{self.r[0]} Cats"]]

        if self.isEgg:
            addcat("Ancient Eggs")
        if self.isCrazed:
            addcat("Crazed Cats")
        if self.isLegend:
            addcat("Legend Cats")
        if self.isCollab:
            addcat("Collaboration Event Cats")
        if self.gacha or self.r[0] == "Uber Rare" and not self.ID in [53, 155]:
            addcat("Gacha Cats")
        elif self.drop: addcat("Item Drop Cats")

        anti_traits = {
            10:     "Anti-Red Cats",
            16:     "Anti-Floating Cats",
            17:     "Anti-Black Cats",
            18:     "Anti-Metal Cats",
            19:     "Anti-Traitless Cats",
            20:     "Anti-Angel Cats",
            21:     "Anti-Alien Cats",
            22:     "Anti-Zombie Cats",
            78:     "Anti-Relic Cats",
            96:     "Anti-Aku Cats"
        }
        categories.append([anti_traits[i] for i in anti_traits if i in data])
        attack_types = {
             8:     "Single Target Cats",
            12:     "Area Attack Cats",
            44:     "Long Distance Cats",
            59:     "Multi-Hit Cats",
            99:     "Cats with different effective ranges"
        }
        if 44 in data and 45 not in data: attack_types[44] = "Omni Strike Cats"
        categories.append([attack_types[i] for i in attack_types if i in data])
        abilities = {
            23:     "Cats with Strong ability",
            24:     "Cats with Knockback ability",
            25:     "Cats with Freeze ability",
            27:     "Cats with Slow ability",
            29:     "Cats with Resistant ability",
            30:     "Cats with Massive Damage ability",
            31:     "Critical Hit Cats",
            32:     "Focused Target Cats",
            33:     "Cats with Extra Money ability",
            34:     "Base Destroyer Cats",
            35:     "Mini-Wave Cats",
            37:     "Cats with Weaken ability",
            40:     "Cats with Strengthen ability",
            42:     "Lethal Strike Resistant Cats",
            43:     "Cats with Metal ability",
            47:     "Wave Shield Cats",
            52:     "Zombie Killer Cats",
            53:     "Witch Killer Cats",
            58:     "Kamikaze Cats",
            70:     "Barrier Breaker Cats",
            77:     "Eva Angel Killer Cats",
            80:     "Cats with Insanely Tough ability",
            81:     "Cats with Insane Damage ability",
            82:     "Savage Blow Cats",
            84:     "Cats with Dodge Attack ability",
            86:     "Mini-Surge Cats",
            92:     "Cats with Curse ability",
            95:     "Shield Piercing Cats",
            97:     "Colossus Slayer Cats",
            98:     "Soulstrike Cats",
            105:    "Behemoth Slayer Cats"
        }
        if 35 in data and 36 not in data: abilities[35] = "Wave Attack Cats"
        if 86 in data and 87 not in data: abilities[86] = "Surge Attack Cats"
        categories.append([abilities[i] for i in abilities if i in data])
        immunities = {
            46:     "Cats with Wave Immunity",
            48:     "Cats with Knockback Immunity",
            49:     "Cats with Freeze Immunity",
            50:     "Cats with Slow Immunity",
            51:     "Cats with Weaken Immunity",
            75:     "Warp Blocker Cats",
            79:     "Cats with Curse Immunity",
            90:     "Cats with Toxic Immunity",
            91:     "Cats with Surge Immunity"
        }
        categories.append([immunities[i] for i in immunities if i in data])

        if self.getCatfruit() != '':
            for i in range(5):
                if i + 167 in self.r[8]:
                    addcat("Cats require Behemoth Stones for True Form")
                    break
                if i == 4: addcat("Cats require Catfruits for True Form")

        talents = opencsv(DIR + "/talents.csv")

        def categories_has(element: str) -> bool:
            """
            Checks if there already exists a particular
            category before adding it
            """
            for i, sublist in enumerate(categories):
                if element in sublist:
                    return True
            return False
        if self.tals:
            addcat("Cats with Talents")
            tal_num = len([i for i in range(len(self.tals)) if self.tals[i][0][0] != 0])
            categories.append([talents[self.tals[i][0][0]][2] for i in
                               range(tal_num) if not
                           categories_has(talents[self.tals[i][0][0]][2])])
            if ts[2] != 0:
                addcat("Cats with Ultra Talents")
        # adds talent categories at the end of the list
        # if there are talents
        if self.r[7] == current_ver: addcat("Translation requests")
        cates = [f"[[Category:{category}]]" for types in
                 categories for category in types]
        return '\n'.join(cates)