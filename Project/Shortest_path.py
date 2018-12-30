from queue import Queue, Empty
from Project.Ear_clipping import *

class Double_ended_queue:

    def __init__(self, apex, start_left, start_right):
        self.apex = apex
        self.apex_index = 0
        self.left_queue = [apex, start_left]
        self.right_queue = [apex, start_right]

    def get_head_left(self):
        return self.left_queue[-1]

    def get_head_right(self):
        return self.right_queue[-1]

def shortest_path(p, q, triangles):
    triangle_p = None
    triangle_q = None
    start_node = Node(p)
    end_node = Node(q)
    for t in triangles:                 #Find the triagles the two points lie inside of
        if point_inside_polygon(p, t.get_nodes()):
            triangle_p = t
        if point_inside_polygon(q, t.get_nodes()):
            triangle_q = t
    if triangle_p == triangle_q:        #If both points are inside the same triangle -> Done
        return [start_node, end_node]

    diagonals = breadth_first_search(triangle_p, triangle_q)
    add_last_diagonal(diagonals, end_node)
    #return diagonals
    start_diagonal = diagonals.pop(0)
    deq = Double_ended_queue(start_node, start_diagonal[0], start_diagonal[1])
    apex_i = 0
    for i in range(0, len(diagonals)):
        # z = r_i+1. The new vertex is should be appended to the right queue
        if deq.get_head_left() in diagonals[i]:
            z = diagonals[i][0] if diagonals[i][1] == deq.get_head_left() else diagonals[i][1]
            while True:
                if deq.get_head_right() == deq.apex:
                    apex_i = build_new_path_right_queue(apex_i, deq, z)
                    break
                if not is_convex(deq.right_queue[len(deq.right_queue) - 2], deq.get_head_right(), z):
                    deq.right_queue.append(z)
                    break
                deq.right_queue.pop()
        # z = l_i+1. The new vertex is should be appended to the right queue
        elif deq.get_head_right() in diagonals[i]:
            z = diagonals[i][0] if diagonals[i][1] == deq.get_head_right() else diagonals[i][1]
            while True:
                if deq.get_head_left() == deq.apex:
                    apex_i = build_new_path_left_queue(apex_i, deq, z)
                    break
                if is_convex(deq.left_queue[len(deq.left_queue) - 2], deq.get_head_left(), z):
                    deq.left_queue.append(z)
                    break
                deq.left_queue.pop()
        else:
            print("error?")

    if deq.get_head_left() == end_node:
        print(deq.left_queue)
        return deq.left_queue
    elif deq.get_head_right() == end_node:
        print(deq.right_queue)
        return deq.right_queue
    else:
        print("No queue ends at q")


def build_new_path_left_queue(apex_i, deq, z):
    deq.left_queue.pop()
    try:
        while not is_convex(deq.right_queue[apex_i], deq.right_queue[apex_i + 1], z):
            deq.left_queue.append(deq.right_queue[apex_i])
            apex_i += 1
    except IndexError:
        print("index error")
        pass
        # deq.left_queue.append(deq.right_queue[apex_i])
        # apex_i += 1
        # deq.right_queue.append(z)
    deq.left_queue.append(deq.right_queue[apex_i])
    deq.left_queue.append(z)
    deq.apex = deq.right_queue[apex_i]
    return apex_i


def build_new_path_right_queue(apex_i, deq, z):
    deq.right_queue.pop()
    try:
        while is_convex(deq.left_queue[apex_i], deq.left_queue[apex_i + 1], z):
            deq.right_queue.append(deq.left_queue[apex_i])
            apex_i += 1
            # deq.right_queue.append(deq.left_queue[apex_i])
    except IndexError:
        print("index error")
        pass
        # deq.right_queue.append(deq.left_queue[apex_i])
        # apex_i += 1
        # deq.left_queue.append(z)
    deq.right_queue.append(deq.left_queue[apex_i])
    deq.right_queue.append(z)
    deq.apex = deq.left_queue[apex_i]
    return apex_i


def add_last_diagonal(diagonals, end_node):
    d_length = len(diagonals)
    if d_length > 1:
        if diagonals[d_length - 1][0] in diagonals[d_length - 2]:
            diagonals.append((diagonals[d_length - 1][0], end_node))
        else:
            diagonals.append((diagonals[d_length - 1][1], end_node))
    else:
        diagonals.append((diagonals[d_length - 1][0], end_node))

def breadth_first_search(start, end):
    # a FIFO open_set
    open_set = Queue()
    # an empty set to maintain visited nodes
    closed_set = set()
    # a dictionary to maintain meta information (used for path formation)
    # key -> (parent state, action to reach child)
    meta = dict()
    # initialize
    root = start
    meta[root] = (None, None)
    open_set.put(root)
    # For each node on the current level expand and process, if no children (leaf) then unwind
    while not open_set.empty():
        #subtree_root = open_set.dequeue()
        subtree_root = open_set.get()

        # We found the node we wanted so stop and emit a path.
        if subtree_root == end:
            return construct_path(subtree_root, meta)
        # For each child of the current tree process
        for child in subtree_root.find_neighbour_triangles():
            # The node has already been processed, so skip over it
            if child in closed_set:
                continue
            action = subtree_root.find_common_diagonal(child)
            # The child is not enqueued to be processed, so enqueue this level of children to be expanded
            if not in_queue(open_set, child):
                meta[child] = (subtree_root, action)  # create metadata for these nodes
                open_set.put(child)  # enqueue these nodes
        # We finished processing the root of this subtree, so add it to the closed set
        closed_set.add(subtree_root)

def in_queue(queue, item):
    my_copy = []
    while True:
        try:
            elem = queue.get(block=False)
        except Empty:
            break
        else:
            my_copy.append(elem)
    for elem in my_copy:
        queue.put(elem)
    if item in my_copy:
        return True
    else:
        return False

# Produce a backtrace of the actions taken to find the goal node, using the recorded meta dictionary
def construct_path(state, meta):
    action_list = []
    # Continue until you reach root meta data (i.e. (None, None))
    s = state
    while meta[s][0] is not None:
        s, action = meta[s]
        action_list.append(action)

    action_list.reverse()
    return action_list
