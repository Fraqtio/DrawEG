from math import sin, cos, pi, radians, sqrt, log2
from Fields import *
from Points import double_closed_pts

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

    def __init__(self,
                 points_list: list = (),
                 opacity: int = 100,
                 thick: int = 0,
                 name: str = 'lastfig',
                 closed=True):
        self.name = name
        self.points = points_list
        self.closed = closed
        self.thick = max(0, thick)
        self.opacity = max(0, opacity) if opacity < 100 else 100
        self.density = round(255 * self.opacity / 100)

        if len(self.points) == 0:
            print(f'Points list is empty in {self.name}')
            self.img_fld = ArtField()

        else:
            self.max_x = max([x for _, x in self.points])
            self.max_y = max([y for y, _ in self.points])
            self.min_x = min([x for _, x in self.points])
            self.min_y = min([y for y, _ in self.points])
            self.points = [(y - self.min_y, x - self.min_x) for y, x in self.points]
            self.dy = self.max_y - self.min_y
            self.dx = self.max_x - self.min_x
            self.img_fld = ArtField(x=self.dx + 2 * self.thick + 1, y=self.dy + 2 * self.thick + 1,
                                    x0=self.min_x - self.thick, y0=self.min_y - self.thick)
            self.draw_lines()

            if self.max_y < 0 and self.max_x < 0:
                print(f'Figure {self.name} is out of field bounds')

    def save_figure(self):
        self.img_fld.save_field(f'{self.name}.png')

    def get_figure(self):
        return self.img_fld

    def draw_dot(self, point):
        y0, x0 = point[0] + self.thick, point[1] + self.thick
        self.img_msk[y0, x0] = True
        if self.thick > 0:
            for x in range(self.thick + 1):
                y = (round(sqrt(self.thick ** 2 - x ** 2)))
                self.img_msk[y0 - y: y0 + y + 1, x0 + x] = True
                self.img_msk[y0 - y: y0 + y + 1, x0 - x] = True

    def draw_crest(self, point):
        y0, x0 = point[0] + self.thick, point[1] + self.thick
        if self.thick > 0:
            self.img_msk[y0 - self.thick: y0 + self.thick + 1, x0] = True
            self.img_msk[y0, x0 - self.thick: x0 + self.thick + 1] = True
        else:
            self.img_msk[y0, x0] = True

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
                 opacity: int = 100,
                 thick: int = 0,
                 corners: int = 4,
                 side_len: int = 10,
                 shift_degree: int = 0,
                 mode: str = 'xy0',
                 first_point: tuple = (0, 0),
                 name: str = 'lastfig'):

        if corners < 3 or side_len < 1:
            print(f"Can't create figure with those params in {self.name}")
            self.img_fld = ArtField()
            return

        rot_deg = round(360 / corners)
        radius_out = round(side_len / (2 * sin(pi / corners)))
        points_list = []

        if mode == 'xy0':
            point_list = []
            mid_y, mid_x = first_point[0] + radius_out, first_point[1] + radius_out
            x_list = []
            y_list = []
            for i in range(corners):
                point = (int(mid_y + radius_out * cos(radians(shift_degree + i * rot_deg))),
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
                point = (int(mid_y + radius_out * cos(radians(shift_degree + i * rot_deg))),
                         int(mid_x + radius_out * sin(radians(shift_degree + i * rot_deg))))
                points_list.append(point)

        elif mode == 'fp':
            mid_y = first_point[0] - round(radius_out * cos(radians(shift_degree)))
            mid_x = first_point[1] - round(radius_out * sin(radians(shift_degree)))
            points_list.append(first_point)
            for i in range(1, corners):
                point = (int(mid_y + radius_out * cos(radians(shift_degree + i * rot_deg))),
                         int(mid_x + radius_out * sin(radians(shift_degree + i * rot_deg))))
                points_list.append(point)

        else:
            print(f'Invalid "mode" parameter in {self.name}')
            self.img_fld = ArtField()
            return

        super().__init__(points_list=points_list, opacity=opacity, thick=thick, name=name)


class Funfig(Figure):
    """
    Figure that created by math function f(x).
    f:              Function Y by X, y = x by default
    x_range: tuple  Range of visualization by X axis, a tuple of int, necessary option
    Y_range: tuple  Range of visualization by Y axis, a tuple of int, unnecessary option
    spec: bool      Is specification needs to visualization, False by default
    scaling: float  Scaling multiplicator in visualization, 1 by default
    x0: int         Origin of X field axis, used in figure placing on field, 0 by default
    y0: int         Origin of Y field axis, used in figure placing on field, 0 by default
    """

    def __init__(self,
                 f=lambda x: x,
                 y_range: tuple = (),
                 x_range: tuple = (0, 10),
                 scaling: float = 1,
                 spec: bool = False,
                 name: str = 'func',
                 thick: int = 0,
                 x0: int = 0,
                 y0: int = 0,
                 opacity: int = 100):

        if (len(x_range) != 2) or (type(x_range[0]) != int) or (type(x_range[1]) != int):
            print('Invalid format of x_range value')
            raise Exception

        if x_range[0] > x_range[1]:
            x_range = x_range[::-1]
        # Calculating figure points
        points_list = []

        for x in np.arange(x_range[0], x_range[1], 1/scaling):
            y = f(x)
            points_list.append((round(y*scaling), round(x*scaling)))

        super().__init__(points_list=points_list, closed=False, thick=thick, opacity=opacity, name=name)
        self.img_fld.y0, self.img_fld.x0 = y0, x0
        # Cutting figure by y_range and x_range
        if len(y_range) == 1:
            y_range = (y_range[0], y_range[0])

        if len(y_range) == 2:
            if y_range[1] < y_range[0]:
                y_range = y_range[::-1]
            y_range = (y_range[0]*scaling, y_range[1]*scaling)

            if y_range[1] < self.min_y or y_range[0] > self.max_y:
                self.img_fld = ArtField()
                print('Chosen y range out of function area')
                return

            # Cutting in range by Y axis
            cut_y_ind, cut_x_ind = np.where(self.img_fld.field != 0)
            self.y0 = max(y_range[0] - self.min_y, 0)
            self.y1 = min(max(y_range[1] - self.min_y, 0), max(cut_y_ind) - self.thick)
            self.img_fld.field = self.img_fld.field[self.y0:self.y1 + 1]
            # Cutting white poles by X axis
            self.x0 = min(cut_x_ind) + self.thick
            self.x1 = max(cut_x_ind) - self.thick
            self.img_fld.field = self.img_fld.field[:, self.x0:self.x1 + 1]

        elif len(y_range) == 0:
            cut_y_ind, cut_x_ind = np.where(self.img_fld.field != 0)
            self.y0 = min(cut_y_ind)
            self.y1 = max(cut_y_ind) - 2 * self.thick
            self.x0 = min(cut_x_ind)
            self.x1 = max(cut_x_ind) - 2 * self.thick

        else:
            print(f'Invalid y_range format in {self.name}')
            self.img_fld = ArtField()
            return

        if spec:
            num_len = 4
            num_hei = 5
            inside_indent = 4
            spec_opacity = 1
            notch_len = 3
            self.y0 += self.min_y
            self.y1 += self.min_y
            self.x0 += self.min_x
            self.x1 += self.min_x
            num_len_y0 = len(str(round(self.y0 / scaling)))
            num_len_y1 = len(str(round(self.y1 / scaling)))
            max_y_len = max(num_len_y0, num_len_y1)
            num_len_x0 = len(str(round(self.x0 / scaling)))
            num_len_x1 = len(str(round(self.x1 / scaling)))
            max_x_len = max(num_len_x0, num_len_x1) * num_len
            # x indent for X axis line from bottom of fld
            outside_x_indent = num_hei + notch_len + 1
            # y indent for Y axis line from left of fld
            outside_y_indent = max_y_len * num_len + notch_len
            total_x_indent = inside_indent + spec_opacity + outside_x_indent
            total_y_indent = inside_indent + spec_opacity + outside_y_indent
            # Expanding field
            tmp = np.zeros(shape=(total_x_indent + outside_x_indent + self.img_fld.field.shape[0],
                                  total_y_indent + outside_y_indent + self.img_fld.field.shape[1] + max_x_len * 2),
                           dtype='uint16')
            tmp[total_x_indent:- outside_x_indent,
                total_y_indent + max_x_len:-outside_y_indent - max_x_len] = self.img_fld.field
            self.img_fld.field = tmp
            # Draw specification axis lines
            self.img_fld.field[outside_x_indent:, outside_y_indent] = 255
            self.img_fld.field[outside_x_indent, outside_y_indent:] = 255
            # Adding notches on axis lines by X axis
            dx = self.x1 - self.x0
            self.img_fld.field[outside_x_indent - notch_len:outside_x_indent,
                               total_y_indent + max_x_len + self.thick] = 255
            self.img_fld.field[outside_x_indent - notch_len:outside_x_indent,
                               total_y_indent + max_x_len + self.thick + dx] = 255
            # Drawn numbers that too close to each other
            if dx < max_x_len and dx != 0:
                num_art = Number(number=str(round(self.x0/scaling)), x0=total_y_indent + self.thick)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.x1/scaling)), x0=total_y_indent + self.thick + max_x_len + dx)
                self.img_fld += num_art.get_numbers()
            # Drawn numbers with normal split
            else:
                num_art = Number(number=str(round(self.x0/scaling)),
                                 x0=total_y_indent - int(num_len_x0 * num_len / 2) + max_x_len + self.thick)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.x1/scaling)),
                                 x0=total_y_indent - int(num_len_x1 * num_len / 2) + max_x_len + self.thick + dx)
                self.img_fld += num_art.get_numbers()
                step = 20 * max(1, round(max_x_len / num_len) - 3)
                start_num = self.x0 + (abs(self.x0) % step) + step
                stop_num = self.x1 - (abs(self.x1) % step) + 1

                for num in range(start_num, stop_num, step):
                    self.img_fld.field[outside_x_indent - notch_len:outside_x_indent,
                                       total_y_indent + num + max_x_len - self.x0 + self.thick] = 255
                    num_art = Number(number=str(round(num/scaling)),
                                     x0=total_y_indent-int((len(str(num))*num_len)/2)+num-self.x0+max_x_len+self.thick)
                    self.img_fld += num_art.get_numbers()
            # Adding notches on axis lines by Y axis
            dy = self.y1 - self.y0
            self.img_fld.field[total_x_indent + self.thick, outside_y_indent - notch_len: outside_y_indent] = 255
            self.img_fld.field[total_x_indent + self.thick + dy, outside_y_indent - notch_len: outside_y_indent] = 255
            # Drawn numbers that too close to each other
            if dy < num_hei and dy != 0:
                num_art = Number(number=str(round(self.y0/scaling)),
                                 x0=outside_y_indent - notch_len - num_len_y0 * num_len,
                                 y0=total_x_indent - num_hei + self.thick)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.y1/scaling)),
                                 x0=outside_y_indent - notch_len - num_len_y1 * num_len,
                                 y0=total_x_indent + dy + self.thick)
                self.img_fld += num_art.get_numbers()
            # Drawn numbers with normal split
            else:
                num_art = Number(number=str(round(self.y0/scaling)),
                                 x0=outside_y_indent - notch_len - num_len_y0 * num_len,
                                 y0=total_x_indent - round(num_hei/2) + self.thick)
                self.img_fld += num_art.get_numbers()
                num_art = Number(number=str(round(self.y1/scaling)),
                                 x0=outside_y_indent - notch_len - num_len_y1 * num_len,
                                 y0=total_x_indent - round(num_hei/2) + dy + self.thick)
                self.img_fld += num_art.get_numbers()
                step = 20 * max(1, max_y_len - 3)
                start_num = self.y0 + (abs(self.y0) % step) + step
                stop_num = self.y1 - (abs(self.y1) % step) + 1

                for num in range(start_num, stop_num, step):
                    self.img_fld.field[total_x_indent + num - self.y0 + self.thick,
                                       outside_y_indent - notch_len:outside_y_indent] = 255
                    num_art = Number(number=str(round(num/scaling)),
                                     x0=outside_y_indent - notch_len - len(str(round(num/scaling))) * num_len,
                                     y0=total_x_indent + num - self.y0 - round(num_hei/2) + self.thick)
                    self.img_fld += num_art.get_numbers()


