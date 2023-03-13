"""Program that takes all modules and converts into a page"""
from CatPage import *
from EnemyPage import *
from StatsCommon import StatsCommon
from common import *

class NoDataError(Exception):
    """Error from no/insufficient information"""
    def __init__(self, data: str, name: str):
        if data in ["catfruits", "talents", "description"]:
            error = f"'{name}' has no {data}."
        elif data == "ID":
            error = "Enter a valid name or ID!"
        elif data == "Increment":
            error = "Incompatible with increment!"
        else:
            error = f"{name} has no page."
        super().__init__(error)


class MakeCatPage:
    """Relays page content to Unit Page Maker"""
    def __init__(self, ID: int = -1, mode: int = 0):
        self.stats = StatsCommon()
        self.mode = mode
        self.cat_page = CatPage(ID)
        self.ID = self.cat_page.ID
        # turns ID to -1 if unit not found
        self.get_errors()
        self.op = vars(Options())
        self.anims = []
        self.cats = self.cat_page.getData()


    def get_errors(self):
        """Throws NoDataError"""
        if self.ID == -1:
            raise NoDataError("ID", "")
        # unit not found error
        name = self.cat_page.names[1]
        if len(self.cat_page.ls) < 3:
            raise NoDataError("", name)
        # insufficient data error
        elif self.mode == 3 and not self.cat_page.getCatfruit():
            raise NoDataError("catfruits", name)
        # no catfruit error
        elif self.mode == 4 and not self.cat_page.tals:
            raise NoDataError("talents", name)
        # no talents error


    def get_mode(self):
        """Turns the appropriate option to True depending on mode"""
        self.op[list(self.op)[self.mode]] = True


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
        anim = lambda k, num, ind: \
            self.stats.get_atkanim(self.ID, k, self.cats[num])[ind]
        self.anims = [anim('f', 0, 0), anim('c', 1, 0), anim('s', 2, 0),
                      anim('f', 0, 1), anim('c', 1, 1), anim('s', 2, 1)]

        # 0-2 attack frequency, 3-5 backswing



    def parse_cat(self):
        """Makes cat data and animation data ready for CatPage"""
        for i in range(3):
            self.cats[i][4] = self.anims[i]
            self.cats[i][7] = f"{self.cats[i][7]} ~ " \
                         f"{round(self.cats[i][7] - 8.8, 2) if self.cats[i][7] > 10.8 else 2}" \
                         f" seconds"
            self.cats[i][12] = "Single Target" if self.cats[i][12] == 0 else "Area Attack"

            if self.anims[i] - (self.cats[i][13] + self.anims[i + 3]) < 0:
                self.anims[i] = self.cats[i][13] + self.anims[i + 3]


    def get_page(self) -> str:
        self.get_errors()
        self.get_mode()
        self.process()
        self.get_anim()
        self.parse_cat()

        # returns depending on option
        if self.op['table']:
            return self.cat_page.getTables(self.anims)

        elif self.op['cost']:
            return self.cat_page.getCost().strip("\n")

        elif self.op['catfruit']:
            return self.cat_page.getCatfruit().strip('\n')

        elif self.op['talents']:
            return self.cat_page.getTalent(self.stats.get_talents(
                self.cat_page.tals, self.cats[2])).strip('\n')
            # FIXME - Literally not going to understand this a few days from now
            # This is what happens when you write 3 functions that
            # sound exactly the same from left to right:
            # if Cat.getTalents: return
            # Page.getTalent(stats.get_talents(Cat.getTalents, Cat.getData)) etc.

        elif self.op['category']:
            return self.cat_page.getCategories()

        else:
            return self.cat_page.getStart() + self.cat_page.getTranslation() + \
                   self.cat_page.getCost() + \
                   self.cat_page.getTables(self.anims) + \
                   self.cat_page.getCatfruit() + \
                   self.cat_page.getTalent(self.stats.get_talents(
                       self.cat_page.tals, self.cats[2])) + \
                   self.cat_page.getEnd() + \
                   self.cat_page.getCategories()


class MakeEnemyPage:
    """Relays page content to Unit Page Maker"""
    def __init__(self, ID: int = -1, mode: int = 6):

        self.stats = StatsCommon(is_enemy=True)
        self.mode = [0, 1, 6, 7, 5][mode - 6]
        self.en_page = EnemyPage(ID)
        self.ID = self.en_page.ID
        # turns ID to -1 if unit not found
        self.op = vars(Options())
        self.get_errors()


    def get_mode(self):
        """Turns the appropriate option to True depending on mode"""
        self.op[list(self.op)[self.mode]] = True


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