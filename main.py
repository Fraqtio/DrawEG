import numpy as np
from PIL import Image
from math import sin, cos, pi, radians, sqrt
import time


#TODO: dataclasses
class ArtField:
    """
    x_size: int         Size of X field axis
    y_size: int         Size of Y field axis
    x0: int             Origin of X field axis
    y0: int             Origin of Y field axis
    field: np.array     Field container
    """

    def __init__(self, y: int = 1, x: int = 1, y0: int = 0, x0: int = 0):
        self.x0 = x0
        self.y0 = y0
        self.x_size = x
        self.y_size = y
        self.field = np.zeros(shape=(self.y_size, self.x_size), dtype='uint16')

    def clear_field(self):
        self.field = np.zeros(shape=(self.y_size, self.x_size), dtype='uint16')

    def save_field(self, filename='draw.png'):
        self.field[self.field>255] = 255
        self.field = np.array(self.field, dtype='uint8')
        Image.fromarray(255 - self.field[::-1], mode='L').save(filename)
        self.field = np.array(self.field, dtype='uint16')

    def __add__(self, other):
        self.field[max(other.y0, 0):max(other.field.shape[0]+other.y0, 0),
                   max(other.x0, 0):max(other.field.shape[1]+other.x0, 0)] += \
            other.field[max(-other.y0, 0):max(other.field.shape[0]-other.y0, other.field.shape[0]),
                        max(-other.x0, 0):max(other.field.shape[1]-other.x0, other.field.shape[1])]
        return self


class Figure:
    """
    name: str           Figure name, used to filename in saving
    points: list        List of figure points (y, x)
    fig_img: np.array   Figure field container
    img_fld: ArtField   Figure field class
    opacity: int        Opacity of figure visualization
    min_x: int          Min X value of figure
    min_y: int          Min Y value of figure
    max_x: int          Max X value of figure
    max_y: int          Max Y value of figure
    density: float      Density of figure visualization
    thick: int          Thick of figure lines
    closed: bool        Is figure closed on not
    """

    def __init__(self, points_list, opacity=100, thick=0, name='lastfig', closed=True):
        self.name = name
        self.points = points_list
        self.closed = closed
        self.thick = max(0, thick)
        self.opacity = max(0, opacity) if opacity < 100 else 100
        self.density = round(255 * self.opacity / 100)
        if len(self.points) == 0:
            raise Exception
        self.min_x = min([x for _, x in self.points])
        self.min_y = min([y for y, _ in self.points])
        self.max_x = max([x for _, x in self.points])
        self.max_y = max([y for y, _ in self.points])
        if self.max_y > 0 and self.max_x > 0:
            self.dy = self.max_y - self.min_y
            self.dx = self.max_x - self.min_x
            self.img_fld = ArtField(x=self.dx + 2 * self.thick + 1, y=self.dy + 2 * self.thick + 1,
                                    x0=self.min_x, y0=self.min_y)
            self.draw_lines()
        else:
            print(f'Figure {self.name} is out of field bounds')
            self.img_fld = ArtField()

    def save_figure(self):
        self.img_fld.save_field(f'{self.name}.png')

    def get_figure(self):
        return self.img_fld

    def draw_dot(self, point):
        y0, x0 = point[0] - self.min_y + self.thick, point[1] - self.min_x + self.thick
        self.img_msk[y0, x0] = True
        if self.thick > 0:
            for x in range(self.thick+1):
                for y in range(round(sqrt(self.thick ** 2 - x ** 2))+1):
                    self.img_msk[y0 + y, x0 + x] = True
                    self.img_msk[y0 - y, x0 + x] = True
                    self.img_msk[y0 + y, x0 - x] = True
                    self.img_msk[y0 - y, x0 - x] = True

    def draw_crest(self, point):
        y0, x0 = point[0] - self.min_y + self.thick, point[1] - self.min_x + self.thick
        self.img_msk[y0, x0] = True
        if self.thick > 0:
            self.img_msk[y0 - self.thick: y0 + self.thick + 1, x0] = True
            self.img_msk[y0, x0 - self.thick: x0 + self.thick + 1] = True

    def draw_lines(self):
        self.img_msk = np.full(shape=self.img_fld.field.shape, fill_value=False, dtype='bool')
        if len(self.points) > 2:
            if self.closed:
                for i in range(len(self.points)):
                    self.draw_line(self.points[i-1], self.points[i])
            else:
                for i in range(len(self.points)-1):
                    self.draw_line(self.points[i], self.points[i+1])
        elif len(self.points) == 2:
            self.draw_line(self.points[0], self.points[1])
        else:
            self.draw_dot(self.points[0])
        self.img_fld.field[self.img_msk == True] = self.density

    def draw_line(self, point0, point1):
        y0, x0 = point0
        self.draw_dot(point0)
        y1, x1 = point1
        self.draw_dot(point1)
        dx = x1 - x0
        dy = y1 - y0

        if (dx == 0) and (dy != 0):
            sdy = np.sign(dy)
            for _ in range(abs(dy)):
                self.draw_crest((y0, x0))
                y0 += sdy

        elif (dy == 0) and (dx != 0):
            sdx = np.sign(dx)
            for _ in range(abs(dx)):
                self.draw_crest((y0, x0))
                x0 += sdx

        elif (dy != 0) and (dx != 0):
            x_list = [x / abs(dx) for x in range(abs(dx), 0, -1)]
            y_list = [y / abs(dy) for y in range(abs(dy), 0, -1)]
            all_list = list(set(x_list + y_list))
            all_list.sort()
            sdy = np.sign(dy)
            sdx = np.sign(dx)

            for shift in all_list:
                if (shift in x_list) and (shift in y_list):
                    self.draw_crest((y0, x0))
                    x0 += sdx
                    y0 += sdy

                elif shift in x_list:
                    self.draw_crest((y0, x0))
                    x0 += sdx

                elif shift in y_list:
                    self.draw_crest((y0, x0))
                    y0 += sdy


