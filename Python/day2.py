import sys
import collections

def sum(s):
    """Returns a list with the additions to 2xsum and 3xsum respectively"""
    d = collections.defaultdict(int)
    for c in s:
        d[c] += 1
    a = [0, 0]
    for k, v in d.items():
        if v == 2:
            a[0] = 1
        elif v == 3:
            a[1] = 1
    return a

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as f:
        totals = [0, 0]
        for line in f:
            twos, threes = sum(line.strip())
            totals[0] += twos
            totals[1] += threes
            print(totals)
        print("Final: {}".format(totals[1] * totals[0]))