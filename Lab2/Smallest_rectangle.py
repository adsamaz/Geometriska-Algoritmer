import math
from random import shuffle
from random import randint
from sympy import Point, Line
from Lab1.Convex_hull import convex_hull
from Lab1.DivideAndConquerConvexHull import rightmost_point_index


def smallest_rectangle(p):
    ch = convex_hull(p)
    p_min_index = 0
    p_max_index = rightmost_point_index(ch)

    line_1 = Line(ch[p_min_index], slope=math.inf)
    line_2 = Line(ch[p_min_index], slope=0)
    line_3 = Line(ch[p_max_index], slope=math.inf)
    line_4 = Line(ch[p_max_index], slope=0)

    area_min = math.inf

    next = Line(ch[p_min_index], ch[p_min_index + 1])
    angle = line_1.angle_between(next)
    line_1 = Line(line_1.p1, slope=line_1.slope + angle)
    print(line_1.slope)
    print(ch)
    print(angle)




list = [(1, 1), (2, 2), (2, 1), (3, 2), (3, 3), (3, 1)]
smallest_rectangle(list)

#p = (1, 1)
#l1 = Line(p, slope=math.inf)
#print(l1.slope)
#print(Point(1, 1).x)
