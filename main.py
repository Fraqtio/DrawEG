import time
from Fields import *
from Figures import *

def main():

    fld = ArtField(x=8000, y=8000)
    # triangle1 = Figure(opacity=50, points_list=[(250, 250), (0, 0), (-100, -150)], thick=10, name='triangle1')
    # triangle1.save_figure()
    # fld += triangle1.get_figure()
    # triangle2 = Figure(opacity=70, points_list=[(40, 40)], thick=2, name='triangle2')
    # triangle2.save_figure()
    # fld += triangle2.get_figure()
    # triangle3 = SimFigure(mode='xy0', first_point=(0, 0), side_len=50, corners=9, thick=2, name='simfig')
    # triangle3.save_figure()
    # fld += triangle3.get_figure()

    f = Funfig(f=lambda x: 10*sin(x),
               x_range=(-350, -360),
               spec=True,
               scaling=10,
               thick=100,
               name='ThickFunc')
    f.save_figure()
    fld += f.get_figure()
    # tr = TriangulatedField(x=1000, y=1000, side_len=30)
    # tr.save_figure()
    # fld += tr.get_figure()
    fld.save_field()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(f"Ends in {round(end, 3)} seconds")
