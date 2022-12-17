"""Program that receives input and writes the contents of a page"""
from common import *
from StatsCommon import StatsCommon
from Enemy import Enemy

class EnemyPage(Enemy):
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
        self.stats = StatsCommon(True)
        self.ls = self.getData()
        # self.desc = self.getDesc()


    def getTables(self) -> str:
        """Gets the standard/detailed stat tables of the cat"""
        atk = self.ls[3] + self.ls[55] + self.ls[56]
        atkfreq = self.stats.get_atkfreq(self.ID, "", self.ls)
        bkswing = self.stats.get_backswing(self.ID, "", self.ls)

        targ = 'Area Attack' if self.ls[11] == 1 else 'Single Target'

        stats = "==Stats==\n" \
                "{{EnemyCharacter Stats\n" \
                f"|Enemy = {self.name}\n" \
                f"|Health = {self.ls[0]:,} HP\n" \
                f"|Attack Power = {atk:,} damage<br>" \
                f"({round(atk / (atkfreq / 30), 2):,} DPS)\n" \
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
                f"|Ability = {self.stats.get_abilities(self.ls, -1)}\n" \
                f"|Element = {self.stats.get_traits(self.ls)}\n" \
                "}}"
        return re.sub('\.0(?![0-9])', '', stats)
