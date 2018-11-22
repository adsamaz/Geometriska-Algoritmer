import math


def smallest_circle_brute(p):
    c_min = Circle((0, 0), math.inf)

    for a in p:
        for b in p:
            if b == a:
                continue
            c = Circle(a, b)



def inside_circle_2P(a, b, d):
    diameter = math.abs(a[0] - b[0])



class Circle(object):
    def __init__(self, center, radius):
        self.center, self.radius = center, radius


smallest_circle_brute([])