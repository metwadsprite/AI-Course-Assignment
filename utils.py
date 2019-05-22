def is_on_segment(A, B, point):
    if B.x <= max(A.x, point.x) and B.x >= min(A.x, point.x) and \
        B.y <= max(A.y, point.y) and B.y >= min(A.y, point.y):
        return True
    return False


def orientation(A, B, C):
    """
    Given 3 points (A, B, C) the function returns:
    0 If the points are colinear
    1 If the points are clockwise
    2 If the points are counter-clockwise
    """
    value = (B.y - A.y) * (C.x - B.x) - (B.x - A.x) * (C.y - B.y)

    return 0 if value == 0 else 1 if value > 0 else 2


def is_intersect(A, B, C, D):
    if A.x == C.x and A.y == C.y:
        return False
    if A.x == D.x and A.y == D.y:
        return False
    if B.x == C.x and B.y == C.y:
        return False
    if B.x == D.x and B.y == D.y:
        return False

    orient1 = orientation(A, B, C)
    orient2 = orientation(A, B, D)
    orient3 = orientation(C, D, A)
    orient4 = orientation(C, D, B)

    if orient1 != orient2 and orient3 != orient4:
        return True

    if orient1 == 0 and is_on_segment(A, B, C):
        return True
    if orient2 == 0 and is_on_segment(A, B, D):
        return True
    if orient3 == 0 and is_on_segment(C, D, A):
        return True
    if orient4 == 0 and is_on_segment(C, D, B):
        return True

    return False