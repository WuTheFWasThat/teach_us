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

def validate_round(round, clues=None, debug=False, verify=False, clue_winner=None):
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
        trick_done = False
        for j, play in enumerate(trick.split(' ')):
            assert not trick_done
            expect_true(
                (play == '-') == (dog or (len(hands[player]) == 14)), 
                "Player %d should pass when done: %s %s %s" % (player, play, dog, ''.join(sorted(hands[player])))
            )
            if dog: 
                trick_done = True
                assert play == '-'
            if play == '-' or play == '.':
                passes += 1
                if passes == 3:
                    trick_done = True
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
                        assert trick == 'd -'
                        dog = True
                if winner is None and len(hands[player]) == 14:
                    winner = player
            if debug:
                if play != '-' and play != '.':
                    print('    Player %d played %s, %d cards remaining' % (player, play, 14 - len(hands[player])))
                # print('  Remaining hand: ', sorted(hands[player]))
            player = (player + 1) % 4
        assert trick_done, trick
        if not dog:
            winners.append(player)
            print('    Winner: ', player, 'Points: ', points)
        if dragon_win:
            round_points[(player + 1) % 4] += points
        else:
            round_points[player] += points
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
        if clue_winner:
            winner = clue_winner
        (part1, part2) = clues
        phrase = ''
        for clue in part1.split(' '):
            assert clue[1] == '.' 
            index = int(clue[2:]) - 1
            if clue[0] == '1':
                # print('card', hands[winner][index])
                phrase += num2char(card2num(hands[winner][index]))
            else:
                # print('card', hands[(winner + 2) % 4][index])
                phrase += num2char(13 + card2num(hands[(winner + 2) % 4][index]))

        phrase += '.'
        for clue in part2.split(' '):
            assert clue[1] == '.' 
            index = int(clue[2:]) - 1
            if clue[0] == '1':
                # print('card', hands[(winner + 2) % 4][index])
                phrase += num2char(card2num(hands[(winner + 2) % 4][index]))
            else:
                # print('card', hands[winner][index])
                phrase += num2char(13 + card2num(hands[winner][index]))
        print('Clued phrase: ', phrase)

# DOT MEANS PASS
# DASH MEANS FORCED PASS (except bomb, should handle that too)

# TODOS AFTER HTML:
# - fill in phoenix and mahjong and dragon choices
# - make forced passes for bombs
# - get rid of passes on last round

res = sys.argv[1]
nums = [char2num(char) for char in res]
# print(num2char(summod(nums)))

# TEACH US, IN LIFE
# 0: 13456789TTQQAD (56789Q)
# 1: 355668899TTJdP
# 2: 223356789KKKKA (358AA)
# 3: 2244477QQJJJAA
round1 = [ 
  '3456789 . . .',
  '1 3 A . . .',
  '2233 JJQQ . . .',
  '44422 . . .',
  '77 TT . . AA . . KKKK . . .',
  '56789 . . .',
  '- J A P - - D . - -',
  'QQ . - -',
]


clues1 = (
    '2.5 1.10 1.1 1.4 1.13 2.6 2.4',
    '1.7 2.1 1.14 1.7 1.4 1.3'
)

# LUCKY AND SKILLED
# 0: 13456789TJQKAP
# 1: 3556668TTTJJKD
# 2: 2222445899JQAd (8QJ 954)
# 3: 33477789QQKKAA
round2 = [
    '1P3456789TJQKA . . .',
    '- 3 5 8 - . J A - . .',
    '4 - 8 Q . - K A . - .',
    '44 . - 55 99 QQ - . .',
    '77733 - TTTJJ 2222 . - .',
    'd -',
    '- 666 . . -',
    'D . . -',
    '- 8 . - -'
]
clues2 = (
    '1.12 2.14 1.3 1.11 2.3',
    '2.6 1.2 1.7 1.3 1.3 1.1 1.6'
)

# WISE AND GOOD WILLED
# 0: 12444677889TAA
# 1: 2233599TTJJAQK (259T)
# 2: 5566788JQQAdDP
# 3: 23345679TJQKKK (45679TQ) 

round3 = [
    '1 A . . .',
    '2233 5566 . . 99TT . . .', 
    '5 7 . 8 Q A . . .',
    '88 . . JJ QQ . . .', 
    'JP . . .', 
    'D . . .', 
    'd -', 
    '444 . - .',
    '6789T . - 9TJQK . . -',
    '234567 . . -',
    'KK AA . - .',
    '2 K - . .',
    '- - 3 . - -',
]
clues3 = (
    '2.2 1.6 2.10 1.10',
    '1.11 2.2 2.3 1.8 2.9 1.1 1.4 1.4 1.9 1.8'
)

# HUSBAND AND WIFE
# 0:  122233377799AP
# 1:  244888TTTQQQQA (248TA) <- should win
# 2:  34455666JJJADd
# 3:  5567899TJKKKKA (5689A) 
round4 = [
    '222333 . . .',
    '77799 88844 . . .',
    '2 3 5 A QQQQ . . .',
    'TTT JJJ . . .',
    '445566 . . .',
    '6 9 . A - KKKK . - .',
    '56789TJ . - .',
    'A . - .',
]
clues4 = (
    '1.1 2.10 2.8 1.6 1.14 2.14 1.5',
    '2.13 1.11 1.8 1.7'
)

# STRAIGHT FLUSH BOMB
# dog to partner for mahjong?
# GRAND VOWS FULFILLED
# 0:  147788JJJQQAAD (478A) <- should win
# 1:  2235999TTJKKKK
# 2:  2345634567QQAd (245669TQQA) 
# 3:  2345667889TTAP

# A1dP
round5 = [
    '1 3 . A . . .',
    '2345678 . . .',
    '6P89T . . 23456 . . .',
    'd -',
    '7788 99TT . . JJQQ . . .',
    '4 5 A . D . . .',
    'A KKKK . . .',
    '22 . . .',
    '9 Q . A . . .',
    'J . Q . - .',
    '34567 . - .'
]
clues5 = (
    '1.3 2.12 1.12 2.7 1.10',
    '1.11 2.2 2.3 1.8 2.9 1.1 1.4 1.4 1.9 1.8'
)

# WINNING PLAYER SHOULD HAVE:
# green on left, red on right

    # LUCKY AND SKILLED
    # 1: (Q3J6)
    # 3: 
    # AND WIFE

# validate_round(
#     round1, clues=clues1, debug=True)
# validate_round(
#     round2, clues=clues2, debug=True)
#validate_round(
#    round3, clues=clues3, debug=True, clue_winner=1)
# validate_round(
#     round4, clues=clues4, debug=True)
validate_round(
    round5, clues=clues5, debug=True)

print()
poem = [
    'teach us,          in life',
     # to be
    'lucky        and   skilled',        # mahjong, sword
     # to be
    'wise         and   good willed',     # star, dog
     # as
    'husband      and   wife',         # dragon, phoenix
     # to have
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
