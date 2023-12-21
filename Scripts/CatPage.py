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

    def __init__(self, ID: int, is_new: bool):
        super().__init__(ID)
        if self.ID == -1:
            return
        self.stats = StatsCommon()
        self.tf = self.trueForm
        self.uf = self.ultraForm
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
        self.is_new = is_new
        if self.r[0] in ["Normal", "Special"]:
            self.rps = [60]
        elif self.r[0] in ["Super Rare", "Uber Rare", "Legend Rare"]:
            self.rps = [60, 80]
        else:
            self.rps = [70, 90]

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

            abils = [self.stats.get_abilities(self.ls[k], 2, link=self.names[-2]) for k in
                     range(self.form)]
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
            elif self.is_new:
                im = f"placeholder.png"
            else:
                im = f'{self.ID:03} {num}.png'

            return f"|image{num} = " + im + "\n"


        limited = "{{LimitedContent}}\n{{Stub}}\n" if self.is_new else ''

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
                 f'{f"{br}|True Form name = {self.names[3]}" if self.tf else ""}\n'\
                 f'{f"|Ultra Form name = {self.names[4]}{br}" if self.uf else ""}'\
                 f"{image(1)}{image(2)}" \
                 f"{f'{image(3)}' if self.tf else ''}" \
                 f"{f'{image(4)}' if self.uf else ''}" + "}}\n\n"

        tu_evol = f"\n\nEvolves into {bold(self.names[3])} at level 30 using " \
                    f"{item} and XP.%s" if self.r[8] else ''

        ultra_evol = f"\n\nEvolves into {bold(self.names[4])} at level 60" \
                     f" using [[Catfruit]], " \
                    f"[[Catfruit#Behemoth Stones|Behemoth Stones]]" \
                     f" and XP." if self.uf else ''

        evol = f"==Evolution==\n" \
               f"Evolves into {bold(self.names[2])} at level 10." \
               f"{tu_evol.replace('%s', ultra_evol)}\n\n" \
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
               (f'|Fourth Form name = {self.names[4]}\n'
                f"{image('u', 4)}"
                f'|cat_endesc4 = {self.en_desc[3]}\n' if self.uf else '') + \
               f"|Normal Form name (JP) = {self.desc[0][0]} (?, ?)\n" \
                f"|cat_jpscript1 = {self.desc[1][0]}\n" \
                f"|cat_jpdesc1 = ?\n" \
                f"|Evolved Form name (JP) = {self.desc[0][1]} (?, ?)\n" \
                f"|cat_jpscript2 = {self.desc[1][1]}\n" \
                f"|cat_jpdesc2 = ?" + \
                (f'{br}|Third Form name (JP) = {self.desc[0][2]} (?, ?)\n'
                 f'|cat_jpscript3 = {self.desc[1][2]}\n'
                 f'|cat_jpdesc3 = ?' if self.tf else '') + \
                (f'{br}|Fourth Form name (JP) = {self.desc[0][3]} (?, ?)\n'
                 f'|cat_jpscript4 = {self.desc[1][3]}\n'
                 f'|cat_jpdesc4 = ?' if self.uf else '') + "\n}}\n\n"


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
        # I have not seen a case where all 3 forms have different costs, so...
        if not compare(0, 1) and compare(1, 2):
            form1, form2 = 'Normal', f'Evolved{"/True" if self.tf else ""}'
        elif compare(0, 1) and not compare(1, 2):
            form1, form2 = 'Normal/Evolved', 'True'

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
            # this gives a mix of XP as given in the rarity list
            upgrade = f"MIX\n|{commarise(int(self.catRarity[1]))}\n" + \
                      '\n'.join([f"|{commarise(int(self.catRarity[i + 3]))}"
                                 for i in range(9)]) + f'\n|{last}\n' \
                                                       f'|max = {self.r[1]}\n'

        return "==Cost==\n" + costs + f"{'{{'}Upgrade Cost|{upgrade}{'}}'}\n\n"


    def getTables(self, a: list) -> str:
        """Gets the standard/detailed stat tables of the cat"""
        tables = []

        def mult(ls: list, a_ls: list, form: int) -> list:
            """
            :param ls: ability list
            :param a_ls: animation list, contains atk freq and backswing
            :param form: stat to target
            :return: multi hit stats

            """
            # format: stat = [total attack damage,
            #                 formatted animation,
            #                 actual backswing]
            try:
                if ls[59] != 0 and ls[60] == 0:
                    # for 2 hits
                    stat = [ls[3] + ls[59],
                            f"{a_ls[0][form]-ls[13] - a_ls[1][form]}f + {ls[13]}f + "
                            f"{ls[61]-ls[13]}f + {a_ls[1][form]-(ls[61]-ls[13])}f",
                            a_ls[1][form] - (ls[61] - ls[13])]

                elif ls[59] != 0 and ls[60] != 0:
                    # for 3 hits
                    stat = [ls[3] + ls[59] + ls[60],
                            f"{a_ls[0][form] - ls[13] - a_ls[1][form]}f +"
                            f" {ls[13]}f + {ls[61] - ls[13]}f"
                            f" + {ls[62] - ls[61]}f + "
                            f"{a_ls[1][form] - (ls[62] - ls[13])}f",
                            a_ls[1][form] - (ls[62] - ls[13])]

                else:
                    # for only 1 hit
                    raise IndexError

            except (IndexError, TypeError):
                # for only 1 hit, try except because some files
                # have long lists while others do not
                stat = [ls[3],
                        f"{a_ls[0][form] - ls[13] - a_ls[1][form]}f + "
                        f"{ls[13]}f + {a_ls[1][form]}f",
                        a_ls[1][form]]
            return stat

        n = self.r[0] == "Normal" # is cat a Normal Cat
        max_lvl = self.r[1] + self.r[2]
        c = self.ls.copy()
        atks = [mult(c[i], a, i) for i in range(self.form)]

        def calcStats(initial: int, level: int):
            """Calculates stats at a certain level given initial"""
            if level <= self.rps[0]:
                # before first reduction point
                return math.floor(2.5 * round(initial * ((level + 4) / 5)))
            else:
                # between first and second reduction point
                if len(self.rps) == 1 or level <= self.rps[1]:
                    return math.floor(2.5 *
                                      round(initial *
                                            ((self.rps[0] + 4) / 5 +
                                             (level - self.rps[0])/ 10)))
                else:
                    # after second reduction point
                    return math.floor(2.5 *
                                      round(initial *
                                            ((self.rps[0] + 4) / 5 +
                                             (self.rps[1] - self.rps[0]) / 10 +
                                             (level - self.rps[1]) / 20)))


        def comparison(lis: list, key: int, other: str = '') -> list:
            """A super compact version of the old compare function"""
            stats = {
                0:      ("HP Initial %",),
                1:      ("Knockback %",),
                2:      ("Movement Speed %",),
                3:      ("AP Initial %",),
                4:      ("Attack Frequency %",),
                5:      ("Attack Range %",),
                6:      ("Ch1 %", "Ch2 %", "Ch3 %"),
                7:      ("Recharge Time %",),
                8:      ("DPS Initial %",),
                12:     ("Target %",),
                13:     ("HP % lvl.MAX",),
                14:     ("AP % lvl.MAX",),
                15:     ("DPS % lvl.MAX",),
            }
            if key not in stats: return [''] * 2
            if other == 'an':
                stats[1] = "Attack Animation %",
            elif other == 'd':
                stats[0] = "DPS Initial %",
            elif other == 'pre_d':
                stats[0] = "DPS Initial Precise %",

            def s(x: int, y: int):
                """Returns appropriate value corresponding to key"""
                if key == 3:
                    return atks[y + 1][0]
                elif key == 4: # atk freq
                    return a[0][y + 1]
                elif key == 6: # costs
                    return commarise((x / 2 + 1) * lis[y + 1][key])
                elif key == 7: # recharge time
                    return f'{lis[y + 1][key]:,} ~ ' \
                           f'{float(lis[y + 1][key]) - 8.8:,} seconds'
                elif key == 12: # target
                    return "Single Target" if lis[y+1][key]==0 else "Area Attack"
                elif key == 13:
                    return commarise(calcStats(c[y + 1][0], max_lvl))
                elif key == 14:
                    return commarise(calcStats(atks[y + 1][0], max_lvl))
                elif key == 15:
                    return f'{round(calcStats(atks[y+1][0],max_lvl)/a[0][y+1]*30):,}'
                else:
                    return commarise(lis[y + 1][key])

            def conditions(k):
                """Conditions to check for repetition"""
                # A bit more complex than I initially thought but oh well
                return (
                        (key == 4 and a[0][k] == a[0][k + 1]) or
                        (key == 13 and lis[k][0] == lis[k + 1][0]) or
                        (key in {14, 15} and atks[k][0] == atks[k + 1][0] and
                         (key != 15 or a[0][k] == a[0][k + 1])) or
                        (key not in {4, 13, 14, 15} and
                         lis[k][key] == lis[k + 1][key])
                )

            return ["" if conditions(j) else
                    ''.join([f"\n|{stats[key][i].replace('%', ['Evolved', 'True', 'Ultra'][j])}"
                             f" = {s(i, j)}" for i in range(3 if key == 6 else 1)]) for j in range(self.form - 1)]


        repeated = [comparison(c, i) for i in range(16)]
        anim = comparison(atks, 1, other="an")
        # for attack animation

        dps_list = [[math.floor(atks[i][0]/(a[0][i]/30))] for i in range(self.form)]
        # list of initial DPS
        preDPS_list = [[f'{"{{"}#expr:{atks[j][0]}/'
                        f'({a[0][j]}/30){"}}"}'] for j in range(self.form)]
        # list of formatted precise DPS

        repeatedDPS = comparison(dps_list, 0, other="d")
        repeatedpreDPS = comparison(preDPS_list, 0, other="pre_d")
        # for DPS

        left = '<' # '&lt;'
        pipe = '|' # '&#124;'
        # this is pretty much impossible to read at this point but w/e
        table_ls = []

        form_max = f'{self.r[1]}{f"+{self.r[2]}" if self.r[2] != 0 else ""}'

        statslevels = "" if not n else f"\n|1st stats Level = {form_max}" + \
                                       f"\n|2nd stats Level = {form_max}" + \
            (f"\n|3rd stats Level = {form_max}" if self.tf else "") + \
            (f"\n|4th stats Level = {form_max}" if self.uf else "")


        for i in range(self.form):
            ind = ['normal', 'evolved', 'third', 'fourth'][i]

            c[i][4] = a[0][i]
            c[i][7] = f"{c[i][7]} ~ " \
                         f"{round(c[i][7] - 8.8, 2) if c[i][7] > 10.8 else 2}" \
                         f" seconds"
            c[i][12] = "Single Target" if c[i][12] == 0 else "Area Attack"

            if n: lvl = max_lvl
            elif i == 3: lvl = 60
            else: lvl = 30

            DPS = round((atks[i][0] if i == 0 else
                         calcStats(atks[i][0], lvl))
                        / (a[0][i] / 30), 2)
            atk = f"{atks[i][0] if i == 0 else calcStats(atks[i][0], lvl):,}"
            hp = f"{c[i][0] if i == 0 else calcStats(c[i][0], lvl):,}"

            table_ls.append(f'|{ind.capitalize()} Form name = {self.names[i + 1]}\n'
                f'|Hp {ind} = {hp} HP\n'
                f'|Atk Power {ind} = {atk} damage<br>({DPS:,} DPS)\n'
                f'|Atk Range {ind} = {c[i][5]:,}\n'
                f'|Attack Frequency {ind} = '
                            f'{a[0][i]:,}f <sub>{round(a[0][i] / 30, 2)} seconds</sub>\n'
                f'|Movement Speed {ind} = {c[i][2]}\n'
                f'|Knockback {ind} = {c[i][1]} time{"s" if c[i][1] > 1 else ""}\n'
                f'|Attack Animation {ind} = '
                            f'{c[i][13]}f <sup>{round(c[i][13] / 30, 2)}s</sup>'
                f'<br>({atks[i][2]}f <sup>'
                            f'{round(atks[i][2] / 30, 2)}s</sup> backswing)\n'
                f'|Recharging Time {ind} = {c[i][7]}\n' +
                (f"|Hp normal Lv.MAX = {calcStats(c[i][0], lvl):,} HP\n"
                 f"|Atk Power normal Lv.MAX = "
                 f"{calcStats(atks[0][0], lvl):,} damage<br>"
                 f"({round(calcStats(atks[0][0], lvl) / (a[0][i] / 30), 2):,}"
                 f" DPS){br}" if i == 0 else "") +
                f'|Attack type {ind} = {c[i][12]}\n'
                f'|Special Ability {ind} = {self.stats.get_abilities(c[i], 0, i < 3, link=self.names[-2])}')

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
            f'|DPS Initial Normal = {round(atks[0][0] / a[0][0] * 30)}\n'
            f'|DPS Initial Precise Normal = '
                      f'{"{{"}#expr:{(atks[0][0])}/({a[0][0]}/30){"}}"}\n'
            f'|HP Normal lvl 10 = {calcStats(c[0][0], 10):,}\n'
            f'|AP Normal lvl 10 = {calcStats(atks[0][0], 10):,}\n'
            f'|DPS Normal lvl 10 = '
                      f'{round(calcStats(atks[0][0], 10) / a[0][0] * 30):,}\n'
            f'|HP Normal lvl.MAX = {calcStats(c[0][0], max_lvl):,}\n'
            f'|AP Normal lvl.MAX = {calcStats(atks[0][0], max_lvl):,}\n'
            f'|DPS Normal lvl.MAX = '
                      f'{round(calcStats(atks[0][0], max_lvl) / a[0][0] * 30):,}\n'
            f'|Attack Frequency Normal = {a[0][0]}\n'
            f'|Attack Animation Normal = {atks[0][1]}\n'
            f'|Attack Range Normal = {c[0][5]:,}\n'
            f'|Target Normal = {c[0][12]}\n'
            f'|Recharge Time Normal = {c[0][7]}\n'
            f'|Knockback Normal = {c[0][1]}\n'
            f'|Movement Speed Normal = {c[0][2]}\n'
            f'|Ch1 Normal = {c[0][6]:,}\n'
            f'|Ch2 Normal = {int(c[0][6] * 1.5):,}\n'
            f'|Ch3 Normal = {c[0][6] * 2:,}\n'
            f'|Special Ability Normal = {self.stats.get_abilities(c[0], 1, link=self.names[-2])}\n'
            f'|Evolved Form Name = {self.names[2]}{repeated[0][0]}'
            f'{repeated[3][0]}{repeatedDPS[0]}{repeatedpreDPS[0]}\n'
            f'|HP Evolved lvl 20 = {calcStats(c[1][0], 20):,}\n'
            f'|AP Evolved lvl 20 = {calcStats(atks[1][0], 20):,}\n'
            f'|DPS Evolved lvl 20 = '
                      f'{round(calcStats(atks[1][0], 20) / a[0][1] * 30):,}'
            f'{repeated[13][0]}{repeated[14][0]}{repeated[15][0]}'
            f'{repeated[4][0]}{anim[0]}{repeated[5][0]}'
            f'{repeated[12][0]}{repeated[7][0]}'
            f'{repeated[1][0]}{repeated[2][0]}{repeated[6][0]}\n'
            f'|Special Ability Evolved = {self.stats.get_abilities(c[1], 1, link=self.names[-2])}\n'+ \
            (f'' if not self.tf else
            f'|True Form Name = {self.names[3]}{repeated[0][1]}'
            f'{repeated[3][1]}{repeatedDPS[1]}{repeatedpreDPS[1]}\n'
            f'|HP True lvl 30 = {calcStats(c[2][0], 30):,}\n'
            f'|AP True lvl 30 = {calcStats(atks[2][0], 30):,}\n'
            f'|DPS True lvl 30 = '
            f'{round(calcStats(atks[2][0], 30) / a[0][2] * 30):,}'
            f'{repeated[13][1]}{repeated[14][1]}{repeated[15][1]}'
            f'{repeated[4][1]}{anim[1]}{repeated[5][1]}'
            f'{repeated[12][1]}{repeated[7][1]}{repeated[1][1]}'
            f'{repeated[2][1]}{repeated[6][1]}\n'
            f'|Special Ability True = {self.stats.get_abilities(c[2], 1, link=self.names[-2])}\n') + \
                      (f'' if not self.uf else
                      f'|Ultra Form Name = {self.names[4]}{repeated[0][2]}'
                      f'{repeated[3][2]}{repeatedDPS[2]}{repeatedpreDPS[2]}\n'
                      f'|HP Ultra lvl 60 = {calcStats(c[3][0], 60):,}\n'
                      f'|AP Ultra lvl 60 = {calcStats(atks[3][0], 60):,}\n'
                      f'|DPS Ultra lvl 60 = '
                      f'{round(calcStats(atks[3][0], 60) / a[0][3] * 30):,}'
                      f'{repeated[13][2]}{repeated[14][2]}{repeated[15][2]}'
                      f'{repeated[4][2]}{anim[2]}{repeated[5][2]}'
                      f'{repeated[12][2]}{repeated[7][2]}{repeated[1][2]}'
                      f'{repeated[2][2]}{repeated[6][2]}\n'
                      f'|Special Ability Ultra = '
                      f'{self.stats.get_abilities(c[3], 1, link=self.names[-2])}\n')
                      )

        s = False
        summon = ""
        for i in range(self.form):
            try:
                if int(self.ls[i][110]) > 0:
                    s_id = int(self.ls[i][110])
                    s = True
                    break
            except IndexError:
                break

        if s:
            s_data = [int(i) for i in opencsv(f"{data_mines}/DataLocal/"
                                              f"unit{s_id + 1}.csv")[0]]
            s_anim = self.stats.get_atkanim(s_id, 'f', s_data)

            atk_type = "Single Target" if s_data[12] == 0 else "Area Attack"

            summon = "\n\n==Summon==\n{{SummonStats\n" \
                     f"|Spirit CRO = {s_id:03}\n" \
                     f"|Spirit Image = {s_id:03} 1.png\n" \
                     f"|Spirit HP = {calcStats(s_data[0], 30):,} HP\n" \
                     f"|Spirit Atk = {calcStats(s_data[3], 30):,} damage\n" \
                     f"|Spirit Range = {s_data[5]:,}\n" \
                     f"|Spirit Speed = {s_data[2]:,}\n" \
                     f"|Spirit Knockback = {s_data[1]:,} time{'s' if s_data[1] > 1 else ''}\n" \
                     f"|Spirit Animation = {s_data[13]}f <sup>" \
                     f"{round(s_data[13] / 30, 2)}s</sup><br>({s_anim[0]}f " \
                     f"<sup>{round(s_anim[0] / 30, 2)}s</sup> backswing)\n" \
                     f"|Spirit Target = {atk_type}\n" \
                     f"|Spirit Ability = {self.stats.get_abilities(s_data, 0)}\n" \
                     "}}"


        return round2('\n\n'.join(tables) + f'{"}}"}\n{left}/tabber>') + summon


    def getCatfruit(self) -> str:
        """
        Method that writes the catfruit section
        """
        cfList = self.r[8]
        ufList = self.r[9]
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

        def get_cftemplate(ls):
            fruits = [catfruits[ls[i]] for i in
                      range(len(ls)) if ls[i] != 0 and i % 2 == 1]
            # list of catfruits
            quant = [ls[j] for j in
                     range(len(ls)) if ls[j] != 0 and j % 2 == 0]
            # list of xp + quantities of catfruit
            catfruit = [f"|Catfruit{k + 1} = {fruits[k]}" for k in
                        range(len(fruits))]
            quantity = [f"|Quantity Catfruit{l + 1} = x{quant[l + 1]}" for l in
                        range(len(fruits))]
            return quant, catfruit, quantity

        print(ufList)

        cf = "\n\n==Catfruit Evolution==\n{{Catfruit Evolution\n" + \
               '\n'.join(get_cftemplate(cfList)[1]) + '\n' \
               + '\n'.join(get_cftemplate(cfList)[2]) + \
               f"\n|Quantity XP = {get_cftemplate(cfList)[0][0]:,}" + "\n}}"

        uf = "\n\n===Ultra Form===\n{{Catfruit Evolution\n" + \
               '\n'.join(get_cftemplate(ufList)[1]) + '\n' +  \
               '\n'.join(get_cftemplate(ufList)[2]) + \
               f"\n|Quantity XP = {get_cftemplate(ufList)[0][0]:,}" + "\n}}"

        return cf + (uf if ufList and ufList != cfList else "")


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
        names = opencsv(DIR + "/catNames.tsv", header=True, delim="\t")

        prev_cat = f"[[{names[self.ID - 1][-2]}|&lt;&lt; {names[self.ID - 1][1]}" \
                   f"]]" if names[self.ID - 1][1] != "N/A" else "&lt;&lt; N/A"

        next_cat = f"[[{names[self.ID + 1][-2]}|{names[self.ID + 1][1]} &gt;&gt;" \
                   f"]]" if names[self.ID + 1][1] != "N/A" else "N/A &gt;&gt;"

        image = lambda: f"Uni{self.ID:03} s00.png" if self.isEgg else f"{self.ID:03} f00"
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
        l = [[i for i in self.ls[j]] for j in range(4 if self.uf else 3)]
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
                l[j][i] not in [-1, 0]] for j in range(4 if self.uf else 3)]
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
            105:    "Behemoth Slayer Cats",
            109:    "Counter Surge Cats",
            110:    "Cats with Summon ability",
            111:    "Slayer Cats",
        }
        if 35 in data and 36 not in data: abilities[35] = "Wave Attack Cats"
        if 86 in data and 87 not in data: abilities[86] = "Surge Attack Cats"
        categories.append([abilities[i] for i in abilities if i in data])
        imun = lambda type: f"Cats with {type} Immunity"
        immunities = {
            46:     imun("Wave"),
            48:     imun("Knockback"),
            49:     imun("Freeze"),
            50:     imun("Slow"),
            51:     imun("Weaken"),
            75:     imun("Warp"),
            79:     imun("Curse"),
            90:     imun("Toxic"),
            91:     imun("Surge")
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
        if self.is_new: addcat("Translation requests")
        cates = [f"[[Category:{category}]]" for types in
                 categories for category in types]
        return '\n'.join(cates)