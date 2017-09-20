import sys

def char2num(char):
    assert len(char) == 1
    return ord(char.lower()) - ord('a') + 1

def summod(nums):
    return ((sum(nums) - 1) % 26) + 1

def num2char(num):
    return chr(ord('a') + num - 1)

res = sys.argv[1]
nums = [char2num(char) for char in res]
print(num2char(summod(nums)))