class TriangulatedField(Figure):
    """
    Field that separated by triangles
    side_len: int       Length of triangle side
    x: int              X axis field size
    y: int              Y axis field size
    """
    def __init__(self,
                 x: int = 1,
                 y: int = 1,
                 side_len: int = 1,
                 x0: int = 0,
                 y0: int = 0,
                 name='triangulated',
                 opacity: int = 100):
        if x < 1 or y < 1 or side_len < 1 or x < side_len or y < side_len:
            print('Wrong axis size format')
            return
        if abs(x0) > x or abs(y0) > y:
            print('Figure has been placed out of field bounds')
            return

        triangle_hei = sqrt(3) / 2 * side_len
        half_side = int(side_len / 2)
        self.trn = int(y // triangle_hei)

        self.left_side_pts = [(round(n * triangle_hei), round(half_side * ((n + 1) % 2)))
                              for n in range(self.trn + 1)]

        self.right_side_pts = [(round(n * triangle_hei), round(x - int(x % side_len) - half_side * ((n + 1) % 2)))
                               for n in range(self.trn + 1)]

        self.bottom_side_pts = [(0, round(half_side + side_len * n)) for n in range(x//side_len)]

        self.top_side_pts = [(round(y - y % triangle_hei), (half_side * ((self.trn + 1) % 2) + side_len * n))
                             for n in range(x // side_len + self.trn % 2)]

        super().__init__(name=name, opacity=opacity)
        self.img_fld = ArtField(x=round(x - x % side_len) + 1, y=round(y - y % triangle_hei) + 1, x0=x0, y0=y0)
        self.draw_lines()


    def draw_lines(self):
        self.img_msk = np.full(shape=self.img_fld.field.shape, fill_value=False, dtype='bool')
        # Draw horizontal lines
        for i in range(len(self.left_side_pts)):
            self.draw_line(self.left_side_pts[i], self.right_side_pts[i])
        # Draw y = kx lines
        first_diag_pts_top = self.left_side_pts[1:-1:2] + self.top_side_pts
        first_diag_pts_bot = self.bottom_side_pts + self.right_side_pts[1:-1:2]
        for i in range(len(first_diag_pts_bot)):
            self.draw_line(first_diag_pts_top[i], first_diag_pts_bot[i])
        # Draw y = -kx lines
        second_diag_pts_top = self.top_side_pts[self.trn % 2:] + self.right_side_pts[-2 - self.trn % 2:0:-2]
        second_diag_pts_bot = self.left_side_pts[-2 - self.trn % 2:0:-2] + self.bottom_side_pts
        for i in range(len(second_diag_pts_bot)):
            self.draw_line(second_diag_pts_bot[i], second_diag_pts_top[i])

        self.img_fld.field[self.img_msk == True] = self.density


class AniFig(Figure):
    """
    name: str           Figure name, used to filename in saving
    points: list        List of figure points (y, x)
    fig_img: np.array   Figure field container
    img_fld: ArtField   Figure field class
    opacity: int        Opacity of figure visualization
    density: float      Density of figure visualization
    thick: int          Thick of figure lines
    closed: bool        Is figure closed on not
    """
    def __init__(self,
                 points_list: list = (),
                 opacity: int = 100,
                 thick: int = 0,
                 name: str = 'anifig',
                 closed: bool = True,
                 loop_steps: int = 1,
                 frames: int = 30):

        if len(points_list) == 0:
            print(f'Points list is empty in {self.name}')
            self.img_fld = AnimatedField()
            return

        self.name = name
        self.thick = max(0, thick)
        self.max_x = max([x for _, x in points_list])
        self.max_y = max([y for y, _ in points_list])
        self.min_x = min([x for _, x in points_list])
        self.min_y = min([y for y, _ in points_list])
        self.dy = self.max_y - self.min_y
        self.dx = self.max_x - self.min_x
        self.ani_fld = AnimatedField(x=self.dx + 2 * self.thick + 1,
                                     y=self.dy + 2 * self.thick + 1,
                                     x0=self.min_x - self.thick,
                                     y0=self.min_y - self.thick,
                                     frames=frames)

        num_of_pts = len(points_list)
        if num_of_pts < frames:
            points_list = double_closed_pts(points_list, steps=(5 - int(log2(num_of_pts))), closed=closed)
            num_of_pts = len(points_list)

        step = num_of_pts * loop_steps / frames

        if step >= frames:
            super().__init__(points_list=self.points, opacity=opacity, thick=thick, closed=closed)
            for fr in range(frames):
                self.ani_fld.place_art(self.img_fld, fr)

        else:
            for fr in range(frames):
                if (step * (fr + 1)) % num_of_pts > (step * fr) % num_of_pts:
                    pts = points_list[round((step * fr) % num_of_pts): round((step * (fr + 1)) % num_of_pts) + 1]
                    super().__init__(points_list=pts, opacity=opacity, thick=thick, name=name, closed=False)
                    self.ani_fld.place_art(self.img_fld, fr)


                else:
                    if closed:
                        pts_head = points_list[round((step * fr) % num_of_pts):]
                        pts_tail = points_list[:round((step * (fr + 1)) % num_of_pts) + 1]
                        pts = pts_head + pts_tail
                        super().__init__(points_list=pts, opacity=opacity, thick=thick, name=name, closed=False)
                        self.ani_fld.place_art(self.img_fld, fr)

                    else:
                        pts_head = points_list[round((step * fr) % num_of_pts):]
                        super().__init__(points_list=pts_head, opacity=opacity, thick=thick, name=name, closed=False)
                        self.ani_fld.place_art(self.img_fld, fr)
                        pts_tail = points_list[:round((step * (fr + 1)) % num_of_pts) + 1]
                        super().__init__(points_list=pts_tail, opacity=opacity, thick=thick, name=name, closed=False)
                        self.ani_fld.place_art(self.img_fld, fr)

    def get_figure(self):
        return self.ani_fld

    def save_figure(self):
        self.ani_fld.save_field(f'{self.name}.gif')
