from math import sqrt


def circle_pts(r=1, x0=0, y0=0):
    pts_list_1 = []
    for x in range(r + 1):
        y = (round(sqrt(r ** 2 - x ** 2)))
        pts_list_1.append((y, x))
    pts_list_1 = pts_list_1[:round(r*sqrt(3)/2)] + [(x, y) for y, x in pts_list_1[round(r/2)::-1]]
    pts_list_4 = [(-y, x) for y, x in pts_list_1[::-1]]
    pts_list_3 = [(-y, -x) for y, x in pts_list_1]
    pts_list_2 = [(y, -x) for y, x in pts_list_1[::-1]]
    circle_pts = pts_list_1 + pts_list_4 + pts_list_3 + pts_list_2

    return [(y + y0, x + x0) for y, x in circle_pts]


def mid_pts(pts1, pts2):
    y0, x0 = pts1
    y1, x1 = pts2
    mid = (round((y0 + y1) / 2), round((x0 + x1) / 2))
    return mid

def double_closed_pts(list: list = (), steps: int = 1, closed: bool = True):
    result = list
    for _ in range(max(steps, 0)):
        tmp_list = []

        for i in range(len(result) - 1):
            tmp_list.append(result[i])
            tmp_list.append(mid_pts(result[i], result[i + 1]))

        tmp_list.append(result[-1])
        if closed:
            tmp_list.append(mid_pts(result[-1], result[0]))
        result = tmp_list
    return result