class SimFigure(Figure):

    """
    corners: int        Number of figure corners
    side_len: int       Length of figure side
    shift_degree: int   Degree of figure turn around self center
    """

    def __init__(self,
                 opacity=100,
                 thick=0,
                 corners: int = 4,
                 side_len: int = 10,
                 shift_degree: int = 0,
                 mode: str = 'xy0',
                 first_point: tuple = (0, 0),
                 name='lastfig'):

        if corners < 3 or side_len < 1:
            raise Exception

        rot_deg = round(360 / corners)
        radius_out = round(side_len / (2 * sin(pi / corners)))
        points_list = []

        if mode == 'xy0':
            point_list = []
            mid_y, mid_x = first_point[0] + radius_out, first_point[1] + radius_out
            x_list = []
            y_list = []
            for i in range(corners):
                point = (int((mid_y + radius_out * cos(radians(shift_degree + i * rot_deg)))),
                         int(mid_x + radius_out * sin(radians(shift_degree + i * rot_deg))))
                point_list.append(point)
                y_list.append(point[0])
                x_list.append(point[1])
            dy = min(y_list) - first_point[0]
            dx = min(x_list) - first_point[1]
            for point in point_list:
                pnt = (point[0] - dy, point[1] - dx)
                points_list.append(pnt)

        elif mode == 'mid':
            mid_y, mid_x = first_point
            for i in range(corners):
                point = (int((mid_y + radius_out * cos(radians(shift_degree + i * rot_deg)))),
                         int(mid_x + radius_out * sin(radians(shift_degree + i * rot_deg))))
                points_list.append(point)

        elif mode == 'fp':
            mid_y = first_point[0] - round(radius_out * cos(radians(shift_degree)))
            mid_x = first_point[1] - round(radius_out * sin(radians(shift_degree)))
            points_list.append(first_point)
            for i in range(1, corners):
                point = (int((mid_y + radius_out * cos(radians(shift_degree + i * rot_deg)))),
                         int(mid_x + radius_out * sin(radians(shift_degree + i * rot_deg))))
                points_list.append(point)

        else:
            raise Exception

        super().__init__(points_list=points_list, opacity=opacity, thick=thick, name=name)


