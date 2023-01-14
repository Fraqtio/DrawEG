import time
from Figures import *


def main():

    TheCube(ln=500, frames=5000)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Done in {round(end, 3)} seconds")
