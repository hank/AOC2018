import sys
from pprint import PrettyPrinter

def react(inp):
    # Find adjacent pairs, react, return result
    kabooming = True
    while kabooming:
        i = 0
        kabooming = False
        # print(inp)
        while i < len(inp)-1:
            if inp[i] == chr(ord(inp[i+1]) ^ 0x20):
                # print("{} !! {}".format(inp[i], inp[i+1]))
                # Kaboom
                inp = inp[:i] + inp[i+2:]
                # print(inp)
                kabooming = True
            else:
                i += 1
    return inp


if __name__ == "__main__":
    pp = PrettyPrinter()
    with open(sys.argv[1], 'r') as f:
        inp = f.read()
        # outp = react("dabAcCaCBAcCcaDA")
        outp = react(inp.strip())
        print(len(outp))