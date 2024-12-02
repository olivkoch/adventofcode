import sys
import re
import copy

input_file = sys.argv[1]

with open(input_file, 'r') as fh:
    lines = [a.strip() for a in fh.readlines()]

mk2fun = {0: lambda old: old * 19, 1: lambda old: old + 6, 2: lambda old: old * old, 3: lambda old: old + 3}


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n): 
        yield l[i:i + n]

class Monkey:
    def __init__ (self, items, op, mod, exit1, exit2):
        self.op = op
        self.mod = mod
        self.items = items
        self.exit1 = exit1
        self.exit2 = exit2
        self.inspected = 0

    def keep_items(self, n):
        self.items = self.items[:n]

    def keep_item (self, n):
        self.items = [self.items[n]]

    def clear_items(self):
        self.items = []

    def __str__(self):
        return f'{self.inspected}'


# read data
def read_lines (lines):
    mlines = divide_chunks(lines, 7)
    monkeys = []
    for mstack in mlines:
        data = re.match(r'Monkey (\d+):', mstack[0])
        id = data.groups()[0]
        items = [int(a) for a in mstack[1].split(':')[1].split(',')]
        op = eval('lambda old: ' + mstack[2].split('=')[1])
        mod = int(mstack[3].split(' ')[-1])
        exit1 = int(mstack[4].split(' ')[-1])
        exit2 = int(mstack[5].split(' ')[-1])
        monkeys.append(Monkey(items, op, mod, exit1, exit2))
    return monkeys


# single item
for rounds in [10000]:
    monkeys = read_lines(lines)

    mod = 1
    for m in monkeys:
        mod *= m.mod
    # for i, m in enumerate(monkeys):
    #     if i == 0:
    #         m.keep_item(0)
    #     else:
    #         m.clear_items()

    # for m in monkeys:
    #      print(m)
    # print()

    # run rounds
    ans = []
    for round in range(rounds):
        for m in monkeys:
            while m.items:
                x = int(m.op(m.items.pop(0)) % mod)
                if x % m.mod == 0:
                    monkeys[m.exit1].items.append(x)
                else:
                    monkeys[m.exit2].items.append(x)
                m.inspected += 1
        # for m in monkeys:
        #     print(m)
        # print()
        # x = [len(m.items) for m in monkeys]
        # z = x.index(1)
        # ans.append(z)
        #if monkeys[0].items and monkeys[0].items[0] * 3 % 7 == 0:
        #    print (f'mod 7 found at round {round}')
    # ins = sorted ([m.inspected for m in monkeys], reverse=True)
    # out = ins[0] * ins[1]
#    print(ans)
    print([m.inspected for m in monkeys])
    