"""Module that contains enemy data information"""
from common import *

class Enemy:

    def __init__(self, ID: int):
        self.ID = ID

        self.enemyNames = opencsv(DIR + "/enemyNames.csv")
        try:
            self.name = self.getName(ID)
            self.enemyData = opencsv(
                f"{data_mines}/DataLocal/t_unit.csv")[ID + 2]

            with open(f"{data_mines}/resLocal/Enemyname.tsv",
                      "r", encoding="utf-8") as f:
                self.jpName = f.read().split("\n")[ID]
                if self.jpName == "ダミー": self.jpName = None
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


"""
Testing:

e = Enemy(600)
print(e.name)
print(e.jpName)
print(e.getDesc())
"""