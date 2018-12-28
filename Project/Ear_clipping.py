import math

from sympy.core.tests.test_sympify import numpy
from Project.Generate_polygon import generate_polygon

class Triangle:

    def __init__(self, p1, p2, p3):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.visited = False
        self.neighbours_visited = 0

    def visited_all_neighbours(self):
        nodes = self.get_nodes()
        visited_triangles = []
        for n in nodes:
            for t in n.triangles:
                if self.find_common_diagonal(t) and not t.visited and t not in visited_triangles:
                    visited_triangles.append(t)

        return self.neighbours_visited == len(visited_triangles)

    def find_common_diagonal(self, t2):
        diagonal = []
        for n in self.get_nodes():
            if n in t2.get_nodes():
                diagonal.append(n)
        if len(diagonal) == 2:
            return diagonal
        return False

    def get_nodes(self):
        return [self.p1, self.p2, self.p3]

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


def ear_clip(points):
    triangles = []
    nodes = []
    for p in points:
        nodes.append(Node(p))
    #old_nodes = nodes[:]
    for i in range(0, len(nodes) - 2):  # Number of triangles is n-2 so run the loop n-3 times (no need to triangulate last triangle)
        ear_index = find_ear(nodes)
        if ear_index is False:
            continue
        triangle = Triangle(nodes[ear_index - 1], nodes[ear_index], nodes[(ear_index + 1) % len(nodes)])
        add_triangle_to_nodes(triangle, nodes[ear_index - 1], nodes[ear_index], nodes[(ear_index + 1) % len(nodes)])
        triangles.append(triangle)
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
        if point_inside_polygon(n.p, [prev, point, next]):
            return False
    return True

def point_inside_polygon(p, polygon):
    for i in range(0, len(polygon)):
        if right_turn([polygon[i].p, polygon[(i+1) % len(polygon)].p, p]):
            continue
        else:
            return False
    return True

def right_turn(p):
    matrix = [[1, p[0][0], p[0][1]], [1, p[1][0], p[1][1]], [1, p[2][0], p[2][1]]]
    sign = numpy.linalg.det(matrix)
    if sign < 0:
        return True
    else:
        return False

def add_triangle_to_nodes(triangle, n1, n2, n3):
    n1.triangles.append(triangle)
    n2.triangles.append(triangle)
    n3.triangles.append(triangle)

# Testing
#points = [Node((574, 229)), Node((711, 487)), Node((555, 175)), Node((695, 88))]  #
#points = generate_polygon(8)
#print(find_ear(points))

#triangles = ear_clip(points)
#print(triangles)