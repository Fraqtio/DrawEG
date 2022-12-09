import time
from Figures import *
from Points import *


def main():

    fld = AnimatedField(x=1000, y=1000)
    anifig = AniFig(points_list=circle_pts(r=10, x0=100, y0=100), loop_steps=4)
    anifig.save_figure()
    fld += anifig.get_figure()
    fld.save_field()

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Ends in {round(end, 3)} seconds")
