"""Program that takes all modules and converts into a page"""
from CatPage import *
from StatsCommon import StatsCommon
from common import *

class NoDataError(Exception):
    """Error from no/insufficient information"""
    def __init__(self, data: str, name: str):
        if data in ["Catfruits", "Talents"]:
            error = f"'{name}' has no {data}."
        elif data == "ID":
            error = "Enter a valid name or ID!"
        else:
            error = f"{name} have no page."
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
            raise NoDataError("Catfruits", name)
        # no catfruit error
        elif self.mode == 4 and not self.cat_page.tals:
            raise NoDataError("Talents", name)
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
        self.anims = [self.stats.get_atkfreq(self.ID, 'f', self.cats[0]),
                      self.stats.get_atkfreq(self.ID, 'c', self.cats[1]),
                      self.stats.get_atkfreq(self.ID, 's', self.cats[2])
                      if self.cat_page.tf else 100,
                      self.stats.get_backswing(self.ID, 'f', self.cats[0]),
                      self.stats.get_backswing(self.ID, 'c', self.cats[1]),
                      self.stats.get_backswing(self.ID, 's', self.cats[2])
                      if self.cat_page.tf else 0]
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
                # print(page.getNames()[i + 1])


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


# TODO: - Simplify the spaghetti