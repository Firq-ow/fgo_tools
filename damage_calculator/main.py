from calc_dmg import CalculateDamage
from get_atlas_json import get_data as update_atlas
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
    try:
        update_atlas()
    except (DateError, HashError) as e:
        print("Atlas Data was already up to date")
        pass

    in_str = "!dmg Shishou totalAttack15000 np5 cardmod50 special100 classmod1.05 cardmultiplier2 npmultiplier2400 classadvantage2 cardmod50"
    c = CalculateDamage()
    c.parse_values(in_str)
    print(c.all_values)
    dmg = c.calculate()
    print(f"Norm: {dmg[0]}\nLow: {dmg[1]}\nHigh: {dmg[2]}")


if __name__ == '__main__':
    main()
