import numpy as np
from PIL import Image
from math import sin, cos, pi, radians, sqrt


class ArtField:

    __x_size: int
    __y_size: int
    __x0: int
    __y0: int
    field: np.array

    def __init__(self, y: int = 8192, x: int = 8192, y0: int = 0, x0: int = 0):
        self.__x0 = x0
        self.__y0 = y0
        self.__x_size = x
        self.__y_size = y
        self.field = np.zeros(shape=(self.__y_size, self.__x_size), dtype='uint8')

    def clear_field(self):
        self.field = np.zeros(shape=(self.__y_size, self.__x_size), dtype='uint8')

    def save_field(self, filename='draw.png'):
        Image.fromarray(255 - self.field, mode='L').save(filename)

    def __add__(self, other):
        y_shape = other.field.shape[0]
        x_shape = other.field.shape[1]
        y1, x1 = y_shape + other.__y0, x_shape + other.__x0
        buf_fig = np.zeros(shape=(
            3 * self.field.shape[0] - 2,
            3 * self.field.shape[1] - 2),
            dtype='uint16')
        buf_fig[y1: y1 + y_shape, x1: x1 + x_shape] += other.field
        tmp = buf_fig[y_shape: self.field.shape[0] + y_shape,
                      x_shape: self.field.shape[1] + x_shape]
        tmp += self.field
        tmp[tmp > 255] = 255
        self.field = np.array(tmp, dtype='uint8')

        return self


class Figure:

    __points: list
    __fig_img: np.array
    __img_fld: ArtField
    __opacity: int
    __min_x: int
    __min_y: int
    __max_x: int
    __max_y: int
    __density: float
    __thick: int

    def __init__(self, points_list, opacity=100, thick=0, name='lastfig'):
        self.name = name
        self.__points = points_list
        self.__thick = max(0, thick)
        self.__opacity = max(0, opacity) if opacity < 100 else 100
        self.__density = round(255 * self.__opacity / 100)
        if len(self.__points) == 0:
            raise Exception
        self.__min_x = min([x for _, x in self.__points])
        self.__min_y = min([y for y, _ in self.__points])
        self.__max_x = max([x for _, x in self.__points])
        self.__max_y = max([y for y, _ in self.__points])
        dy = self.__max_y - self.__min_y
        dx = self.__max_x - self.__min_x
        self.__img_fld = ArtField(x=dx + 2 * self.__thick + 1, y=dy + 2 * self.__thick + 1,
                                  x0=self.__min_x, y0=self.__min_y)
        self.__fig_img = self.__img_fld.field
        self.__img_msk = np.full(shape=(dy + 2 * self.__thick + 1, dx + 2 * self.__thick + 1),
                                 fill_value=False, dtype='bool')
        self.draw_lines()
        self.__img_fld.save_field(f'{self.name}.png')

    def get_figure(self):
        return self.__img_fld

    def draw_dot(self, point):
        y0, x0 = point[0] - self.__min_y + self.__thick, point[1] - self.__min_x + self.__thick
        self.__img_msk[y0, x0] = True
        if self.__thick > 0:
            for x in range(self.__thick+1):
                for y in range(round(sqrt(self.__thick ** 2 - x ** 2))+1):
                    self.__img_msk[y0 + y, x0 + x] = True
                    self.__img_msk[y0 - y, x0 + x] = True
                    self.__img_msk[y0 + y, x0 - x] = True
                    self.__img_msk[y0 - y, x0 - x] = True

    def draw_lines(self):
        if len(self.__points) > 2:
            for i in range(len(self.__points)):
                self.draw_line(self.__points[i-1], self.__points[i])
        elif len(self.__points) == 2:
            self.draw_line(self.__points[0], self.__points[1])
        else:
            self.draw_dot(self.__points[0])
        self.__fig_img[self.__img_msk == True] = self.__density

    def draw_line(self, point0, point1):
        y0, x0 = point0
        y1, x1 = point1
        dx = x1 - (x0)
        dy = y1 - (y0)

        if (dx == 0) and (dy != 0):
            sdy = int(dy / abs(dy))
            for _ in range(abs(dy)+1):
                self.draw_dot((y0, x0))
                y0 += sdy

        elif (dy == 0) and (dx != 0):
            sdx = int(dx / abs(dx))
            for _ in range(abs(dx)+1):
                self.draw_dot((y0, x0))
                x0 += sdx

        elif (dy == 0) and (dx == 0):
            self.draw_dot((y0, x0))

        else:
            x_list, y_list = [x / abs(dx) for x in range(abs(dx)+1, 0, -1)], \
                             [y / abs(dy) for y in range(abs(dy)+1, 0, -1)]
            all_list = list(set(x_list + y_list))
            all_list.sort()
            sdy = int(dy / abs(dy))
            sdx = int(dx / abs(dx))
            for shift in all_list:
                if (shift in x_list) and (shift in y_list):
                    self.draw_dot((y0, x0))
                    x0 += sdx
                    y0 += sdy

                elif shift in x_list:
                    self.draw_dot((y0, x0))
                    x0 += sdx

                elif shift in y_list:
                    self.draw_dot((y0, x0))
                    y0 += sdy


class SimFigure(Figure):

    __corners: int
    __side_len: int
    __shift_degree: int

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


class FunFig(Figure):

    def __init__(self, f=1, y_range=(0, 1), x_range=(0, 1)):
        for x in range(*x_range):
            print(x)


def main():
    fld = ArtField()
    triangle1 = Figure(opacity=50, points_list=[(10, 50), (10, 100)], thick=2, name='triangle1')
    triangle2 = Figure(opacity=70, points_list=[(40, 40)], thick=2, name='triangle2')
    triangle3 = SimFigure(mode='xy0', first_point=(0, 0), side_len=50, corners=9, thick=2, name='simfig')
    fld += triangle1.get_figure()
    fld += triangle2.get_figure()
    fld += triangle3.get_figure()
    fld.save_field()


if __name__ == '__main__':
    main()
