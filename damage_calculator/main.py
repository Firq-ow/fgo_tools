"""
main module
"""
from calc_dmg import CalculateDamage
from get_atlas_json import AtlasFunctions
from get_atlas_json import DateError, HashError

# servantATK    = 'totalAttack'
# servantNP     = 'np'
# atkMod        = 'attack'
# defMod        = 'defense'
# npMod         = 'npdmg'
# powerMod      = 'special'
# cardMod       = 'cardmod'
# npspMod       = 'npspecial'
# adv           = 'classadvantage'
# fa            = 'flatattack'
# npMult        = 'npmultiplier'
# cardMult      = 'cardmultiplier'
# cMod          = 'classmod'


def main():
    """
    main fuction
    :return: None
    """
    atlas = AtlasFunctions()
    try:
        atlas.get_data()
    except (DateError, HashError):
        print("Atlas Data was already up to date")

    in_str = "!dmg Shishou totalAttack15000 np5 cardmod50 special100 " \
             "classmod1.05 cardmultiplier2 npmultiplier2400 classadvantage2 cardmod50"
    calc = CalculateDamage()
    calc.parse_values(in_str)
    print(calc.all_values)
    dmg = calc.calculate()
    print(f"Norm: {dmg[0]}\nLow: {dmg[1]}\nHigh: {dmg[2]}")


if __name__ == '__main__':
    main()
