from collections import Counter
import os
import sys


INPUT_FILE = r'book.gam'

def createOpeningsDict():

    if not os.path.isfile(INPUT_FILE):
        print('Could not find file')
        sys.exit(1)
    d = Counter()

    with open (INPUT_FILE, 'r') as fh:

        for line in fh.readlines():
            line = line[:30]
            d.update([line])

    return d.most_common(70)


d = createOpeningsDict()
