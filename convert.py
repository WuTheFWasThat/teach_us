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
        if play == '-':
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

def validate_round(round):
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

    for trick in round:
        passes = 0
        expect_done = False
        for play in trick:
            assert not expect_done
            if play == '-':
                passes += 1
                if passes == 3:
                    expect_done = True
            else:
                passes = 0
                for card in play:
                    hands[player].append(card)
                    card_counts[card] -= 1
                    # assert card_counts[card] >= 0, "Too many %s" % card
                    if card_counts[card] < 0: 
                        print("Too many %s" % card)
                    if card == 'd':
                        assert len(trick) == 1
                        expect_done = True
                        player = (player + 1) % 4
            player = (player + 1) % 4
        assert expect_done
    print('\nHands were\n ', '\n  '.join(['%d: %s' % (player, ''.join(sorted(hand))) for (player, hand) in hands.items()]))
    print('Cards remain: ', ''.join(['%s: %d, ' % (card, count) for (card, count) in card_counts.items() if count > 0]))
    # assert expect_done
res = sys.argv[1]
nums = [char2num(char) for char in res]
# print(num2char(summod(nums)))

PASS = 0
rounds = [
    [ # TEACH US OF LIFE
        ['1', '6', 'Q',  'A', '-', '-', '-'],
        ['22', '88', 'KK', '-', '-', '-'],
        ['23', '6', 'Q',  'A', '-', '-', '-'],
    ],
    [ # HUSBAND AND WIFE
        ['123456', '-', '-', '456789', '-', '-', '-'],
        ['222JJ', '-', '-', 'KKK33', '-', '-', '-'],
        ['3', '4', 'Q', 'A', 'D', '-', '-', '-'],
    ],
]

for round in rounds:
    validate_round(round)

    print(list(
        sum_trick(trick) for trick in round
    ))


print()
poem = [
    'teach us of life',
    'lucky and skilled',      # mahjong, sword
    'smart and good willed',  # dog, star
    'husband and wife',       # phoenix, pagoda
    'grand bets fulfilled', # dragon, jade
]
for line in poem:
    print(line)
    print(' '.join(str(char2num(x)) for x in line))