class Number():
    """
    num: str            String interpretation of number
    fld: ArtField       Image container
    x0: int             Origin of X field axis
    y0: int             Origin of Y field axis
    """

    def __init__(self, number, y0=0, x0=0):

        self.fld = ArtField(x0=x0, y0=y0, y=5, x=len(number)*5-len(number)+1)

        for idx, num in enumerate(number):
            num_fld = ArtField(y=5, x=3, y0=0, x0=idx*4)
            if num == '-':
                num_fld.field = np.array(([0, 0, 0],
                                          [0, 0, 0],
                                          [255, 255, 255],
                                          [0, 0, 0],
                                          [0, 0, 0]), dtype='uint8')
            elif num == '0':
                num_fld.field = np.array(([255, 255, 255],
                                          [255, 0, 255],
                                          [255, 0, 255],
                                          [255, 0, 255],
                                          [255, 255, 255]), dtype='uint8')
            elif num == '1':
                num_fld.field[::-1] = np.array(([0, 0, 255],
                                                [0, 255, 255],
                                                [0, 0, 255],
                                                [0, 0, 255],
                                                [0, 0, 255]), dtype='uint8')
            elif num == '2':
                num_fld.field[::-1] = np.array(([255, 255, 255],
                                                [0, 0, 255],
                                                [255, 255, 255],
                                                [255, 0, 0],
                                                [255, 255, 255]), dtype='uint8')
            elif num == '3':
                num_fld.field = np.array(([255, 255, 255],
                                          [0, 0, 255],
                                          [255, 255, 255],
                                          [0, 0, 255],
                                          [255, 255, 255]), dtype='uint8')
            elif num == '4':
                num_fld.field[::-1] = np.array(([255, 0, 255],
                                                [255, 0, 255],
                                                [255, 255, 255],
                                                [0, 0, 255],
                                                [0, 0, 255]), dtype='uint8')
            elif num == '5':
                num_fld.field[::-1] = np.array(([255, 255, 255],
                                                [255, 0, 0],
                                                [255, 255, 255],
                                                [0, 0, 255],
                                                [255, 255, 255]), dtype='uint8')
            elif num == '6':
                num_fld.field[::-1] = np.array(([255, 0, 0],
                                                [255, 0, 0],
                                                [255, 255, 255],
                                                [255, 0, 255],
                                                [255, 255, 255]), dtype='uint8')
            elif num == '7':
                num_fld.field[::-1] = np.array(([255, 255, 255],
                                                [0, 0, 255],
                                                [0, 0, 255],
                                                [0, 0, 255],
                                                [0, 0, 255]), dtype='uint8')
            elif num == '8':
                num_fld.field = np.array(([255, 255, 255],
                                          [255, 0, 255],
                                          [255, 255, 255],
                                          [255, 0, 255],
                                          [255, 255, 255]), dtype='uint8')
            elif num == '9':
                num_fld.field[::-1] = np.array(([255, 255, 255],
                                                [255, 0, 255],
                                                [255, 255, 255],
                                                [0, 0, 255],
                                                [0, 0, 255]), dtype='uint8')
            else:
                print('wrong number')
                raise Exception

            self.fld += num_fld

    def get_numbers(self):
        return self.fld


class Funfig(Figure):
    """
    f:              Function Y by X
    x_range: tuple  Range of visualization by X axis
    Y_range: tuple  Range of visualization by Y axis
    spec: bool      Is specification needs to visualization
    scaling: float  Scaling multiplicator in visualization
    x0: int         Origin of X field axis, used in figure placing on field
    y0: int         Origin of Y field axis, used in figure placing on field
    """
