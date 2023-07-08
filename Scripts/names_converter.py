"""Script that converts wiki csv into a form readable by UnitPageMaker"""
from common import *

def get_names(unit):
    start = "https://battle-cats.fandom.com/wiki/Module:"
    # request from bc wiki
    try:
        webpage = request.urlopen(start + unit)
    except urllib.error.URLError:
        return "Unable to open URL! (No connection?)"
    # extract and decode html
    html = webpage.read().decode("UTF-8").split("\n")

    lines = []

    for line in html:
        if line:
            if line[0:3] == "Num" or line[0:3] == "Ima" or line[0].isnumeric():
                # keep lines that have csv content in them
                lines.append(line)

    # remove </div> elements in the last line of csv
    lines[-1] = lines[-1][0:-17]

    # change tab characters into commas
    content = "\n".join(lines)

    if "Cat (Normal Cat)" in content:
        # write content into catNames.csv
        with open(DIR + "/catNames.csv", 'w', encoding='utf8') as f:
            f.write(content + "\nN/A\tN/A\t\t\tN/A\tN/A")

    else:
        if "2000\n021\t" in content:
            # fill in missing 019 and 020 between The Face and Ms Sign
            content = content.replace("The Face (Floating)\t99999\t2000\n",
                             "The Face (Floating)\t99999\t2000\n"
                             "019\tN/A\t\t\t\n020\tN/A\t\t\t\n")
        # write content into enemiesNames.csv
        with open(DIR + "/enemyNames.csv", 'w', encoding='utf8') as f:
            f.write(content + "\nN/A\tN/A\t\t\t")

    return "Names retrieved successfully!"