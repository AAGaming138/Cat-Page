"""Script that converts wiki csv into a form readable by UnitPageMaker"""
from common import *

class WikiReader:

    def __init__(self, page):
        self.url = f"https://battle-cats.fandom.com/wiki/{page}?action=raw"
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
        return webpage.read().decode("UTF-8")


    def readNames(self):
        """Extract names from wiki html"""
        if "Cat (Normal Cat)" in self.html:
            # write content into catNames.tsv
            with open(DIR + "/catNames.tsv", 'w', encoding='utf8') as f:
                f.write(self.html + "\nN/A\tN/A\t\t\tN/A\tN/A")

        elif self.html == "Unable to open URL! (No connection?)":
            return self.html

        else:
            if "2000\n021\t" in self.html:
                # fill in missing 019 and 020 between The Face and Ms Sign
                content = self.html.replace("The Face (Floating)\t99999\t2000\n021",
                                          "The Face (Floating)\t99999\t2000\n"
                                          "019\tN/A\t\t\t\n020\tN/A\t\t\t\n021")
            # write content into enemyNames.tsv
            with open(DIR + "/enemyNames.tsv", 'w', encoding='utf8') as f:
                f.write(content + "\nN/A\tN/A\t\t\t")

        return "\tNames retrieved successfully!\t"


    def readStageNames(self):
        """Extract stage names from wiki html"""
        if self.html == "Unable to open URL! (No connection?)":
            return self.html

        with open(DIR + "/stageNames.csv", 'w', encoding='utf8') as f:
            f.write(self.html.strip("<pre>\n").strip("\n</pre>"))
            return "Stage names retrieved successfully!"


    def readStats(self):
        """Extract stats section"""
        started = False
        content = []
        for line in self.html.split("\n"):
            if line and line == "==Stats==":
                content.append(line)
                started = True
                continue

            if started:
                if line[:2] != "==":
                    content.append(line)
                else:
                    break

        return "\n".join(content).strip("\n")