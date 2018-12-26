from Project.Ear_clipping import *


def shortest_path(p, q, polygon, triangles):
    triangle_p = None
    triangle_q = None

    for t in triangles:                 #Find the triagles the two points lie inside of
        if point_inside_polygon(p, t.get_nodes()):
            triangle_p = t
        if point_inside_polygon(q, t.get_nodes()):
            triangle_q = t
    if triangle_p == triangle_q:        #If both points are inside the same triangle -> Done
        return [Node(p), Node(q)]



