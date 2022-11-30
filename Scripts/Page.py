"""Program that receives input and writes the contents of a page"""
from stats import *
from Cat import Cat

class Page(Cat):

    ID:         int     # Unit ID
    ls:         list    # Ability and stats list
    r:          tuple   # Rarity, max level, catfruit, version tuple
    tf:         bool    # Does unit have true form
    names:      list    # Names list
    gacha:      str     # Gacha banner (if part of one)
    drop:       bool    # Is unit a drop item (from stage)
    desc:       list    # JP description + names
    tals:       list    # Talents list

    def __init__(self, ID: int):
        super().__init__(ID)
        if self.ID == -1:
            return

        self.tf = self.trueForm
        self.r = self.getRarity()
        self.names = self.getNames(ID)
        self.ls = self.getData()
        self.gacha = self.getGacha()
        self.drop = self.isDrop()
        self.desc = self.getDesc()
        self.tals = self.getTalents()


    def getStart(self) -> str:
        """
        Gets the start of the page: intro templates, intro,
        cat appearance, performance, pros/cons, job, strategy/usage
        """
        # this just prevents the parameters being too long
        bold = lambda x: f"'''{x}'''"
        def get_perf():
            """Gets performance section"""

            abils = [get_abilities(self.ls[k], 2) for k in
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
                if self.tf and has(2):
                    if not (has(0) or has(1)):
                        perf[p] += f' {bold("[True]")}'
                    elif not has(0) and has(1):
                        perf[p] += f' {bold("[Evolved/True]")}'
                elif has(1) and not has(0):
                    perf[p] += f' {bold("[Evolved]")}'
                else:
                    continue
            move('[True]')
            move('Immune to')
            move(f'{bold("-")} ')
            perf = '<br>\n'.join(perf) + ('\n\n' if perf else '')
            # WTF this is such a disaster :skull:
            # oh well at least this works for some units
            return re.sub('\.0(?![0-9])', '', perf)

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

        image = lambda num: f"|image{num} = " + ('placeholder.png'
            if self.r[7] == current_ver else f'{self.ID:03} {num}.png') + "\n"

        limited = "{{LimitedContent}}\n{{Stub}}\n" if self.r[7] == current_ver else ''

        start = f"{bold(self.names[1])} is a{'n' if self.r[0] == 'Uber Rare' else ''}" \
                f" [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]] that can be {cond}" + \
                (f'. It was added in [[Version {self.r[7]} Update|'
                f'Version {self.r[7]}]]' if self.r[7] != '5.1' else '') + ".\n\n"

        catapp = f"{'{{'}Cat Appearance\n" \
                 f"|Cat Unit Number = {self.ID}\n" \
                 f"|cat category = [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]]\n" \
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
                    f"===Pros===\n*?\n\n===Cons===\n*?\n" + \
               "{{Job|Classification = [TODO]}}\n\n==Strategy/Usage==\n-\n\n"

        return limited + start + catapp + evol


    def getTranslation(self) -> str:
        """
        Method that writes the translation template
        """
        image = lambda id: 'placeholder.png'\
            if self.r[7] == current_ver else f'Uni{self.ID:03} {id}00.png'
        # TODO add english description
        return "==Description==\n{{Translation\n" + \
                f"|Cat Unit Number = {self.ID}\n" \
                f"|cat category = [[:Category:{self.r[0]} Cats|{self.r[0]} Cat]]\n" \
                f"|Normal Form name = {self.names[1]}\n" \
                f"|image1 = {image('f')}\n" \
                f"|cat_endesc1 = -\n" \
                f"|Evolved Form name = {self.names[2]}\n" \
                f"|image2 = {image('c')}\n" \
                f"|cat_endesc2 = -\n" + \
                (f'|Third Form name = {self.names[3]}\n'
                 f'|'f'image3 = {image("s")}\n'
                 f'|cat_endesc3 = -\n' if self.tf else '') + \
                f"|Normal Form name (JP) = {self.desc[0]} (?, ?)\n" \
                f"|cat_jpscriptc1 = {self.desc[3]}\n" \
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
        rarity = self.catRarity
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
        if rarity[3] in defaults:
            if rarity[3] == "9800":
                if not self.isLegend:
                    upgrade = "UR" if rarity[13] == '4' else "LR"
                else: upgrade = "EXL"
            else:
                upgrade = defaults[rarity[3]]
        else:
            upgrade = "MIX\n" + \
                      '\n'.join([f"|{i + 1:02} = {rarity[i + 3]}"
                                 for i in range(9)]) + f'\n|10 = ' \
                      f'{int(rarity[2])*2 if self.isCrazed else int(int(rarity[3])*1.5)}\n'
        # this gives a mix of XP as given in the rarity list
        return "==Cost==\n" + costs + f"{'{{'}Upgrade Cost|{upgrade}{'}}'}\n\n"


    def getTables(self, a: list) -> str:
        """Gets the standard/detailed stat tables of the cat"""
        tables = []

        def comparison(lis: list, key: int, an: bool = False) -> list:
            """A super compact version of the old compare function"""
            # TODO make comparison function cover health, attack, and DPS
            stats = {
                1: ("Knockback",),
                2: ("Movement Speed",),
                4: ("Attack Frequency",),
                5: ("Attack Range",),
                6: ("Ch1", "Ch2", "Ch3"),
                7: ("Recharge Time",),
                12: ("Target",)
            }
            if key not in stats: return [''] * 2
            if an: stats[1] = "Attack Animation",
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
                    stat = [ls[3],
                            f"{a_ls[form] - ls[13] - a_ls[form + 3]}f + "
                            f"{ls[13]}f + {a_ls[form + 3]}f",
                            a_ls[form + 3]]
                    # for only 1 hit

            except (IndexError, TypeError):
                stat = [ls[3],
                        f"{a_ls[form] - ls[13] - a_ls[form + 3]}f + "
                        f"{ls[13]}f + {a_ls[form + 3]}f",
                        a_ls[form + 3]]
                # for only 1 hit, try except because some files
                # have long lists while others do not
            return stat

        repeated = [comparison(self.ls, i) for i in range(13)]
        atks = [mult(self.ls[i], a, i) for i in range(3)]
        anim = comparison(atks, 1, an=True)
        # for attack animation
        mods = self.r[9:12]

        # TODO: figure out the weird stats - Crazed Fish, Crazed Bird,
        #  Flower Cat, Gacha Cat, Dom Cat
        left = '<'
        pipe = '|'
        # this is pretty much impossible to read at this point but w/e
        table_ls = []
        for i in range(3 if self.tf else 2):
            if i == 0:
                ind = 'normal'
            elif i == 1:
                ind = 'evolved'
            else:
                ind = 'third'

            DPS = round((atks[i][0] if i == 0 else
                         atks[i][0] * mods[2]) / (a[i] / 30), 2)
            atk = f"{atks[i][0] if i == 0 else int(atks[i][0] * mods[2] + 0.5):,}"
            hp = f"{self.ls[i][0] if i == 0 else int(self.ls[i][0] * mods[2] + 0.5):,}"

            table_ls.append(f'|{ind.capitalize()} Form name = {self.names[i + 1]}\n'
                f'|Hp {ind} = {hp} HP\n'
                f'|Atk Power {ind} = {atk} damage<br>({DPS} DPS)\n'
                f'|Atk Range {ind} = {self.ls[i][5]:,}\n'
                f'|Attack Frequency {ind} = '
                            f'{a[i]}f <sub>{round(a[i] / 30, 2)} seconds</sub>\n'
                f'|Movement Speed {ind} = {self.ls[i][2]}\n'
                f'|Knockback {ind} = {self.ls[i][1]} time{"s" if self.ls[i][1] > 1 else ""}\n'
                f'|Attack Animation {ind} = '
                            f'{self.ls[i][13]}f <sup>{round(self.ls[i][13] / 30, 2)}s</sup>'
                f'<br>({atks[i][2]}f <sup>'
                            f'{round(atks[i][2] / 30, 2)}s</sup> backswing)\n'
                f'|Recharging Time {ind} = {self.ls[i][7]}\n' +
                (f"|Hp normal Lv.MAX = {int(self.ls[i][0] * mods[2] + 0.5):,} HP\n"
                 f"|Atk Power normal Lv.MAX = "
                 f"{int(atks[i][0] * mods[2] + 0.5):,} damage<br>"
                 f"({round((int(atks[i][0] * mods[2] + 0.5)) / (a[i] / 30), 2):,}"
                 f" DPS){br}" if i == 0 else "") +
                f'|Attack type {ind} = {self.ls[i][12]}\n'
                f'|Special Ability {ind} = {get_abilities(self.ls[i], 0)}')
        tables.append(f"==Stats==\n<tabber>\nStandard=\n{'{{'}Cat Stats\n" +
                      '\n'.join(table_ls) + f'\n|Lv.MAX = Lv.{self.r[1]}' \
                      f'{f"+{self.r[2]}" if self.r[2] != 0 else ""}\n{"}}"}')

        tables.append(f'{pipe}-|Detailed=\n{"{{"}Calcstatstable{self.r[4]}\n'
            f'|Max Natural Level = {self.r[1]}{self.r[5]}\n'
            f'|Basic Form Name = {self.names[1]}\n'
            f'|HP Initial Normal = '
                      f'{self.ls[0][0]:,}\n|AP Initial Normal = {atks[0][0]:,}\n'
            f'|DPS Initial Normal = {math.floor(atks[0][0] / a[0] * 30)}\n'
            f'|DPS Initial Precise Normal = '
                      f'{"{{"}#expr:{(atks[0][0])}/({a[0]}/30){"}}"}\n'
            f'|HP Normal lvl 10 = {self.ls[0][0] * mods[0]:,}\n'
            f'|AP Normal lvl 10 = {int(atks[0][0] * mods[0] + 0.5):,}\n'
            f'|DPS Normal lvl 10 = '
                      f'{math.floor((atks[0][0] * mods[0]) / a[0] * 30):,}\n'
            f'|HP Normal lvl.MAX = {int(self.ls[0][0] * self.r[3]):,}\n'
            f'|AP Normal lvl.MAX = {int(atks[0][0] * self.r[3]):,}\n'
            f'|DPS Normal lvl.MAX = '
                      f'{math.floor(int(atks[0][0] * self.r[3]) / a[0] * 30):,}\n'
            f'|Attack Frequency Normal = {a[0]}\n'
            f'|Attack Animation Normal = {atks[0][1]}\n'
            f'|Attack Range Normal = {self.ls[0][5]:,}\n'
            f'|Target Normal = {self.ls[0][12]}\n'
            f'|Recharge Time Normal = {self.ls[0][7]}\n'
            f'|Knockback Normal = {self.ls[0][1]}\n'
            f'|Movement Speed Normal = {self.ls[0][2]}\n'
            f'|Ch1 Normal = {self.ls[0][6]:,}\n'
            f'|Ch2 Normal = {int(self.ls[0][6] * 1.5):,}\n'
            f'|Ch3 Normal = {self.ls[0][6] * 2:,}\n'
            f'|Special Ability Normal = {get_abilities(self.ls[0], 1)}\n'
            f'|Evolved Form Name = {self.names[2]}\n'
            f'|HP Initial Evolved = {self.ls[1][0]:,}\n'
            f'|AP Initial Evolved = {atks[1][0]:,}\n'
            f'|DPS Initial Evolved = {math.floor(atks[1][0] / a[1] * 30)}\n'
            f'|DPS Initial Precise Evolved ='
                      f' {"{{"}#expr:{atks[1][0]}/({a[1]}/30){"}}"}\n'
            f'|HP Evolved lvl 20 = {self.ls[1][0] * mods[1]:,}\n'
            f'|AP Evolved lvl 20 = {int(atks[1][0] * mods[1] + 0.5):,}\n'
            f'|DPS Evolved lvl 20 = '
                      f'{math.floor((atks[1][0] * mods[1]) / a[1] * 30):,}\n'
            f'|HP Evolved lvl.MAX = {int(self.ls[1][0] * self.r[3]):,}\n'
            f'|AP Evolved lvl.MAX = {int(atks[1][0] * self.r[3]):,}\n'
            f'|DPS Evolved lvl.MAX = '
                      f'{math.floor(int((atks[1][0] * self.r[3])) / a[1] * 30):,}'
            f'{repeated[4][0]}{anim[0]}{repeated[5][0]}'
            f'{repeated[12][0]}{repeated[7][0]}'
            f'{repeated[1][0]}{repeated[2][0]}{repeated[6][0]}\n'
            f'|Special Ability Evolved = {get_abilities(self.ls[1], 1)}\n' + \
            (f'{"}}"}\n{left}/tabber>' if not self.tf else
            f'|True Form Name = {self.names[3]}\n'
            f'|HP Initial True = {self.ls[2][0]:,}\n'
            f'|AP Initial True = {atks[2][0]:,}\n'
            f'|DPS Initial True = {math.floor(atks[2][0] / a[2] * 30)}\n'
            f'|DPS Initial Precise True = '
            f'{"{{"}#expr:{atks[2][0]}/({a[2]}/30){"}}"}\n'
            f'|HP True lvl 30 = {self.ls[2][0] * mods[2]:,}\n'
            f'|AP True lvl 30 = {int(atks[2][0] * mods[2] + 0.5):,}\n'
            f'|DPS True lvl 30 = '
            f'{math.floor((atks[2][0] * mods[2]) / a[2] * 30):,}\n'
            f'|HP True lvl.MAX = {int(self.ls[2][0] * self.r[3]):,}\n'
            f'|AP True lvl.MAX = {int(atks[2][0] * self.r[3]):,}\n'
            f'|DPS True lvl.MAX = '
            f'{math.floor(int((atks[2][0] * self.r[3])) / a[2] * 30):,}'
            f'{repeated[4][1]}{anim[1]}{repeated[5][1]}'
            f'{repeated[12][1]}{repeated[7][1]}{repeated[1][1]}'
            f'{repeated[2][1]}{repeated[6][1]}\n'
            f'|Special Ability True = {get_abilities(self.ls[2], 1)}\n{"}}"}\n{left}/tabber>'))

        return re.sub('\.0(?![0-9])', '', '\n\n'.join(tables))


    def getCatfruit(self) -> str:
        """
        Method that writes the catfruit section
        """
        cfList = self.r[8]
        if not cfList: return ''
        else:
            catfruits = {
            30: "PurpleSeed",
            31: "RedSeed",
            32: "BlueSeed",
            33: "GreenSeed",
            34: "YellowSeed",
            35: "PurpleFruit",
            36: "RedFruit",
            37: "BlueFruit",
            38: "GreenFruit",
            39: "YellowFruit",
            40: "RainbowFruit",
            41: "AncientSeed",
            42: "AncientFruit",
            43: "RainbowSeed",
            44: "GoldenFruit",
            160: "AkuSeed",
            161: "AkuFruit",
            164: "GoldenSeed",
            167: "PurpleCube",
            168: "RedCube",
            169: "BlueCube",
            170: "GreenCube",
            171: "YellowCube"}
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
    def getTalent(talents: list) -> str:
        """Writes the talents section"""
        if not talents: return ''
        else: return re.sub('\.0(?![0-9])', '',
                            f"\n\n==Talents==\n*{f'{br}*'.join(talents)}")


    def getEnd(self) -> str:
        """
        Method that writes the appearance, gallery, reference,
        and previous/next page links
        """
        ver = self.r[7]
        names = opencsv(DIR + "/names.csv", header=True)
        appearance = f"\n\n==Appearance==\n*Normal Form: ?\n*Evolved Form: " \
                     f"?{f'{br}*True Form: ?' if self.tf else ''}\n\n" \
                     f"{'<!--' if ver == current_ver else ''}" +\
                     "{{Gallery|Gatyachara " + f"{self.ID:03}" + " f}}" + \
                     f"{'-->' if ver == current_ver else ''}\n\n"
        reference = f'==Reference==\n' \
                    f'*https://battlecats-db.com/unit/{self.ID + 1:03}.html\n\n'
        end = f'----\n<p style="text-align:center;">' \
              f'[[Cat Release Order|Units Release Order]]:</p>\n\n' +\
              f'<p style="text-align:center;">\'\'' \
              f'\'[[{names[self.ID - 1][4]}|' \
              f'&lt;&lt; {names[self.ID - 1][1]}]] ' + \
              f'| [[{names[self.ID + 1][4]}|' \
              f'{names[self.ID + 1][1]} &gt;&gt;]]' \
              f'\'\'\'</p>\n----\n\n{"{{Cats}}"}\n'

        return appearance + reference + end


    def getCategories(self) -> str:
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
            except IndexError:
                continue
        lis = [[i for i in range(len(l[j])) if not
                (l[j][i] == 0 or l[j][i] == -1)] for j in range(3)]
        # lis is a list of lists of indices where data is not 0
        # if there is only a single line,
        # there is no need for another list comprehension

        data = list(set([item for sublist in lis for item in sublist]))
        data.sort()
        addcat = lambda ca: categories.append([ca])
        categories = [["Cat Units", f"{self.r[0]} Cats"]]

        if 'Ancient Egg' in self.names[1]: addcat("Ancient Eggs")
        elif self.isCrazed: addcat("Crazed Cats")
        elif self.isLegend: addcat("Legend Cats")
        if self.gacha or self.r[0] == "Uber Rare" and not (self.ID == 53 or self.ID == 155):
            addcat("Gacha Cats")
        elif self.drop: addcat("Item Drop Cats")

        anti_traits = {
            10: "Anti-Red Cats",
            16: "Anti-Floating Cats",
            17: "Anti-Black Cats",
            18: "Anti-Metal Cats",
            19: "Anti-Traitless Cats",
            20: "Anti-Angel Cats",
            21: "Anti-Alien Cats",
            22: "Anti-Zombie Cats",
            78: "Anti-Relic Cats",
            96: "Anti-Aku Cats"
        }
        categories.append([anti_traits[i] for i in anti_traits if i in data])
        attack_types = {
             8: "Single Target Cats",
            12: "Area Attack Cats",
            44: "Long Distance Cats",
            59: "Multi-Hit Cats",
            99: "Cats with different effective ranges"
        }
        if 44 in data and 45 not in data: attack_types[44] = "Omni Strike Cats"
        categories.append([attack_types[i] for i in attack_types if i in data])
        abilities = {
            23: "Cats with Strong ability",
            24: "Cats with Knockback ability",
            25: "Cats with Freeze ability",
            27: "Cats with Slow ability",
            29: "Cats with Resistant ability",
            30: "Cats with Massive Damage ability",
            31: "Critical Hit Cats",
            32: "Focused Target Cats",
            33: "Cats with Extra Money ability",
            34: "Base Destroyer Cats",
            35: "Mini-Wave Cats",
            37: "Cats with Weaken ability",
            40: "Cats with Strengthen ability",
            42: "Lethal Strike Resistant Cats",
            43: "Cats with Metal ability",
            47: "Wave Shield Cats",
            52: "Zombie Killer Cats",
            53: "Witch Killer Cats",
            70: "Barrier Breaker Cats",
            77: "Eva Angel Killer Cats",
            80: "Cats with Insanely Tough ability",
            81: "Cats with Insane Damage ability",
            82: "Savage Blow Cats",
            84: "Cats with Dodge Attack ability",
            86: "Surge Attack Cats",
            92: "Cats with Curse ability",
            95: "Shield Piercing Cats",
            97: "Colossus Slayer Cats",
            98: "Soulstrike Cats",
            105:"Behemoth Slayer Cats"
        }
        if 35 in data and 36 not in data: abilities[35] = "Wave Attack Cats"
        categories.append([abilities[i] for i in abilities if i in data])
        immunities = {
            46: "Cats with Wave Immunity",
            48: "Cats with Knockback Immunity",
            49: "Cats with Freeze Immunity",
            50: "Cats with Slow Immunity",
            51: "Cats with Weaken Immunity",
            75: "Warp Blocker Cats",
            79: "Cats with Curse Immunity",
            90: "Cats with Toxic Immunity",
            91: "Cats with Surge Immunity"
        }
        categories.append([immunities[i] for i in immunities if i in data])

        if self.getCatfruit() != '':
            for i in range(5):
                if i + 167 in self.r[8]:
                    addcat("Cats require Behemoth Stones for True Form")
                    break
                if i == 4: addcat("Cats require Catfruits for True Form")

        talents = {
            1: "Cats with Weaken ability",
            2: "Cats with Freeze ability",
            3: "Cats with Slow ability",
            6: "Cats with Resistant ability",
            7: "Cats with Massive Damage ability",
            8: "Cats with Knockback ability",
            10: "Cats with Strengthen ability",
            11: "Lethal Strike Resistant Cats",
            13: "Critical Hit Cats",
            14: "Zombie Killer Cats",
            15: "Barrier Breaker Cats",
            16: "Cats with Extra Money ability",
            17: "Wave Attack Cats",
            18: "Resist Weaken Cats",
            19: "Resist Freeze Cats",
            20: "Resist Slow Cats",
            21: "Resist Knockback Cats",
            22: "Resist Wave Cats",
            25: "Cats with Cost Down Talent",
            26: "Cats with Recover Speed Up Talent",
            27: "Cats with Move Speed Up Talent",
            29: "Cats with Curse Immunity",
            30: "Resist Curse Cats",
            31: "Cats with Attack Buff Talent",
            32: "Cats with Defense Buff Talent",
            35: "Anti-Black Cats",
            37: "Anti-Angel Cats",
            38: "Anti-Alien Cats",
            39: "Anti-Zombie Cats",
            40: "Anti-Relic Cats",
            44: "Cats with Weaken Immunity",
            45: "Cats with Freeze Immunity",
            46: "Cats with Slow Immunity",
            47: "Cats with Knockback Immunity",
            48: "Cats with Wave Immunity",
            49: "Warp Blocker Cats",
            50: "Savage Blow Cats",
            51: "Cats with Dodge Attack ability",
            52: "Resist Toxic Cats",
            53: "Cats with Toxic Immunity",
            54: "Resist Surge Cats",
            55: "Cats with Surge Immunity",
            56: "Surge Attack Cats",
            57: "Anti-Aku Cats",
            58: "Shield Piercing Cats",
            59: "Soulstrike Cats"
        }
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
            categories.append([talents[self.tals[i][0][0]] for i in
                               range(5 if self.tals[5][0][0] == 0 else 6) if not
                           categories_has(talents[self.tals[i][0][0]])])
        # adds talent categories at the end of the list
        # if there are talents
        if self.r[7] == current_ver: addcat("Translation requests")
        cates = [f"[[Category:{category}]]" for types in
                 categories for category in types]
        return '\n'.join(cates)