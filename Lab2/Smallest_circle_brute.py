import math
from Lab1.Convex_hull import left_turn


def smallest_circle_brute(p):
    c_min = Circle2P((-math.inf, -math.inf), (math.inf, math.inf))
    for a in p:
        for b in p:
            valid = True
            if b == a:
                continue
            circle = Circle2P(a, b)
            for d in p:
                if d == a or d == b:
                    continue
                if not inside_circle_2p(circle, d):
                    valid = False
                    break
            print("Circle2P: " + str(circle.midpoint) + str(circle.radius))
            if valid and circle.diameter < c_min.diameter:
                c_min = circle

    for a in p:
        for b in p:
            if b == a:
                continue
            for c in p:
                if c == a or c == b:
                    valid = True
                    continue
                circle = Circle3P(a, b, c)
                for d in p:
                    if d == a or d == b or d == c:
                        continue
                if not inside_circle_3p(circle, d):
                    valid = False
                    break
            print("Circle3P: " + str(circle.radius))
            if valid and circle.diameter < c_min.diameter:
                c_min = circle
    return c_min


def mid_point(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2     # tuple


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def inside_circle_2p(circle, d):
    distance = math.sqrt((circle.midpoint[0] - d[0])**2 + (circle.midpoint[1] - d[1])**2)
    if distance <= circle.radius:
        return True
    else:
        return False

def sort_clockwise(p1, p2, p3):
    p = [p1, p2, p3]
    if left_turn(p):
        return p1, p3, p2
    return p1, p2, p3


def inside_circle_3p(circle, d):
    p1, p2, p3 = sort_clockwise(circle.p1, circle.p2, circle.p3)
    adx = p1[0] - d[0]
    ady = p1[1] - d[1]
    bdx = p2[0] - d[0]
    bdy = p2[1] - d[1]
    cdx = p3[0] - d[0]
    cdy = p3[1] - d[1]

    abdet = adx * bdy - bdx * ady
    bcdet = bdx * cdy - cdx * bdy
    cadet = cdx * ady - adx * cdy
    alift = adx * adx + ady * ady
    blift = bdx * bdx + bdy * bdy
    clift = cdx * cdx + cdy * cdy

    sign = alift * bcdet + blift * cadet + clift * abdet
    if sign >= 0:
        return True
    else:
        return False


class Circle2P(object):
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.diameter = distance(p1, p2)
        self.radius = self.diameter / 2
        self.midpoint = mid_point(p1, p2)


class Circle3P(object):
    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.diameter = math.inf
        self.radius = math.inf
        x1, y1, x2, y2, x3, y3 = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]

        """A = x2 - x1
        B = y2 - y1
        C = x3 - x1
        D = y3 - y1
        E = A * (x1 + x2) + B * (y1 + y2)
        F = C * (x1 + x3) + D * (y1 + y3)
        G = 2 * (A * (y3 - y2) - B * (x3 - x2))
        if G == 0:
            self.radius = 0
        x = (D * E - B * F) / G
        y = (A * F - C * E) / G"""
        try:
            ma = (y2-y1)/(x2-x1)
            mb = (y3-y2)/(x3-x2)
            x = (ma*mb*(y1-y3) + mb*(x1+x2) - ma*(x2+x3))/(2*(mb-ma))
            if not ma == 0:
                y = (-1/ma)*(x-(x1+x2)/2)+(y1+y2)/2
            else:
                y = (-1/mb)*(x-(x2+x3)/2)+(y2+y3)/2

            self.radius = math.sqrt((x - x1) * (x - x1) + (y - y1) * (y - y1))
            self.diameter = self.radius * 2
        except ZeroDivisionError:
            print("No circle could be made")


c = smallest_circle_brute([(1, 1), (1, 2), (2, 2), (2, 1), (4, 1), (3, 7), (10, 10)])
# c = Circle3P((1, 1), (2, 2), (1, 2))
print(c)
print(c.radius)
#print(c.midpoint)
