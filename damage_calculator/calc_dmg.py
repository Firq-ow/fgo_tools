# Formula

# damage for this card =
# (servantAtk * npDamageMultiplier *
# (firstCardBonus + (cardDamageValue * (1 + cardMod))) *
# classAtkBonus * triangleModifier * attributeModifier * randomModifier * 0.23 *
# (1 + atkMod - defMod) * criticalModifier * extraCardModifier * (1 - specialDefMod) *
# (1 + powerMod + selfDamageMod + (critDamageMod * isCrit) + (npDamageMod * isNP)) *
# (1 + ((superEffectiveModifier - 1) * isSuperEffective))) + dmgPlusAdd + selfDmgCutAdd +
# (servantAtk * busterChainMod)

class CalculateDamage:

    def __init__(self):
        self.all_values = []

    def parse_values(self, string_in):
        fields_in = string_in.split()
        return fields_in
