import itertools

weapons = {8:4, 10:5, 25:6, 40:7, 74:8}
armors = {0:0, 13:1, 31:2, 53:3, 75:4, 102:5}
rings = {25:(1,0), 50:(2,0), 100:(3,0), 20:(0,1), 40:(0,2), 80:(0,3), 0:(0,0)}

hits = 100

boss_hits = 109
boss_damage = 8
boss_armor = 2


def play_game (hits, damage, armor, hits_b, damage_b, armor_b):
    """ return True if player loses the game """
    while hits > 0 or hits_b > 0:
        d = max([1, damage - armor_b])
        hits_b -= d
        if hits_b < 0:
            return False
        d_b = max([1, damage_b - armor])
        hits -= d_b
        if hits < 0:
            return True
    assert(False)

def can_lose_with (gold):
    for weapon in weapons.items():
        for armor in armors.items():
            for r in itertools.combinations (rings.keys(), 2):
               # print(weapon)
               # print(armor)
                ring = [rings[x] for x in r]
               # print(ring)
                # without rings
                cost = weapon[0] + armor[0]
                if cost == gold and play_game (hits, weapon[1], armor[1], boss_hits, boss_damage, boss_armor):
               #     print(f'\tcan with with this combo: weapon: {weapon}, armor: {armor}. cost = {cost}')
                    return True
                # with rings
                cost += sum(r)
                if cost == gold and play_game (hits, weapon[1] + sum([ring[x][0] for x in range(len(ring))]), armor[1] + sum([ring[x][1] for x in range(len(ring))]), boss_hits, boss_damage, boss_armor):
               #     print(f'\tcan with with this combo: weapon: {weapon}, armor: {armor}. rings: {ring}. cost = {cost}. {r}')
                    return True
    return False

gold_left = 8
gold_right = 10000

for g in range(1000):
    if can_lose_with(g):
        print (f'can lose with {g}')

#print(gold_left, gold_right)
#print(can_lose_with (gold_left))
#print(can_lose_with (gold_right))





