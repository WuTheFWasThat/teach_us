import sys

def char2num(char):
    assert len(char) == 1
    return ord(char.lower()) - ord('a') + 1

def char2trits(char):
    num = char2num(char)
    trits = [num // 9, (num % 9) // 3, num % 3]
    return trits

def card2num(card):
    if card == 'T':
        return 10
    elif card == 'J':
        return 11
    elif card == 'Q':
        return 12
    elif card == 'K':
        return 13
    elif card == 'A':
        return 1
    else:
        i = int(card)
        assert i > 1
        assert i < 10
        return i

def summod(nums):
    return ((sum(nums) - 1) % 26) + 1

def num2char(num):
    return chr(ord('a') + num - 1)

def validate_round(round, clues=None, debug=False, verify=False):
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
    winner = None
    winners = []
    round_points = { 0:0, 1:0, 2:0, 3:0 }

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
        points = 0
        dog = False
        dragon_win = False
        for j, play in enumerate(trick.split(' ')):
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
                for card in play:
                    if card == '5':
                        points += 5
                    elif card == 'T' or card == 'K':
                        points += 10
                    elif card == 'D':
                        dragon_win = True
                        points += 25
                    elif card == 'P':
                        points -= 25
                    hands[player].append(card)
                    card_counts[card] -= 1
                    expect_true(
                        card_counts[card] >= 0, 
                        "Too many %s" % card
                    )
                    if card == 'd':
                        assert len(trick) == 1
                        dog = True
                if winner is None and len(hands[player]) == 14:
                    winner = player
            if debug:
                if play != '-' and play != 'x':
                    print('    Player %d played %s, %d cards remaining' % (player, play, 14 - len(hands[player])))
                # print('  Remaining hand: ', sorted(hands[player]))
            if dog:
                player = (player + 1) % 4
        winners.append(player)
        if dragon_win:
            round_points[(player + 1) % 4] += points
        else:
            round_points[player] += points
        print('    Winner: ', player, 'Points: ', points)
    print()
    print('Winners were', winners)
    print('Winner was', winner)
    print('Points: ', round_points)
    print('Hands were')
    for (player, hand) in hands.items():
        hand = list(hand)
        while len(hand) < 14:
            hand.append('.')
        print('%d: %s' % (player, ''.join(sorted(hand))))
        expect_true(len(hand) <= 14, "Hand too large!")
    print('Cards remain: ', ''.join([card * count for (card, count) in card_counts.items()]))

    if clues:
        (part1, part2) = clues
        phrase = ''
        for clue in part1.split(' '):
            index = int(clue[1:])
            print('index', index)
            if clue[0] == '1':
                phrase += num2char(card2num(hands[winner][index]))
            else:
                print('card', hands[(winner + 2) % 4][index])
                phrase += num2char(13 + card2num(hands[(winner + 2) % 4][index]))

        phrase += ':'
        for clue in part2.split(' '):
            index = int(clue[1:])
            if clue[0] == '1':
                phrase += num2char(card2num(hands[(winner + 2) % 4][index]))
            else:
                phrase += num2char(13 + card2num(hands[winner][index]))
        print('Clued phrase: ', phrase)

res = sys.argv[1]
nums = [char2num(char) for char in res]
# print(num2char(summod(nums)))

PASS = 0
rounds = [
    [ # TEACH US, IN LIFE
      # 1: 13456789TTQAAD (358AA)
      # 2: 355668899TTJdP
      # 3: 223356789KKKKQ (56789Q)
      # 4: 2244477QQJJJAA
      '3456789',
      '1 3 Q',
      '2233 JJQQ',
      '44477',
      '22 TT - - AA - - KKKK',
      '56789',
      'x J A P x x D',
      'A',
      'Q',
    ],
    # LUCKY AND SKILLED
    # 1: (Q3J6)
    # 3: 
    # AND WIFE
]

all_clues = [
    (
        '212',
        '212',
     )
]

for round, clues in zip(rounds, all_clues):
    validate_round(round, clues=clues, debug=True)


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

1: 3459JQ
2: 68QA

1: 3459JQ
2: 68QA
"""
