"""Program that receives input and writes the contents of a page"""
from common import *
from StatsCommon import StatsCommon

class Enemy:
    """Enemy data from data mines"""
    def __init__(self, ID: int):
        self.ID = ID

        self.enemyNames = opencsv(DIR + "/enemyNames.csv", header=True)
        try:
            self.name = self.getName(ID)
            self.enemyData = opencsv(
                f"{data_mines}/DataLocal/t_unit.csv")[ID + 2]

            with open(f"{data_mines}/resLocal/Enemyname.tsv",
                      "r", encoding="utf-8") as f:
                self.jpName = f.read().split("\n")[ID]
                if self.jpName == "ダミー":
                    self.jpName = None
            # bruh why can't ponos just make this a csv file ffs

            self.enemyDesc = opencsv(f"{data_mines}/resLocal/"
                                f"EnemyPictureBook_ja.csv")[ID][1:-1]
        except (IndexError, FileNotFoundError):
            self.ID = -1


    def getName(self, ID):
        return self.enemyNames[ID][1]


    def getData(self):
        return [int(i) for i in self.enemyData]


    def getDesc(self):
        return "<br>".join(self.enemyDesc)


class EnemyPage(Enemy):
    """
    Inherits from Enemy class.
    """
    def __init__(self, ID: int):
        super().__init__(ID)
        if self.ID == -1:
            return
        self.stats = StatsCommon(is_enemy=True)
        self.ls = self.getData()
        if self.stats.get_atkanim(ID, "", self.ls)[1] < 1 or self.name == "N/A":
            self.ID = -2
            return
        self.desc = self.getDesc()


    def getStart(self):
        """Gets the start of the page"""
        t = " ({}, ''?'', '''?''')".format(
            self.jpName) if self.jpName is not None else ""
        try:
            traits = self.stats.get_traits(self.ls)
            vowel = ('an ' if traits[0] in ['A', 'E'] else 'a ') + \
                    self.stats.get_traits(self.ls, True) + ' enemy'
            if traits == "Typeless":
                raise IndexError
        except IndexError:
            vowel = 'an [[Enemy Bases|enemy base]]'
        start = f"'''{self.name}'''{t} is {vowel} that" \
                f" appears in [TODO].\n\n"
        money = f"{self.ls[6]:,}¢ - " \
                f"{int(self.ls[6] * 3.95):,}¢" if self.ls[6] else "N/A"
        enemy_info = f"|name = {self.name}\n" \
                     f"|image = E {self.ID + 2:03}.png\n" \
                     f"|first appearance = ?\n" \
                     f"|money drop = {money}\n"

        info = "==Enemy==\n?\n\n==Strategy==\n?\n\n"

        return start + "{{Enemy Info\n" + enemy_info + "}}\n\n" + info


    def getDict(self):
        """Gets the enemy dictionary description, if exists"""
        return "==Dictionary==\n" \
               "{{EnemyDescription\n" \
               f"|Enemy Unit Number = {self.ID:03}\n" \
               f"|enemy category = {self.stats.get_traits(self.ls, True)}\n" \
               f"|Enemy name = {self.name}\n" \
               f"|enemy_endesc1 = -\n" \
               f"|image1 = Enemy icon {self.ID:03}.png\n" \
               f"|enemy_jpscriptc1 = {self.desc}\n" \
               f"|enemy_jpdesc1 = ?\n" \
               f"|Enemy name (JP) = {self.jpName} (?, ?)\n" \
               "}}\n\n" if self.jpName is not None else ""


    def getEncounters(self):
        """Gets the enemy encounters !!!INCOMPLETE!!!"""
        def stg():
            cache = []

            for datafile in os.listdir(f"{data_mines}/DataLocal"):
                if datafile[:5] == "stage":
                    x = opencsv(f"{data_mines}/DataLocal/{datafile}")
                    for i, ls in enumerate(x):
                        if len(ls) > 9 and ls[0] == self.ID and i > 0 and datafile not in cache:
                            cache.append(datafile)
                            yield datafile
        print(list(stg()))
        return "\n".join(list(stg()))


    def getStats(self) -> str:
        """Gets the stat table of the enemy"""
        atk = self.ls[3] + self.ls[55] + self.ls[56]
        bkswing, atkfreq = self.stats.get_atkanim(self.ID, "", self.ls)
        traits = self.stats.get_traits(self.ls)
        targ = 'Area Attack' if self.ls[11] == 1 else 'Single Target'
        # general stats

        bkswing = bkswing + \
                  (self.ls[12] - self.ls[58 if self.ls[56] else 57]
                   if self.ls[55] else 0)
        # obtaining actual backswing from multi-hit

        aste = "*" if self.ls[18] else ""
        msg = f"<br>\n''*Stats shown are with all" \
              f" [[Anti-{'S' if self.ls[69] else 'uns'}tarred" \
              f" Alien Treasures]].''" if self.ls[18] else ""
        # for treasures regarding aliens

        stats = "==Stats==\n" \
                "{{EnemyCharacter Stats\n" \
                f"|Enemy = {self.name}\n" \
                f"|Health = {self.ls[0]:,}{aste} HP\n" \
                f"|Attack Power = {atk:,}{aste} damage<br>" \
                f"({round(atk / (atkfreq / 30), 2):,}{aste} DPS)\n" \
                f"|Attack Range = {self.ls[5]:,}<br>" \
                f"([[Special Abilities#{targ}|{targ}]])\n" \
                f"|Time between attacks = {atkfreq:,}f <sub>" \
                f"{round(atkfreq / 30, 2)} seconds</sub>\n" \
                f"|Movement Speed = {self.ls[2]}\n" \
                f"|Knockback = {self.ls[1]:,} time" \
                f"{'s' if self.ls[1] != 1 else ''}\n" \
                f"|Occurrence = {self.ls[12]:,}f <sup>" \
                f"{round(self.ls[12] / 30, 2)}s</sup><br>({bkswing:,}f <sup>" \
                f"{round(bkswing / 30, 2)}s</sup> backswing)\n" \
                f"|Ability = {self.stats.get_abilities(self.ls, -1)}{msg}\n" \
                f"|Element = {traits if traits else 'Typeless'}\n" \
                "}}\n\n"
        return re.sub('\.0(?![0-9])', '', stats)


    def getEnd(self):
        """Gets the end of the enemy page"""
        def get_nbr(p: int):
            """PONOS cringe"""
            try:
                en = self.enemyNames[self.ID + p]
                if self.ID + p < 0:
                    raise IndexError
            except IndexError:
                return "N/A"
            if en[1] == "N/A":
                for i in range(1, len(self.enemyNames)):
                    if self.enemyNames[self.ID + p * i][1] != "N/A":
                        en = self.enemyNames[self.ID + p * i]
                        break
            en[2] = en[1] if not en[2] else en[2]
            return en

        prev_en = f"[[{get_nbr(-1)[2]}|&lt;&lt; {get_nbr(-1)[1]}" \
                  f"]]" if get_nbr(-1) != "N/A" else "&lt;&lt; N/A"

        next_en = f"[[{get_nbr(1)[2]}|{get_nbr(1)[1]} &gt;&gt;" \
                  f"]]" if get_nbr(1) != "N/A" else "N/A &gt;&gt;"

        gallery = "==Gallery==\n" \
                  '<gallery hideaddbutton="true" bordercolor="transparent">\n' \
                  f"{self.ID} e.png|{self.name}'s spritesheet\n" \
                  "</gallery>\n\n"

        reference = "==Reference==\n" \
                    f"*https://battlecats-db.com/enemy/" \
                    f"{self.ID + 2:03}.html\n\n"

        end =  "----\n" \
               '<p style="text-align:center;">' \
               '[[Enemy Release Order]]:</p>\n\n' \
               f'<p style="text-align:center;">' \
               f"'''{prev_en} | {next_en}'''</p>" \
               "\n----\n\n{{Enemies}}\n"

        return gallery + reference + end


    def getCategories(self):
        """Gets the enemy page categories"""
        if self.ls[27] != 0 and (len(self.ls) < 87 or self.ls[86] != 1):
            self.ls[28] = 0
        data = [index for index, x in enumerate(self.ls)
                if x not in [-1, 0] and index > 8]
        categories = [["Enemy Units"]]
        traits = {
            10: "Red Enemies",
            13: "Floating Enemies",
            14: "Black Enemies",
            15: "Metal Enemies",
            16: "Traitless Enemies",
            17: "Angel Enemies",
            18: "Alien Enemies",
            19: "Zombie Enemies",
            48: "Witch Enemies",
            49: "Typeless Enemies",
            63: "Unstarred Alien Enemies",
            69: "Starred Alien Enemies",
            71: "Eva Angel Enemies",
            72: "Relic Enemies",
            93: "Aku Enemies",
            94: "Colossal Enemies",
            101: "Behemoth Enemies"
        }
        if 18 in data and 69 not in data:
            data.append(63)
        categories.append([traits[i] for i in traits if i in data])
        attack_types = {
             8: "Single Target Enemies",
            11: "Area Attack Enemies",
            35: "Long Distance Enemies",
            55: "Multi-Hit Enemies",
            95: "Enemies with different effective ranges"
        }
        if 11 not in data:
            data.insert(0, 8)
        categories.append([attack_types[i] for i in attack_types if i in data])

        abilities = {
            20: "Enemies with Knockback ability",
            21: "Enemies with Freeze ability",
            23: "Enemies with Slow ability",
            25: "Critical Hit Enemies",
            26: "Base Destroyer Enemies",
            27: "Mini-Wave Enemies",
            29: "Enemies with Weaken ability",
            32: "Enemies with Strengthen ability",
            34: "Lethal Strike Resistant Enemies",
            43: "Enemies with Burrow ability",
            45: "Enemies with Revive ability",
            52: "Kamikaze Enemies",
            64: "Enemies with Barriers",
            65: "Enemies with Warp ability",
            73: "Enemies with Curse ability",
            75: "Savage Blow Enemies",
            77: "Enemies with Dodge Attack ability",
            79: "Enemies with Toxic ability",
            81: "Surge Attack Enemies",
            87: "Enemies with Shields",
            89: "Enemies with Aftermath ability"
        }
        if 27 in data and 28 not in data:
            abilities[27] = "Wave Attack Enemies"
        categories.append([abilities[i] for i in abilities if i in data])

        immunities = {
            37: "Enemies with Wave Immunity",
            39: "Enemies with Knockback Immunity",
            40: "Enemies with Freeze Immunity",
            41: "Enemies with Slow Immunity",
            42: "Enemies with Weaken Immunity",
            85: "Enemies with Surge Immunity"
        }
        # I'm geniunely surprised on how short this is
        categories.append([immunities[i] for i in immunities if i in data])

        cates = [f"[[Category:{category}]]" for types in
                 categories for category in types]
        return '\n'.join(cates)


