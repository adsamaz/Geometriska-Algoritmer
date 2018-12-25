import math

from sympy.core.tests.test_sympify import numpy
from Project.Generate_polygon import generate_polygon

class Triangle:

    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __repr__(self):
        return "Triangle: " + str(self.p1.p) + str(self.p2.p) + str(self.p3.p) + "\n"

class Node:

    def __init__(self, p):
        self.p = p
        self.x = p[0]
        self.y = p[1]
        self.triangles = []

    def __repr__(self):
        return "Node: " + str(self.p) + "\n"


def get_x(point):
    return point[0]


def ear_clip(points):
    triangles = []
    nodes = []
    for p in points:
        nodes.append(Node(p))
    old_nodes = nodes[:]
    for i in range(0, len(nodes) - 3):  # Number of triangles is n-2 so run the loop n-3 times (no need to triangulate last triangle)
        ear_index = find_ear(nodes)
        if ear_index is False:
            continue

        triangles.append(Triangle(nodes[ear_index - 1], nodes[ear_index], nodes[(ear_index + 1) % len(nodes)]))
        nodes.__delitem__(ear_index)
    return triangles



def find_ear(nodes):
    for i in range(0, len(nodes)):
        prev = nodes[i - 1]
        point = nodes[i]
        next = nodes[(i + 1) % len(nodes)]

        if is_convex(prev, point, next) and contains_no_points(prev, point, next, nodes):
            return i
    print("Error: No ears found")
    return False


def is_convex(prev, point, next):
    return prev.x * (next.y - point.y) + point.x * (prev.y - next.y) + next.x * (point.y - prev.y) >= 0


def contains_no_points(prev, point, next, nodes):
    for n in nodes:
        if right_turn([prev.p, point.p, n.p]) and right_turn([point.p, next.p, n.p]) and right_turn([next.p, prev.p, n.p]):
            return False
    return True

def right_turn(p):
    matrix = [[1, p[0][0], p[0][1]], [1, p[1][0], p[1][1]], [1, p[2][0], p[2][1]]]
    sign = numpy.linalg.det(matrix)
    if sign < 0:
        return True
    else:
        return False

# Testing
#points = [Node((574, 229)), Node((711, 487)), Node((555, 175)), Node((695, 88))]  #
#points = generate_polygon(8)
#print(find_ear(points))

#triangles = ear_clip(points)
#print(triangles)