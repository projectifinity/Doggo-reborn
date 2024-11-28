import random

def random_line(fname):

    # finds out how many lines in txt file
    lines = open(fname).read().splitlines()

    while True:
        return random.choice(lines)