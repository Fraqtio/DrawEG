from Figures import Figure
import numpy as np
from math import sqrt
from Fields import ArtField


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
