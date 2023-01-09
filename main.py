import time
from Figures import *
from Points import *


def main():
    print('Hello, world!')

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Done in {round(end, 3)} seconds")
