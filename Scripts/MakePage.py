"""Program that takes all modules and converts into a page"""
from CatPage import *
from EnemyPage import *
from StatsCommon import StatsCommon
from common import *


class MakePage:
    """Placeholder Parent Class"""
    def __init__(self, mode: int = 0, isEnemy: bool = False):
        self.stats = StatsCommon(is_enemy=isEnemy)
        self.mode = mode if not isEnemy else [0, 1, 6, 7, 5][mode - 6]
        self.op = vars(Options())


    def get_mode(self):
        """Turns the appropriate option to True depending on mode"""
        self.op[list(self.op)[self.mode]] = True


class MakeCatPage(MakePage):
    """Relays page content to Unit Page Maker"""
    def __init__(self, ID: int = -1, mode: int = 0):
        super().__init__(mode)
        self.cat_page = CatPage(ID)
        self.ID = self.cat_page.ID
        # turns ID to -1 if unit not found
        self.name = self.cat_page.names[1]
        self.get_errors()
        self.anims = []
        self.cats = self.cat_page.ls


    def get_errors(self):
        """Throws NoDataError"""
        if self.ID == -1:
            raise NoDataError("ID", "")
        # unit not found error
        if len(self.cat_page.ls) < 3:
            raise NoDataError("", self.name)
        # insufficient data error
        elif self.mode == 3 and not self.cat_page.getCatfruit():
            raise NoDataError("catfruits", self.name)
        # no catfruit error
        elif self.mode == 4 and not self.cat_page.tals:
            raise NoDataError("talents", self.name)
        # no talents error


    def process(self):
        """Changes cat data to be easily parsable"""
        for k in range(len(self.cats)):
            try:
                for n in range(len(self.cats[0])):
                    try:
                        self.cats[k][n] = int(self.cats[k][n])
                        if n == 7:
                            self.cats[k][7] = round((self.cats[k][7] * 2) / 30, 2)
                    except IndexError:
                        continue
            except ValueError:
                continue


    def get_anim(self):
        """Gets all the animation data"""
        def anim(k: str, num: int, ind: int):
            "Formatting"
            if self.cat_page.isEgg and num < 2:
                return 44 if ind == 0 else 471
            else:
                return self.stats.get_atkanim(self.ID, k, self.cats[num])[ind]

        self.anims = [[anim('f', 0, 1), anim('c', 1, 1), anim('s', 2, 1),
                       anim('u', 3, 1) if self.cat_page.uf else -1],
                      [anim('f', 0, 0), anim('c', 1, 0), anim('s', 2, 0),
                       anim('u', 3, 0) if self.cat_page.uf else -1]
                      ]

        # attack frequency, backswing


    def get_page(self) -> str:
        self.get_errors()
        self.get_mode()
        self.process()
        self.get_anim()

        c = self.cat_page
        t = self.stats.get_talents(c.tals, self.cats[2])

        # returns depending on option
        if self.op['table']:
            return c.getTables(self.anims)

        elif self.op['cost']:
            return c.getCost().strip("\n")

        elif self.op['catfruit']:
            return c.getCatfruit().strip('\n')

        elif self.op['talents']:
            return c.getTalent(t).strip('\n')

        elif self.op['category']:
            return c.getCategories(t)

        else:
            return f"{c.getStart()}" \
                   f"{c.getTranslation()}" \
                   f"{c.getCost()}" \
                   f"{c.getTables(self.anims)}" \
                   f"{c.getCatfruit()}" \
                   f"{c.getTalent(t)}" \
                   f"{c.getEnd()}" \
                   f"{c.getCategories(t)}"


class MakeEnemyPage(MakePage):
    """Relays page content to Unit Page Maker"""
    def __init__(self, ID: int = -1, mode: int = 6):
        super().__init__(mode, True)
        self.en_page = EnemyPage(ID)
        self.ID = self.en_page.ID
        # turns ID to -1 if unit not found
        self.op = vars(Options())
        self.get_errors()


    def get_errors(self):
        if self.ID == -1:
            raise NoDataError("ID", "")
        # unit not found error
        if self.ID == -2:
            raise NoDataError("", f"This enemy")
        name = self.en_page.name
        if self.mode == 6 and self.en_page.jpName is None:
            raise NoDataError("description", name)
        # no description error


    def get_page(self) -> str:
        self.get_mode()
        if self.op['table']:
            return self.en_page.getStats().strip("\n")

        elif self.op['desc']:
            return self.en_page.getDict().strip("\n")

        elif self.op['encounters']:
            return self.en_page.getEncounters().strip('\n')

        elif self.op['category']:
            return self.en_page.getCategories().strip('\n')

        else:
            return self.en_page.getStart() + self.en_page.getDict() + \
                   self.en_page.getStats() + \
                   self.en_page.getEnd() + self.en_page.getCategories()

# NOTE: Maybe 2 classes for practically the same thing isn't the most efficient