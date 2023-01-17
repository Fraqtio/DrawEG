import time
from Figures import *


def main():

    TheCube(ln=200, frames=600)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Done in {round(end, 3)} seconds")
