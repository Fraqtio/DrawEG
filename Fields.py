import numpy as np
from PIL import Image


class ArtField:
    """
    x_size: int         Size of X field axis
    y_size: int         Size of Y field axis
    x0: int             Origin of X field axis
    y0: int             Origin of Y field axis
    field: np.array     Field container
    """

    def __init__(self, y: int = 1, x: int = 1, y0: int = 0, x0: int = 0):
        if y < 0 or x < 0:
            print('Field must have positive axis size value')
            raise Exception

        if y * x > 80000000:
            print('Too big field to construct')
            raise Exception

        self.x0 = x0
        self.y0 = y0
        self.x_size = x
        self.y_size = y
        self.field = np.zeros(shape=(self.y_size, self.x_size), dtype='uint16')

    def clear_field(self):
        self.field = np.zeros(shape=(self.y_size, self.x_size), dtype='uint16')

    def save_field(self, filename='draw.png'):
        self.field[self.field > 255] = 255
        self.field = np.array(self.field, dtype='uint8')
        Image.fromarray(255 - self.field[::-1], mode='L').save(filename)
        self.field = np.array(self.field, dtype='uint16')

    def __add__(self, other):
        self.field[max(other.y0, 0):max(other.field.shape[0]+other.y0, 0),
                   max(other.x0, 0):max(other.field.shape[1]+other.x0, 0)] += \
            other.field[max(-other.y0, 0):max(other.field.shape[0]-other.y0, other.field.shape[0]),
                        max(-other.x0, 0):max(other.field.shape[1]-other.x0, other.field.shape[1])]
        return self


class AnimatedField():
    """
    x_size: int         Size of X field axis
    y_size: int         Size of Y field axis
    x0: int             Origin of X field axis
    y0: int             Origin of Y field axis
    frames: int         Number of frames in out gif file
    field: np.array     Field container
    """

    def __init__(self,
                 y: int = 1,
                 x: int = 1,
                 y0: int = 0,
                 x0: int = 0,
                 frames: int = 30):
        if y < 0 or x < 0:
            print('Field must have positive axis size value')
            raise Exception

        if y * x > 80000000:
            print('Too big field to construct')
            raise Exception

        self.x0 = x0
        self.y0 = y0
        self.x_size = x
        self.y_size = y
        self.frames = frames
        self.field = np.zeros(shape=(self.frames, self.y_size, self.x_size), dtype='uint16')

    def save_field(self, filename='draw.gif'):
        self.field[self.field > 255] = 255
        self.field = np.array(self.field, dtype='uint8')
        last_frame = max(np.where(self.field != 0)[0])
        imgs = [Image.fromarray(255 - self.field[i, ::-1, :], mode='L') for i in range(last_frame + 1)]
        imgs[0].save(filename, save_all=True, append_images=imgs[1:], loop=0)
        self.field = np.array(self.field, dtype='uint16')

    def place_art(self, fld: ArtField, frame):
        self.field[frame, max(fld.y0 - self.y0, 0):max(fld.field.shape[0] + fld.y0 - self.y0, 0),
                   max(fld.x0 - self.x0, 0):max(fld.field.shape[1] + fld.x0 - self.x0, 0)] += \
            fld.field

    def __add__(self, other):
        self.field[:, max(other.y0, 0):max(other.field.shape[1]+other.y0, 0),
                   max(other.x0, 0):max(other.field.shape[2]+other.x0, 0)] += \
            other.field[:, max(-other.y0, 0):max(other.field.shape[1]-other.y0, other.field.shape[1]),
                        max(-other.x0, 0):max(other.field.shape[2]-other.x0, other.field.shape[2])]
        return self


class Number:
    """
    num: str            String interpretation of number
    fld: ArtField       Image container
    x0: int             Origin of X field axis
    y0: int             Origin of Y field axis
    """

    def __init__(self, number, y0=0, x0=0):

        self.fld = ArtField(x0=x0, y0=y0, y=5, x=len(number)*5-len(number)+1)

        for idx, num in enumerate(number):
            num_fld = ArtField(y=5, x=3, x0=idx*4)
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
