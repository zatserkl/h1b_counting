import sys


class H1B_counting:
    def __init__(self):
        print('Hello')


if __name__ == '__main__':
    for iarg, item in enumerate(sys.argv):
        print(iarg, item)

h1b_counting = H1B_counting()
