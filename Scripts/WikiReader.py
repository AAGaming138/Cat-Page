"""Script that converts wiki csv into a form readable by UnitPageMaker"""
from common import *

class WikiReader:

    def __init__(self, page):
        self.url = "https://battle-cats.fandom.com/wiki/" + page
        self.processed = []
        self.html = self.openUrl()
        self.cor = {"000":   "RN",
                    "001":   "RS",
                    "002":   "RC",
                    "003":   "main",
                    "004":   "EX",
                    "006":   "RT",
                    "007":   "RV",
                    "011":   "R",
                    "012":   "DM",
                    "013":   "RNA",
                    "014":   "RB",
                    "024":   "RA",
                    "025":   "RH",
                    "027":   "RCA",
                    "031":   "RQ",
                    "033":   "L",
                    "034":   "RND",
                    }

    def openUrl(self):
        try:
            webpage = request.urlopen(self.url)
        except urllib.error.URLError:
            return "Unable to open URL! (No connection?)"
        # extract and decode html
        return webpage.read().decode("UTF-8").split("\n")


    def readNames(self):
        """Extract names from wiki html"""
        for line in self.html:
            if line:
                if line[0:3] == "Num" or line[0:3] == "Ima" or line[0].isnumeric():
                    # keep lines that have csv content in them
                    self.processed.append(line)

        for i in range(len(self.processed[-1])):
            try:
                if self.processed[-1][i:i+6] == "</div>":
                    self.processed[-1] = self.processed[-1][0:i]
            except IndexError:
                pass

        content = "\n".join(self.processed)

        if "Cat (Normal Cat)" in content:
            # write content into catNames.tsv
            with open(DIR + "/catNames.tsv", 'w', encoding='utf8') as f:
                f.write(content + "\nN/A\tN/A\t\t\tN/A\tN/A")

        else:
            if "2000\n021\t" in content:
                # fill in missing 019 and 020 between The Face and Ms Sign
                content = content.replace("The Face (Floating)\t99999\t2000\n",
                                          "The Face (Floating)\t99999\t2000\n"
                                          "019\tN/A\t\t\t\n020\tN/A\t\t\t\n")
            # write content into enemyNames.tsv
            with open(DIR + "/enemyNames.tsv", 'w', encoding='utf8') as f:
                f.write(content + "\nN/A\tN/A\t\t\t")

        return "\tNames retrieved successfully!\t"


    def readStageNames(self):
        """Extract stage names from wiki html"""
        for line in self.html:
            if len(line) > 0 and line[0].isnumeric() and "," in line:
                for key in self.cor:
                    if line[0:3] == key:
                        line = self.cor[key] + line[3:]
                self.processed.append(line)


        with open(DIR + "/stageNames.csv", 'w', encoding='utf8') as f:
            f.write("\n".join(self.processed))
            return "Stage names retrieved successfully!"


