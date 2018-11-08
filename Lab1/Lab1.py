
import numpy


def convex_hull(p):
    p = sort_points(p)

    l_upper = [p[0], p[1]]      # add the first 2 points
    for i in range(2, len(p)):
        l_upper.append(p[i])
        while len(l_upper) > 2 and not right_turn(l_upper[len(l_upper)-3:len(l_upper)]):
            del l_upper[len(l_upper)-2]

    l_lower = [p[len(p)-1], p[len(p)-2]]  # add the last 2 points
    for i in reversed(range(0, len(p) - 2)):
        l_lower.append(p[i])
        while len(l_lower) > 2 and not right_turn(l_lower[len(l_lower)-3:len(l_lower)]):
            del l_lower[len(l_lower)-2]

    del l_lower[0]
    del l_lower[-1]
    return l_upper + l_lower


def right_turn(p):
    matrix = [[1, p[0][0], p[0][1]], [1, p[1][0], p[1][1]], [1, p[2][0], p[2][1]]]
    sign = numpy.linalg.det(matrix)
    if sign > 0:
        return False
    else:
        return True


# Sortera i x-led
def sort_points(p):
    p.sort()
    return p
