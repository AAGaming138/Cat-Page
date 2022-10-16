"""Program that is used everywhere"""
import csv, os, math, re
import time, datetime
import builtins
from typing import Union
from pathlib import Path
DIR = Path(__file__).parent.absolute()

current_ver = "11.9"
data_mines = str(DIR).replace('\\', '/') + f'/Version {current_ver}.0'

br = "\n"

class Options:
    """Options for terminal"""
    wiki:           bool    # output is wiki only
    table:          bool    # output is table only
    catfruit:       bool    # output is catfruit only
    talents:        bool    # output is talent only

Options.wiki = False
Options.table = False
Options.catfruit = False
Options.talents = False


def logfunc(func):
    """For debugging purposes, also for learning decorators"""
    def innerfunc(*args, **kwargs):
        with open("log.txt", 'a', encoding="utf-8") as f:
            f.write(f"Called {func.__name__} with arguments {', '.join([str(arg) for arg in args])} "
                    f'''{f"and keyword arguments {', '.join([str(kwarg) for kwarg in kwargs])} "
                    if len(kwargs) > 0 else ""}'''
                    f"at {datetime.datetime.now()}\n")
        return func(*args, **kwargs)
    return innerfunc


def load(t: int) -> str:
    """Activates time gap for debugging purposes"""
    if t < 0: return ''
    for i in range(t):
        time.sleep(0.1)
        # print('.', end='') if i != t - 1 else print('')
    return ''


def quit(message: str, loading: bool = True) -> None:
    """Quits the code with message"""
    load(20 if loading else 0)
    print(message)
    builtins.quit()

@logfunc
def opencsv(filename: str, header: bool = False) -> list:
    """Opens and reads csv file, return list of data"""
    try:
        with open(filename, 'r', encoding='utf8', newline='') as f:
            rf = csv.reader(f)
            if header: next(rf)
            return [row for row in rf]
    except (UnicodeDecodeError, StopIteration):
        quit("Unit is unobtainable.")


def commarise(num: Union[int, float, str]) -> Union[int, float, str]:
    """Wow! I wonder what this does"""
    if type(num) not in [int, float]: return num
    else: return f"{num:,}"