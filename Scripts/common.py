"""Program that is used everywhere"""
import csv, os, math, re
import time, datetime
import builtins
from typing import Union
from pathlib import Path
DIR = str(Path(__file__
               ).parent.absolute()).replace('\\', '/').replace("/Scripts", "")

current_ver = "11.10"
data_mines = DIR + f'/Version {current_ver}.0'

br = "\n"

class Options:
    """Options for output"""

    def __init__(self):
        self.cost = False
        self.table = False
        self.catfruit = False
        self.talents = False
        self.category = False


def logfunc(func):
    '''For debugging purposes'''
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