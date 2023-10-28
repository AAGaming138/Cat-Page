"""Testing script. Not in use at the moment"""

def link(ability: str, type: str = 'default'):
    if type == 'default':
        l = ability
    elif type == 'res':
        l = "Resist"
    elif type == 'stat':
        l = "Stat Enhancements"
    elif type == 'tar':
        return f"Target [[:Category:{ability} Enemies|{ability}]]"
    else:
        l = type
    return f"[[Special Abilities#{l}|{ability}]]"


talents = {
    1: link("Weaken"),
    2: link("Freeze"),
    3: link("Slow"),
    5: link("Strong Against"),
    6: link("Tough Vs", "Resistant"),
    7: link("Massive Damage"),
    8: link("Knockback"),
    10: link("Attack Up", "Strengthen"),
    11: link("Survives", "Survive"),
    13: link("Critical"),
    14: link("Zombie Killer"),
    15: link("Barrier Breaker"),
    16: link("Money Up", "Extra Money"),
    17: link("Wave Attack"),
    18: link("Resist Weaken", "res"),
    19: link("Resist Freeze", "res"),
    20: link("Resist Slow", "res"),
    21: link("Resist Knockback", "res"),
    22: link("Resist Wave", "res"),
    25: link("Cost Down", "stat"),
    26: link("Recover Speed Up", "stat"),
    27: link("Move Speed Up", "stat"),
    29: link("Curse Immunity", "Immune to Curse"),
    30: link("Resist Curse", "res"),
    31: link("Attack Buff", "stat"),
    32: link("Defense Buff", "stat"),
    35: link("Black", "tar"),
    36: link("Metal", "tar"),
    37: link("Angel", "tar"),
    38: link("Alien", "tar"),
    39: link("Zombie", "tar"),
    40: link("Relic", "tar"),
    41: link("Traitless", "tar"),
    44: link("Immune to Weaken"),
    45: link("Immune to Freeze"),
    46: link("Immune to Slow"),
    47: link("Immune to Knockback"),
    48: link("Immune to Waves"),
    49: link("Warp Blocker"),
    50: link("Savage Blow"),
    51: link("Dodge Attack"),
    52: link("Resist Toxic", "res"),
    53: link("Immune to Toxic"),
    54: link("Resist Surge", "res"),
    55: link("Immune to Surge", "Evade Surge"),
    56: link("Surge Attack", "Surge Attacks"),
    57: link("Aku", "tar"),
    58: link("Shield Piercing"),
    59: link("Soulstrike"),
    60: link("Curse"),
    61: link("Attack Frequency Up", "stat"),
    62: link("Mini-Wave"),
    63: link("Colossus Slayer"),
    64: link("Behemoth Slayer"),
    65: link("Mini-Surge")
}

for key in talents:
    print(talents[key])