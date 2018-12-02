from math import inf, ceil
from random import shuffle
from random import randint
from sympy import Point, Line, Ray, pi, Polygon
from Lab1.Convex_hull import convex_hull
from Lab1.DivideAndConquerConvexHull import rightmost_point_index, get_prev_index


def smallest_rectangle(p):
    ch = convex_hull(p)
    print(ch)
    # Find extreme points
    x_min_index = 0
    y_max_index = uppermost_point_index(ch)
    x_max_index = rightmost_point_index(ch)
    y_min_index = lowermost_point_index(ch)

    # Create vertical and horizontal Rays
    ray_1 = Ray(ch[x_min_index], angle=pi/2)
    ray_2 = Ray(ch[y_min_index], angle=0)
    ray_3 = Ray(ch[x_max_index], angle=pi/2)
    ray_4 = Ray(ch[y_max_index], angle=0)

    min_rectangle = Polygon((0, 0), (99999999, 0), (99999999, 99999999), (0, 99999999))


    for j in range(0, ceil(len(ch) / 4)):
        # Convert Rays to lines
        line_1 = Line(ray_1)
        line_2 = Line(ray_2)
        line_3 = Line(ray_3)
        line_4 = Line(ray_4)

        # Find the intersections of the lines
        p1 = line_1.intersection(line_2)[0]
        p2 = line_2.intersection(line_3)[0]
        p3 = line_3.intersection(line_4)[0]
        p4 = line_4.intersection(line_1)[0]
        current_rectangle = Polygon(p1, p2, p3, p4)

        # Calculate the area of the rectangle
        if current_rectangle.area < min_rectangle.area:
            min_rectangle = current_rectangle

        print(min_rectangle)
        print(min_rectangle.area)


        # Find the next Ray on the convex hull for each Ray in counter clockwise direction
        next_ray_1 = Ray(ch[x_min_index], ch[get_prev_index(ch, x_min_index)])
        next_ray_2 = Ray(ch[y_min_index], ch[get_prev_index(ch, y_min_index)])
        next_ray_3 = Ray(ch[x_max_index], ch[get_prev_index(ch, x_max_index)])
        next_ray_4 = Ray(ch[y_max_index], ch[get_prev_index(ch, y_max_index)])

        # Decrement the indecies
        """x_min_index = get_prev_index(ch, x_min_index)
        y_min_index = get_prev_index(ch, y_min_index)
        x_max_index = get_prev_index(ch, x_max_index)
        y_max_index = get_prev_index(ch, y_max_index)"""

        # Find the minimal angle to rotate each Ray until one aligns with the convex hull
        angle_1 = positive_angle(next_ray_1.closing_angle(ray_1))
        angle_2 = positive_angle(next_ray_2.closing_angle(ray_2))
        angle_3 = positive_angle(next_ray_3.closing_angle(ray_3))
        angle_4 = positive_angle(next_ray_4.closing_angle(ray_4))
        min_angle = min(angle_1, angle_2, angle_3, angle_4)

        # Find the minimal angle to rotate each Ray until one aligns with the convex hull
        """min_angle = min(
            positive_angle(next_ray_1.closing_angle(ray_1)),
            positive_angle(next_ray_2.closing_angle(ray_2)),
            positive_angle(next_ray_3.closing_angle(ray_3)),
            positive_angle(next_ray_4.closing_angle(ray_4)))
        print(min_angle)"""

        # Rotate all Rays around its origin with the angle calculated
        ray_1.rotate(min_angle)
        ray_2.rotate(min_angle)
        ray_3.rotate(min_angle)
        ray_4.rotate(min_angle)

        # Set the next point in the convex hull as the origin of the Ray that alligned
        # and decrement the index
        if min_angle == angle_1:
            ray_1 = Ray(next_ray_1.p2, angle=angle_1)
            x_min_index = get_prev_index(ch, x_min_index)
        elif min_angle == angle_2:
            ray_2 = Ray(next_ray_2.p2, angle=angle_2)
            y_min_index = get_prev_index(ch, y_min_index)
        elif min_angle == angle_3:
            ray_3 = Ray(next_ray_3.p2, angle=angle_3)
            x_max_index = get_prev_index(ch, x_max_index)
        elif min_angle == angle_4:
            ray_4 = Ray(next_ray_4.p2, angle=angle_4)
            y_max_index = get_prev_index(ch, y_max_index)

    return min_rectangle


def positive_angle(angle):
    if angle < 0:
        return 2 * pi + angle
    return angle


def uppermost_point_index(p):
    ump = - inf
    ump_index = 0
    for i in range(0, len(p)):
        if p[i][1] > ump:
            ump = p[i][1]
            ump_index = i
    return ump_index


def lowermost_point_index(p):
    lmp = - inf
    lmp_index = 0
    for i in range(0, len(p)):
        if p[i][1] < lmp:
            lmp = p[i][1]
            lmp_index = i
    return lmp_index


#list = [(1, 1), (2, 2), (2, 1), (3, 2), (3, 3), (3, 1), (1, 4)]
#r = smallest_rectangle(list)
#print(r)
#p = (1, 1)
#l1 = Line(p, slope=math.inf)
#print(l1.slope)
#print(Point(1, 1).x)
