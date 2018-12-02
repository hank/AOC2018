import sys
import string
from profilehooks import timecall

def find_oneoff(inventory, b):
    for o in range(0, len(b)):
        # Try for each letter subbed at this position
        for c in string.ascii_lowercase:
            candidate = b
            candidate = candidate[0:o] + c + candidate[o+1:]
            if candidate in inventory:
                return b, candidate
    return None, None

@timecall
def main():
    inventory = set()
    with open(sys.argv[1], 'r') as f:
        for line in f:
            to_test = line.strip()
            first, second = find_oneoff(inventory, to_test)
            if first is not None:
                print("FOUND: {} {}".format(first, second))
                # Produce answer to submit
                final = ""
                for o in range(0, len(first)):
                    if first[o] != second[o]:
                        print("Changed character was: {} to {} at offset {}".format(first[o], second[o], o))
                    else:
                        final += first[o]
                print("Final answer: {}".format(final))
                sys.exit(0)
            inventory.add(to_test)

if __name__ == "__main__":
    main()