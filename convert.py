import sys

def char2num(char):
    assert len(char) == 1
    return ord(char.lower()) - ord('a') + 1

def summod(nums):
    return ((sum(nums) - 1) % 26) + 1

def num2char(num):
    return chr(ord('a') + num - 1)

def sum_play(play):
    nums = []
    if play == '-' or play == 'x':
        return 0
    for card in play:
        if card == '1':
            nums.append(1)
        elif card == 'd':
            return 'd'
        elif card == 'D':
            nums.append(-1)
        elif card == 'P':
            continue
        elif card == 'T':
            nums.append(10)
        elif card == 'J':
            nums.append(11)
        elif card == 'Q':
            nums.append(12)
        elif card == 'K':
            nums.append(13)
        elif card == 'A':
            nums.append(1)
        else:
            num = int(card)
            assert num < 10
            assert num > 1
            nums.append(num)
    return num2char(summod(nums))

def sum_trick(trick):
    nums = []
    phoenix = False
    for play in trick:
        if play == '-' or play == 'x':
            continue
        for card in play:
            if card == '1':
                nums.append(1)
            elif card == 'd':
                assert len(trick) == 1
                return None
            elif card == 'D':
                nums.append(-1)
            elif card == 'P':
                continue
            elif card == 'T':
                nums.append(10)
            elif card == 'J':
                nums.append(11)
            elif card == 'Q':
                nums.append(12)
            elif card == 'K':
                nums.append(13)
            elif card == 'A':
                nums.append(1)
            else:
                num = int(card)
                assert num < 10
                assert num > 1
                nums.append(num)
    return num2char(summod(nums))

def validate_round(round, debug=False, verify=False):
    card_counts = {
        '2': 4,
        '3': 4,
        '4': 4,
        '5': 4,
        '6': 4,
        '7': 4,
        '8': 4,
        '9': 4,
        'T': 4,
        'J': 4,
        'Q': 4,
        'K': 4,
        'A': 4,
        '1': 1,
        'd': 1,
        'P': 1,
        'D': 1,
    }
    hands = {
        0: [],
        1: [],
        2: [],
        3: [],
    }

    player = 0
    winners = []

    def expect_true(pred, message):
        if verify:
            assert pred, message
        else:
            if not pred:
                print("ERROR: ", message)

    for i, trick in enumerate(round):
        if debug:
            print('  Trick', i)
        passes = 0
        dog = False
        for j, play in enumerate(trick):
            if j != 0:
                player = (player + 1) % 4
            expect_true(
                (len(hands[player]) == 14) == (play == 'x'),
                "Player %d should play x only when done: %s %s" % (player, play, ''.join(sorted(hands[player])))
            )
            if play == '-' or play == 'x':
                passes += 1
                assert passes < 3
            else:
                passes = 0
                phoenix = False
                for card in play:
                    if not phoenix:
                        hands[player].append(card)
                        card_counts[card] -= 1
                        expect_true(
                            card_counts[card] >= 0, 
                            "Too many %s" % card
                        )
                    phoenix = card == 'P'
                    if card == 'd':
                        assert len(trick) == 1
                        dog = True
            if debug:
                if play != '-' and play != 'x':
                    print('    Player %d played %s, %d cards remaining' % (player, play, 14 - len(hands[player])))
                # print('  Remaining hand: ', sorted(hands[player]))
            if dog:
                player = (player + 1) % 4
        winners.append(player)
    print()
    print('Winners were', winners)
    print('Hands were')
    for (player, hand) in hands.items():
        hand = list(hand)
        while len(hand) < 14:
            hand.append('.')
        print('%d: %s' % (player, ''.join(sorted(hand))))
        expect_true(len(hand) <= 14, "Hand too large!")
    print('Cards remain: ', ''.join([card * count for (card, count) in card_counts.items()]))
res = sys.argv[1]
nums = [char2num(char) for char in res]
# print(num2char(summod(nums)))

PASS = 0
rounds = [
    [ # TEACH US
        ['1', '6', 'Q',  'A'],
        ['22', '88', 'KK'],
        ['2', '3', '6', 'Q',  'A'],
    ],
    # OF LIFE
    # [ # HUSBAND 
    #     ['123456', '-', '-', '456789'],
    #     ['22299', '-', 'JJJ88'],
    #     ['3', '7', '8', '-', 'A'],
    #     ['7', '9', 'J', 'A', 'D'],
    #     # ['7', 'Q'],
    #     # ['5566', '-' ,'-', 'TTQQ'],
    #     # ['4', 'T', 'K', 'A'],
    #     # ['8899', '-', '-', 'QQQQ'],
    #     # ['d'],
    #     ['2', '-', '-', 'KKKK'],
    #     ['d'],
    #     ['2', '-', 'x', '7', '9', '-', 'x', 'TTTT', 'QQQQ'],
    #     ['445566'],
    # ],
    [ # HUSBAND 
        ['1P345678'],
        ['66699', 'JJJ77'],
        ['99444', '55533', '33KKK'],
        ['22', '-', '88', 'QQ', 'AA'],
        ['7', '8', 'K', 'A'],
        ['2', 'J', 'A', '-', 'TTTT'],
        ['d'],
    ],
    # AND WIFE
]

for round in rounds:
    validate_round(round)

    print(list(
        # sum_trick(trick) for trick in round
        sum_play(trick[-1]) for trick in round
    ))

validate_round(rounds[1], True)
print(list(
    # sum_trick(trick) for trick in rounds[1]
    sum_play(trick[-1]) for trick in rounds[1]
))

print()
poem = [
    'teach us, in life',
     # 'to be'
    'lucky and skilled',        # mahjong, sword
     # 'to be'
    'wise and good willed',     # star, dog
     # 'to be'
    'husband and wife',         # dragon, phoenix
     # 'to have'
    'grand stakes fulfilled',   # jade, pagoda 
]
for line in poem:
    print(line)
    print(' '.join(str(char2num(x)) for x in line))

"""
                 TEACH US          IN LIFE,     100-0
to be            _____ ___         _______,     200-0
to be            _____ ___     ____-______,     400-0
to become        _______          ___ ____,     600-0
to have          _____ ____      _________.    1000-0
"""

print(u"")
