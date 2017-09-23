import sys

def char2num(char):
    assert len(char) == 1
    return ord(char.lower()) - ord('a') + 1

def char2trits(char):
    num = char2num(char)
    trits = [num // 9, (num % 9) // 3, num % 3]
    return trits

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
            return 'd'
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
                nums.append(char2num('d'))
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
        ['88222', '55533', '33KKK'],
        ['44', '-', '99', 'QQ', 'AA'],
        ['7', '8', 'K', 'A'],
        ['2', 'J', 'A', '-', 'TTTT'],
        ['d'],
    ],
    [ # GOOD-WILLED
        ['345678'],
        ['JJJ44'],
        ['12345'],
        ['d'],
        ['456789T'],
        ['9P'], 
        ['66'],
        ['Q'],
        [''],
        ['D'],
    ],
    [ # AND WIFE
        ['1', 'A'],
        ['6789T'],
        ['d'],
        ['-'],
        ['456789T'],
        ['9P'], 
        ['66'],
        ['Q'],
    ],
    # [ # HUSBAND 
    #     ['????????'],
    #     ['???99', 'JJJ77'],
    #     ['99444', '55533', '33???'],
    #     ['22', '-', '88', 'QQ', 'AA'],
    #     ['7', '8', '?', 'A'],
    #     ['2', 'J', 'A', '-', 'TTTT'],
    #     ['d'],
    # ],
    # AND WIFE
]

for round in rounds:
    validate_round(round)

    print(list(
        # sum_trick(trick) for trick in round
        sum_play(trick[-1]) for trick in round
    ))

validate_round(rounds[-1], True)
print(list(
    # sum_trick(trick) for trick in rounds[1]
    sum_play(trick[-1]) for trick in rounds[-1]
))

print()
poem = [
    'teach us,          in life',
     # 'to be'
    'lucky        and   skilled',        # mahjong, sword
     # 'to be'
    'wise         and   good willed',     # star, dog
     # 'to be'
    'husband      and   wife',         # dragon, phoenix
     # 'to have'
    'grand vows         fulfilled',   # jade, pagoda 
]
for line in poem:
    print(line)
    print(' '.join(str(char2num(x)) for x in line))

class colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def char2card(x):
    if x == ' ' or x == ',':
        return x
    num = char2num(x)
    card = (num - 1) % 13 + 1
    color = colors.RED if num > 13 else colors.GREEN
    cardstr = str(card)
    if card == 1:
        cardstr = 'A'
    elif card == 10:
        cardstr = 'T'
    elif card == 11:
        cardstr = 'J'
    elif card == 12:
        cardstr = 'Q'
    elif card == 13:
        cardstr = 'K'
    return color + cardstr + colors.END


for line in poem:
    print(line)
    print(''.join(char2card(x) for x in line))

# MECHANICS (meh):
#   sum of lead numbers mod 26 (mahjong)
#   num passes in trinary (dog)
#   permutation of suits of numbers (phoenix)
#   winning numbers (dragon)

"""
                 TEACH US          IN LIFE,    
to be            _____ ___         _______,    
to be            _____ ___     ____-______,    
to become        _______          ___ ____,    
to have          _____ ____      _________.    
"""

print(u"")

"""
[0, 1, 2, 3] = A
[0, 1, 3, 2] = B
[0, 2, 1, 3] = C
[0, 2, 3, 1] = D
[0, 3, 1, 2] = E
[0, 3, 2, 1] = F
[1, 0, 2, 3] = G
[1, 0, 3, 2] = H
[1, 2, 0, 3] = I
[1, 2, 3, 0] = J
[1, 3, 0, 2] = K
[1, 3, 2, 0] = L
[2, 0, 1, 3] = M
[2, 0, 3, 1] = N
[2, 1, 0, 3] = O
[2, 1, 3, 0] = P
[2, 3, 0, 1] = Q
[2, 3, 1, 0] = R
[3, 0, 1, 2] = S
[3, 0, 2, 1] = T
[3, 1, 0, 2] = U
[3, 1, 2, 0] = V
[3, 2, 0, 1] = W
[3, 2, 1, 0] = X
"""

# for i in 'abcdefghijklmnopqrstuvwxyz':
#     print(char2trits(i))

"""
1: 123456789QQKAD
3: 223356789JJJJA
2: 2355668899TTdP
4: 44477TTQQKKKAA

1: 3459JQ
2: 68QA

1: 3459JQ
2: 68QA
"""