#TODO: finish scaling and choose optimize max Y and X ranges
    def __init__(self, f=lambda x: x, y_range=(), x_range=(0, 10), scaling=1, spec=False, name='func', x0=0, y0=0):
        point_list = []
        if (len(x_range) != 2) or (type(x_range[0]) != int) or (type(x_range[1]) != int):
            raise Exception
        if x_range[0] > x_range[1]:
            x_range = x_range[::-1]

        for x in range(x_range[0], x_range[1]+1):
            y = f(x)
            point_list.append((round(y*scaling), round(x*scaling)))

        self.y_shift = min([y[0] for y in point_list])
        self.x_shift = min([x[1] for x in point_list])
        points_list = [(y-self.y_shift, x-self.x_shift) for y, x in point_list]

        super().__init__(points_list=points_list, closed=False, name=name)

        self.img_fld.x0 = x0
        self.img_fld.y0 = y0

        if len(y_range) == 1:
            y_range = (y_range[0], y_range[0])

        if len(y_range) == 2:
            if y_range[1] < y_range[0]:
                y_range = y_range[::-1]
            y_range = (y_range[0]*scaling, y_range[1]*scaling)
            # Cutting in range by Y axis
            cut_y_ind = np.where(self.img_fld.field != 0)[0]
            self.y0 = max(y_range[0] - self.y_shift, 0)
            self.y1 = min(max(y_range[1] - self.y_shift, 0), max(cut_y_ind))
            self.img_fld.field = self.img_fld.field[self.y0:self.y1 + 1]
            # Cutting white poles by X axis
            cut_x_ind = np.where(self.img_fld.field != 0)[1]
            self.x0 = min(cut_x_ind)
            self.x1 = max(cut_x_ind)
            self.img_fld.field = self.img_fld.field[:, self.x0:self.x1+1]

        elif len(y_range) == 0:
            cut_y_ind = np.where(self.img_fld.field != 0)[0]
            self.y0 = min(cut_y_ind)
            self.y1 = max(cut_y_ind)
            cut_x_ind = np.where(self.img_fld.field != 0)[1]
            self.x0 = min(cut_x_ind)
            self.x1 = max(cut_x_ind)

        else:
            raise Exception

        if spec:
            num_len = 4
            num_hei = 5
            inside_indent = 4
            spec_opacity = 1
            notch_len = 3
            self.y0 += self.y_shift
            self.y1 += self.y_shift
            self.x0 += self.x_shift
            self.x1 += self.x_shift
            max_y_num = max(len(str(self.y0)), len(str(self.y1)))
            # x indent for X axis line from bottom of fld
            outside_x_indent = num_hei + notch_len + 1
            # y indent for Y axis line from left of fld
            outside_y_indent = max_y_num * num_len + notch_len
            total_x_indent = inside_indent + spec_opacity + outside_x_indent
            total_y_indent = inside_indent + spec_opacity + outside_y_indent
            # Expanding field
            x_spec = np.zeros(shape=(total_x_indent, self.img_fld.field.shape[1]), dtype='uint8')
            self.img_fld.field = np.row_stack((x_spec, self.img_fld.field))
            y_spec = np.zeros(shape=(self.img_fld.field.shape[0], total_y_indent), dtype='uint8')
            self.img_fld.field = np.column_stack((y_spec, self.img_fld.field))
            self.img_fld.field = np.row_stack((self.img_fld.field, np.zeros(shape=
                                                (outside_x_indent, self.img_fld.field.shape[1]), dtype='uint8')))
            self.img_fld.field = np.column_stack((self.img_fld.field, np.zeros(shape=
                                                (self.img_fld.field.shape[0], outside_y_indent), dtype='uint8')))
            # Draw specification axis lines
            self.points = [(outside_x_indent - notch_len, self.img_fld.field.shape[1] - 1 - notch_len),
                           (outside_x_indent, self.img_fld.field.shape[1] - 1),
                           (outside_x_indent, outside_y_indent),
                           (self.img_fld.field.shape[0] - 1, outside_y_indent),
                           (self.img_fld.field.shape[0] - 1 - notch_len, outside_y_indent - notch_len)]
            self.draw_lines()

            # Adding notches on axis lines
            num_len_x0 = len(str(self.x0))
            num_len_x1 = len(str(self.x1))
            dx = abs(self.x1 - self.x0)
            max_x_len = len(str(
                max(abs(round(self.x0/scaling)),
                    abs(round(self.x1/scaling)))))
            self.img_fld.field[outside_x_indent - notch_len:outside_x_indent, total_y_indent] = 255
            self.img_fld.field[outside_x_indent - notch_len:outside_x_indent, total_y_indent + dx] = 255

            if dx < max_x_len * num_len and dx != 0:
                num_art = Number(number=str(round(self.x0/scaling)),
                                 x0=total_y_indent - num_len_x0 * num_len)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.x1/scaling)),
                                 x0=total_y_indent + dx)
                self.img_fld += num_art.get_numbers()

            else:
                num_art = Number(number=str(round(self.x0/scaling)),
                                 x0=total_y_indent - int((num_len_x0 * num_len)/2))
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.x1/scaling)),
                                 x0=total_y_indent - int((num_len_x1 * num_len)/2) + dx)
                self.img_fld += num_art.get_numbers()
                step = 20 * max(1, max_x_len - 3)
                start = self.x0 + abs(self.x0)%step + step
                stop = self.x1 - abs(self.x1)%step - step + 1

                for num in range(start, stop, step):
                    self.img_fld.field[outside_x_indent - notch_len:outside_x_indent,
                                       total_y_indent + num - self.x0] = 255
                    num_art = Number(number=str(round(num/scaling)),
                                     x0=total_y_indent - int((len(str(num)) * num_len) / 2) + num - self.x0)
                    self.img_fld += num_art.get_numbers()

            dy = abs(self.y1 - self.y0)
            max_y_len = len(str(
                max(abs(round(self.y0/scaling)),
                    abs(round(self.y1/scaling)))))
            self.img_fld.field[total_x_indent, outside_y_indent - notch_len: outside_y_indent] = 255
            self.img_fld.field[total_x_indent + dy, outside_y_indent - notch_len: outside_y_indent] = 255

            if dy < num_hei and dy != 0:
                num_art = Number(number=str(round(self.y0/scaling)),
                                 y0=total_x_indent - num_hei)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.y1/scaling)),
                                 y0=total_x_indent + dy)
                self.img_fld += num_art.get_numbers()

            else:
                num_art = Number(number=str(round(self.y0/scaling)),
                                 y0=total_x_indent - round(num_hei/2))
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.y1/scaling)),
                                 y0=total_x_indent - round(num_hei/2) + dy)
                self.img_fld += num_art.get_numbers()
                step = 20 * max(1, max_y_len - 3)
                start = self.y0 + abs(self.y0) % step + step
                stop = self.y1 - abs(self.y1) % step - step + 1

                for num in range(start, stop, step):
                    self.img_fld.field[total_x_indent + num - self.y0,
                                       outside_y_indent - notch_len:outside_y_indent] = 255
                    num_art = Number(number=str(round(num/scaling)),
                                     y0=total_x_indent + num - self.y0 - round(num_hei/2))
                    self.img_fld += num_art.get_numbers()


def main():

    fld = ArtField(x=8000, y=8000)
    # triangle1 = Figure(opacity=50, points_list=[(-1000, -5000), (-10, -100)], thick=2, name='triangle1')
    # triangle1.save_figure()
    # triangle2 = Figure(opacity=70, points_list=[(40, 40)], thick=2, name='triangle2')
    # triangle2.save_figure()
    # triangle3 = SimFigure(mode='xy0', first_point=(0, 0), side_len=50, corners=9, thick=2, name='simfig')
    # triangle3.save_figure()
    # fld += triangle1.get_figure()
    # fld += triangle2.get_figure()
    # fld += triangle3.get_figure()
    y = lambda x: 2*sin(x)
    f = Funfig(f=y, x_range=(-200, 200), spec=True, scaling=10)
    f.save_figure()
    fld += f.get_figure()
    fld.save_field()


if __name__ == '__main__':
    start = time.time()
    main()
    end = time.time() - start
    print(end,'s')