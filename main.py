import time
from Figures import *
from Points import *

#TODO: net of the diff speed circles
def main():

    fld = AnimatedField(x=1000, y=1000, frames=30)
    anifig1 = AniFig(points_list=circle_pts(r=30, x0=100, y0=100),
                     loop_steps=1,
                     frames=30,
                     thick=2,
                     opacity=100,
                     tail=True)
    anifig1.save_figure()
    fld += anifig1.get_figure()
    # anifig2 = AniFig(points_list=circle_pts(r=30, x0=100, y0=103), loop_steps=1, frames=30, thick=0, opacity=50)
    #anifig2.save_figure()
    #fld += anifig2.get_figure()
    fld.save_field()

    # lst = [_ for _ in range(100000)]
    # lst = drop_n_lst(lst, n=1)

if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Done in {round(end, 3)} seconds")
