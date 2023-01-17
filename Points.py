from math import sqrt


def circle_pts(r=1, x0=0, y0=0):
    pts_list_1 = []
    for x in range(1, r + 1):
        y = (round(sqrt(r ** 2 - x ** 2)))
        pts_list_1.append((y, x))
    pts_list_1 = pts_list_1[:round(r * sqrt(3) / 2)] + [(x, y) for y, x in pts_list_1[round(r / 2)::-1]]
    pts_list_4 = [(-y, x) for y, x in pts_list_1[::-1]]
    pts_list_3 = [(-y, -x) for y, x in pts_list_1]
    pts_list_2 = [(y, -x) for y, x in pts_list_1[::-1]]
    crl_pts = pts_list_1 + pts_list_4 + pts_list_3 + pts_list_2
    return [(y + y0, x + x0) for y, x in crl_pts]


def mid_pts(pts1, pts2):
    y0, x0 = pts1
    y1, x1 = pts2
    mid = (round((y0 + y1) / 2), round((x0 + x1) / 2))
    return mid


def double_pts(lst: list = (), steps: int = 1, closed: bool = True):
    if steps < 1:
        print('Invalid steps value')
        return lst

    if len(lst) == 0:
        print('Double_pts gave null list')
        return lst

    elif len(lst) == 1:
        result = lst * (2 ** steps)

    else:
        result = lst
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


def drop_n_lst(lst: list, n: int = 0):
    len_lst = len(lst)
    if n < 0 or len_lst < n:
        print('Wrong deleting number value')
        return
    # A little troubles with big float nums but working well in 100000 range
    trg_len = len_lst - n
    result = []
    i = 0
    sep = trg_len / len_lst / 2
    while trg_len > len(result):
        sep += trg_len / len_lst
        if sep > 1:
            sep -= 1
            result.append(lst[i])
        i += 1

    return result


def sqr_sort(pts: list):
    def ln(point1, point2):
        n = 0
        for i in range(3):
            if point1[i] == point2[i]:
                n += 1
        return n == 2

    if ln(pts[0], pts[1]) is False:
        pts[1], pts[2] = pts[2], pts[1]

    if ln(pts[2], pts[1]) is False:
        pts[3], pts[2] = pts[2], pts[3]



