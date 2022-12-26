"""Module that contains cat data information"""
from common import *

class Cat:
    """Cat class parses data from data mines"""
    trueForm = False    # does unit have true form
    isLegend = False    # is unit a legend unit e.g. Ururun Wolf
    isCrazed = False    # is unit a crazed cat
    isCollab = False    # is unit a collab unit

    def __init__(self, ID: int):
        self.ID = ID
        self.trueForm = True
        try:
            self.catNames = opencsv(DIR + "/catNames.csv", header=True)
            self.names = self.getNames(ID)
            self.catData = opencsv(f"{data_mines}/DataLocal/unit{ID + 1:03}.csv")[0:3]
            self.catRarity = opencsv(f"{data_mines}/DataLocal/unitbuy.csv")[ID]
            self.catRedPts = opencsv(f"{data_mines}/DataLocal/unitlevel.csv")[ID]
            self.catGacha = opencsv(f"{data_mines}/DataLocal/GatyaDataSetR1.csv")
            self.catDesc = opencsv(f"{data_mines}/resLocal/Unit_Explanation{ID + 1}_ja.csv")
            self.catTalents = opencsv(f"{data_mines}/DataLocal/SkillAcquisition.csv")
            self.NPCosts = opencsv(f"{data_mines}/DataLocal/SkillLevel.csv")
        except (FileNotFoundError, IndexError):
            self.ID = -1


    def getData(self):
        """Gets cat data (abilities and stats)"""
        return self.catData


    def getRarity(self):
        """gives tuple of rarity information, check comment for return"""
        reduction = self.catRedPts
        # data on reduction points
        rarFile = self.catRarity
        # unitbuy.csv data
        maxLevel = int(rarFile[50]) + int(rarFile[51])  # max level + max plus level
        rp = [len([i for i in reduction if i == '20']) * 10,
              len([j for j in reduction if j == '10']) * 10]
        # list of reduction points
        rp[1] += rp[0]
        if rp[1] > maxLevel: rp.pop(1)
        rarities = "Normal", "Special", "Rare", "Super Rare",\
                   "Uber Rare", "Legend Rare"
        r = int(rarFile[13])
        # r is the rarity index
        maxPlus = f"\n|Max Plus Level = " \
                  f"{int(rarFile[51])}" if int(rarFile[51]) != 0 else ""
        if int(rarFile[3]) > 50000 and r == 3:
            self.isCrazed = True

        def getMod(level: int) -> tuple:
            """:return: max modifier, growth modifier"""
            if len(rp) == 1:
                mod = math.floor(2.5 * round(((rp[0] + 4) / 5 + (level - rp[0]) / 10) * 5500)) / 5500 if level > rp[0] \
                    else math.floor(2.5 * round(((level + 4) / 5) * 5500) / 5500)
                if r != 0:
                    growMod = f"\n|Grow Level 1 = {rp[0]}" if level > rp[0] else ""
                else:
                    growMod = f"\n|Grow Level 2 = 111" if level > rp[0] else ""
                # for only 1 reduction point rarities, like normal, special, etc.
                # maths from level-up page
            else:
                if level <= rp[0]:
                    mod = math.floor(2.5 * round(((level + 4) / 5) * 5500)) / 5500
                    growMod = ""
                    # growMod is formatted for reduction points
                elif rp[0] < level <= rp[1]:
                    mod = math.floor(2.5 * round(((rp[0] + 4) / 5 + (level - rp[0]) / 10) * 5500)) / 5500
                    growMod = f"\n|Grow Level 1 = {rp[0]}" if r == 2 else ""
                else:
                    mod = math.floor(
                        2.5 * round((((rp[0] + 4) / 5 + (rp[1] - rp[0]) / 10) + (level - rp[1]) / 20) * 5500)) / 5500
                    growMod = f"\n|Grow Level 1 = {rp[0]}\n|Grow Level 2 = {rp[1]}" if r == 2 else ""
            mod = mod if not int(mod) == mod else int(mod)
            return mod, growMod

        def getVersion():
            """:return: version unit is introduced"""
            if len(rarFile[-6]) == 6:
                version = f'{rarFile[-6][0:2]}.{int(rarFile[-6][2:4])}'
            elif len(rarFile[-6]) == 5:
                version = f'{rarFile[-6][0:1]}.{int(rarFile[-6][1:3])}'
            else:
                version = '5.1'  # FIXME fix this bit (obviously)
            return version

        def getFruit():
            """:return: catfruit information"""
            if int(rarFile[27]) == 0:
                return False
            else:
                fruits = rarFile[27:38]
            return [int(i) for i in fruits]

        if rarFile[14][0:2] == '19' and rarFile[17] == '3':
            self.isLegend = True
        # Note: Work on this in case of outliers

        return rarities[r], int(rarFile[50]), int(rarFile[51]), getMod(maxLevel)[0],\
                      getMod(maxLevel)[1], maxPlus, -1, getVersion(), getFruit(),\
                      getMod(10)[0], getMod(20)[0], getMod(30)[0]
        # rarity, max natural level, max plus level, lvl max mod, grow levels,
        # formatted max plus, -1, version, catfruits, lvl 10 mod, lvl 20 mod, lvl 30 mod


    def getNames(self, ID: int = -1):
        """Gets the names of unit and also whether unit has true form or not"""
        if ID == -1: ID = self.ID
        n = self.catNames
        if n[ID][3] == '': self.trueForm = False
        self.names = n[ID]
        return self.names
        # [normal name, evolved name, true name, web name]


    def getGacha(self):
        """False if unit is not Gacha, otherwise returns gacha banner"""
        self.getRarity()
        pos = -1
        gachaFile = self.catGacha

        def link(event, collab = False):
            return f"[[{event} " \
                   f"{'(Gacha Event)' if not collab else 'Collaboration Event'}" \
            f"|{event}]] {'gacha' if not collab else 'collaboration'} event"

        # TODO: Expand on this, need selections, Neon Genesis Evangelion 2nd,
        #       Street Fighter V/Blue Team, Street Fighter V/Red Team,
        #       June Bride, N/BotB,
        #       SUPERFEST, Red Busters, Air Busters, Metal Busters, Wave Busters,
        #       Colossus Busters, Dynasty Fest, Royal Fest,
        #       Yurudrasil, Gudetama.
        gachas = {
            34: link("Tales of the Nekoluga"),
            42: link("The Dynamites"),
            66: link("Princess Punt Sweets", collab=True),
            71: link("Sengoku Wargods Vajiras"),
            75: link("Cyber Academy Galaxy Gals"),
            83: link("Lords of Destruction Dragon Emperors"),
            110: link("Merc Storia", collab=True),
            134: link("Ancient Heroes Ultra Souls"),
            174: link("Survive! Mola Mola!", collab=True),
            180: link("Shoumetsu Toshi", collab=True),
            194: link("Dark Heroes"),
            225: link("Metal Slug Defense", collab=True),
            229: link("Halloween Capsules"),
            241: link("Xmas Gals"),
            257: link("The Almighties"),
            288: link("Puella Magi Madoka Magica", collab=True),
            304: link("Frontline Assault Iron Legion"),
            326: link("Crash Fever", collab=True),
            330: link("Easter Carnival"),
            334: link("Girls & Monsters: Angels of Terror"),
            354: link("Gals of Summer"),
            359: link("Nature's Guardians Elemental Pixies"),
            362: link("Fate/Stay Night: Heaven's Feel", collab=True),
            393: link("Power Pro Baseball", collab=True),
            412: link("Neon Genesis Evangelion", collab=True),
            467: link("Bikkuriman", collab=True),
            511: link("Street Fighter V", collab=True),
            535: link("Hatsune Miku", collab=True),
            587: link("Valentine Gals"),
            596: link("Ranma 1/2", collab=True),
            648: link("White Day"),
        }
        fests = {
            269: link("UBERFEST"),
            333: link("EPICFEST")
        }

        for i in range(len(gachaFile)):
            ind = gachaFile[i].index('-1') if len(gachaFile[i]) != 0 else 0
            gachaFile[i] = gachaFile[i][0:ind]
            if str(self.ID) in gachaFile[i]:
                pos = i
                break
            if i == len(gachaFile) - 1: return False

        pool = fests if '34' in gachaFile[pos] and '42' in gachaFile[pos] else gachas
        # Note: Temporary, change later
        for key in pool:
            if str(key) in gachaFile[pos]:
                self.isCollab = "Collaboration" in pool[key]
                self.gacha = pool[key]
                return self.gacha


    def isDrop(self) -> bool:
        """Checks if unit is a drop item"""
        gachaFile = self.catGacha
        for i in gachaFile:
            if str(self.ID) in i: return False
        # first, check if unit is gacha. If it is, then it is not a drop.
        dropFile = opencsv(f"{data_mines}/DataLocal/drop_chara.csv", header=True)

        for j in dropFile:
            if not j: continue
            if str(self.ID) == j[-1] and j[0] != '-1': return True
        return False


    def getNPCost(self, LvID: int) -> tuple:
        c = self.NPCosts[LvID]
        if LvID != 0:
            costs = [int(i) for i in c if i if i != '\x03\x03\x03']
            return sum(costs[1:]), True if len(costs) > 2 else False
        else: return 0,


    def getTalents(self) -> list:
        """Checks if unit has talents"""
        tals = self.catTalents
        for i in tals:
            if i[0] == str(self.ID):
                i = [int(x) for x in i if x != '\x03\x03\x03']
                return [(i[13 * k + 2:13 * k + 14], self.getNPCost(i[13 * k + 13])) for k in range(6)]
        return []


    def getDesc(self):
        """Gets the jp description and names for cat"""
        descriptions = self.catDesc
        # this file contains both jp descriptions and names
        self.desc = [descriptions[x][0] for x in range(3)]
        for i in range(3):
            try:
                self.desc.append('<br>'.join(descriptions[i][1:4]))
            except IndexError:
                continue
        return self.desc
        # [name1, name2, name3, desc1, desc2, desc3]