import sys

def char2num(char):
    assert len(char) == 1
    return ord(char.lower()) - ord('a') + 1

def summod(nums):
    return ((sum(nums) - 1) % 26) + 1

def num2char(num):
    return chr(ord('a') + num - 1)

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
                phoenix = True
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
    if phoenix:
        return '*'
    else:
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

    player = -1
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
        expect_done = False
        dog = False
        for play in trick:
            player = (player + 1) % 4
            expect_true(
                (len(hands[player]) == 14) == (play == 'x'),
                "Player should play x only when done: %s %s %s" % (player, play, hands[player])
            )
            expect_true(not expect_done, "Round over?!")
            assert not expect_done
            if play == '-' or play == 'x':
                passes += 1
                if passes == 3:
                    expect_done = True
            else:
                passes = 0
                for card in play:
                    hands[player].append(card)
                    card_counts[card] -= 1
                    expect_true(
                        card_counts[card] >= 0, 
                        "Too many %s" % card
                    )
                    if card == 'd':
                        assert len(trick) == 1
                        expect_done = True
                        dog = True
            if debug:
                if play != '-':
                    print('    Player', player, 'played', play)
                # print('  Remaining hand: ', sorted(hands[player]))
            if dog:
                player = (player + 2) % 4
        assert expect_done
        winners.append(player)
    print()
    print('Winners were', winners)
    print('Hands were')
    for (player, hand) in hands.items():
        hand = list(hand)
        while len(hand) < 14:
            hand.append('.')
        print('%d: %s' % (player, ''.join(sorted(hand))))
        assert len(hand) <= 14, "Hand too large!"
    print('Cards remain: ', ''.join([card * count for (card, count) in card_counts.items()]))
    # assert expect_done
res = sys.argv[1]
nums = [char2num(char) for char in res]
# print(num2char(summod(nums)))

PASS = 0
rounds = [
    [ # TEACH US
        ['1', '6', 'Q',  'A', '-', '-', '-'],
        ['22', '88', 'KK', '-', '-', '-'],
        ['2', '3', '6', 'Q',  'A', '-', '-', '-'],
    ],
    # OF LIFE
    [ # HUSBAND 
        ['123456', '-', '-', '456789', '-', '-', '-'],
        ['22299', '-', '-', 'JJJ88', '-', '-', '-'],
        ['3', '6', '9', 'A', '-', '-', '-'],
        ['7', '9', '-', 'J', '-', 'A', '-', '-', '-'],
        ['7', 'Q', '-', '-', '-']
        # ['5566', '-' ,'-', 'TTQQ', '-', '-', '-'],
        # ['4', 'T', 'K', 'A', '-', '-', '-'],
        # ['8899', '-', '-', 'QQQQ',  '-', '-', '-'],
        # ['d'],
    ],
    # AND WIFE
]

for round in rounds:
    validate_round(round)

    print(list(
        sum_trick(trick) for trick in round
    ))

validate_round(rounds[1], True)

print()
poem = [
    'teach us, in life',
     # 'to be'
    'lucky and skilled',      # mahjong, sword
     # 'to be'
    'smart and good willed',  # dog, star
     # 'to be'
    'husband and wife',       # phoenix, pagoda
     # 'to have'
    'grand bets fulfilled',   # dragon, jade
]
for line in poem:
    print(line)
    print(' '.join(str(char2num(x)) for x in line))

"""
                 TEACH US          IN LIFE,
to have been     _____ ___         _______,     200-0
to be            _____ ___     ____-______,     400-0
to become        _______          ___ ____,     600-0
to have          _____ ____      _________.    1000-0
"""
