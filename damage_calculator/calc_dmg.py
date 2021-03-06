# Formula

#  var total = atk * np * cardType * advantage * servantClass * 0.23 *
#                 (1 + attackBuffs + defenseDebuffs) *
#                 (1 + cardBuffs + cardDebuffs) *
#                 (1 + npBuffs + spBuffs) *
#                 (1 + npspBuffs) * esAdvantage + flatAttack;


class CalculateDamage:

    def __init__(self):

        self.all_values = dict(servantATK=[0, 'totalAttack'],
                               servantNP=[0, 'np'],
                               atkMod=[0, 'attack'],
                               defMod=[0, 'defense'],
                               powerMod=[0, 'special'],
                               npMod=[0, 'npdmg'],
                               cardMod=[0, 'cardmod'],
                               npspMod=[0, 'npspecial'],
                               adv=[1, 'classadvantage'],
                               fa=[0, 'flatattack'],
                               npMult=[0, 'npmultiplier'],
                               cardMult=[0, 'cardmultiplier'],
                               cMod=[1, 'classmod'])

    def parse_values(self, string_in):
        if string_in[:4] != '!dmg':
            print(f"Character {string_in[:4]} is not the toggle character.")
            raise NameError

        # Split up string into individual values
        fields_in = string_in.split()

        # cycle through input fields, parse input args
        for index, fields in enumerate(fields_in):
            tags = ''.join(filter(str.isalpha, fields))
            if not tags and index == 1:
                tags = fields
            for item in self.all_values.items():
                if item[1][1] == tags:
                    values = float(fields.replace(tags, ''))

                    if float(item[1][0]) == float(0):
                        item[1][0] += values
                    elif float(item[1][0]) < float(2):
                        item[1][0] = values
                    else:
                        item[1][0] += values

                    val = {item[0]: item[1]}

                    self.all_values.update(val)

        return fields_in

    def calculate(self):
        dmg_arr = [0, 0, 0]

        cardmult = 1
        if self.all_values["cardMult"][0] == float('0'):
            cardmult = 1.5
        elif self.all_values["cardMult"][0] == float('2'):
            cardmult = 0.8

        # norm dmg
        dmg_arr[0] = round(int(self.all_values["servantATK"][0]) * (int(self.all_values["npMult"][0]) * 0.01) * \
                     cardmult * 0.23 * float(self.all_values["cMod"][0]) *
                     (1 + (int(self.all_values["atkMod"][0]) * 0.01) + (int(self.all_values["defMod"][0]) * 0.01)) * \
                     (1 + (int(self.all_values["cardMod"][0]) * 0.01)) * \
                     (1 + (int(self.all_values["npMod"][0]) * 0.01) + (int(self.all_values["powerMod"][0]) * 0.01)) * \
                     (1 + (int(self.all_values["npspMod"][0]) * 0.01)) * int(self.all_values["adv"][0]) + \
                     int(self.all_values["fa"][0]))

        # min dmg
        dmg_arr[1] = round(0.9 * (dmg_arr[0] - int(self.all_values["fa"][0])) + int(self.all_values["fa"][0]))
        # max dmg
        dmg_arr[2] = round(1.1 * (dmg_arr[0] - int(self.all_values["fa"][0])) + int(self.all_values["fa"][0]))

        return dmg_arr
