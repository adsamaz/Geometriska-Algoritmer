import math
from random import shuffle
from random import randint


# Brute minidisk
def smallest_circle_brute(p):
    c_min = Circle2P((-math.inf, -math.inf), (math.inf, math.inf))
    for a in p:
        for b in p:
            if b == a:
                continue
            valid = True
            circle = Circle2P(a, b)
            for d in p:
                if d == a or d == b:
                    continue
                if not inside_circle(circle, d):
                    valid = False
                    break
            if valid and circle.diameter < c_min.diameter:
                c_min = circle
    for a in p:
        for b in p:
            if b == a:
                continue
            for c in p:
                if c == a or c == b:
                    continue
                valid = True
                circle = Circle3P(a, b, c)
                for d in p:
                    if d == a or d == b or d == c:
                        continue
                if not inside_circle(circle, d):
                    valid = False
                    break
            if valid and circle.diameter < c_min.diameter:
                c_min = circle
    return c_min


# Randomized minidisk
def smallest_circle_randomized(p):
    shuffle(p)
    disk = Circle2P(p[0], p[1])
    for i in range(2, len(p)):
        if not inside_circle(disk, p[i]):
            disk = mini_disk_with_point(p[0:i], p[i])
    return disk


def mini_disk_with_point(p, q):
    shuffle(p)
    disk = Circle2P(p[0], q)
    for i in range(1, len(p)):
        if not inside_circle(disk, p[i]):
            disk = mini_disk_with_2_points(p[0:i], p[i], q)
    return disk


def mini_disk_with_2_points(p, q1, q2):
    disk = Circle2P(q1, q2)
    for i in range(1, len(p)):
        if not inside_circle(disk, p[i]):
            disk = Circle3P(q1, q2, p[i])
    return disk


def inside_circle(circle, d):
    dist = math.sqrt((circle.midpoint[0] - d[0])**2 + (circle.midpoint[1] - d[1])**2)
    if dist <= circle.radius:
        return True
    else:
        return False


def mid_point(p1, p2):
    return (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2     # tuple


def distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


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
        self.midpoint = (math.inf, math.inf)
        x1, y1, x2, y2, x3, y3 = p1[0], p1[1], p2[0], p2[1], p3[0], p3[1]

        try:
            x = ((x1 ** 2 + y1 ** 2) * (y2 - y3) + (x2 ** 2 + y2 ** 2) * (y3 - y1) + (x3 ** 2 + y3 ** 2) * (y1 - y2)) / (
                        2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2))

            y = ((x1 ** 2 + y1 ** 2) * (x3 - x2) + (x2 ** 2 + y2 ** 2) * (x1 - x3) + (x3 ** 2 + y3 ** 2) * (x2 - x1)) / (
                        2 * (x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2))

            self.midpoint = (x, y)
            self.radius = distance(self.midpoint, p1)
            self.diameter = self.radius * 2
        except ZeroDivisionError:
            print("No circle could be made")


# TEST
l = []
for i in range(50):
    l.append((randint(200, 600), randint(100, 400)))

#cb = smallest_circle_brute([(1, 1), (1, 2), (2, 2), (2, 1), (3, 2), (2, 3), (3, 3), (3, 1), (1, 3)])
#cr = smallest_circle_randomized([(1, 1), (1, 2), (2, 2), (2, 1), (3, 2), (2, 3), (3, 3), (3, 1), (1, 3)])

cb = smallest_circle_brute(l)
cr = smallest_circle_randomized(l)

print("Brute:")
print(cb)
print(cb.radius)
print(cb.midpoint)
print(cb.p1 + cb.p2)

print("Randomized:")
print(cr)
print(cr.radius)
print(cr.midpoint)
print(cr.p1 + cr.p2)
