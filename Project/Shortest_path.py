from Project.Ear_clipping import *


def shortest_path(p, q, polygon, triangles):
    triangle_p = None
    triangle_q = None

    for t in triangles:                 #Find the triagles the two points lie inside of
        print(t.get_nodes())
        if point_inside_polygon(p, t.get_nodes()):
            triangle_p = t
        if point_inside_polygon(q, t.get_nodes()):
            triangle_q = t
    if triangle_p == triangle_q:        #If both points are inside the same triangle -> Done
        return [Node(p), Node(q)]

    triangle_p.visited = True
    current_triangle = triangle_p
    diagonals = []
    done = False
    triangles_traversed = 0
    prev_triangle = None
    potential_triangles = []
    while not done:
        print(triangles_traversed)
        #print(potential_triangles)
        if prev_triangle == current_triangle:
            current_triangle = potential_triangles.pop()
            removed_diagonal = diagonals.pop()
            while removed_diagonal[0] not in current_triangle.get_nodes() and removed_diagonal[1] not in current_triangle.get_nodes():
                removed_diagonal = diagonals.pop()
        prev_triangle = current_triangle
        current_triangle_nodes = current_triangle.get_nodes()
        #print(current_triangle)
        for node in current_triangle_nodes:
            node_triangles = node.triangles
            #print(node_triangles)
            if len(node_triangles) > 1:
                #print(node_triangles)
                for t in node_triangles:
                    if not t.visited:
                        diagonal = current_triangle.find_common_diagonal(t)
                        if not diagonal:
                            continue
                        triangles_traversed += 1
                        current_triangle.neighbours_visited += 1
                        if not current_triangle.visited_all_neighbours():
                            potential_triangles.append(current_triangle)
                        else:
                            if current_triangle in potential_triangles:
                                potential_triangles.remove(current_triangle)
                        t.visited = True
                        diagonals.append((diagonal[0], diagonal[1]))
                        current_triangle = t
                        if t == triangle_q:
                            diagonals.append((node, Node(q)))
                            done = True
                            break

    print(triangles_traversed)
    print(diagonals)
    return diagonals







