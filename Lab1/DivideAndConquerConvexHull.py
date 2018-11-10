import math

import numpy

from Lab1.Convex_hull import right_turn
from Lab1.Convex_hull import sort_points
from Lab1.Convex_hull import convex_hull


def daq_convex_hull(p):
    p = sort_points(p)
    return daq_help_function(p)


def daq_help_function(p):
    if len(p) <= 5:
        return convex_hull(p)

    first_half = p[:len(p)//2]
    second_half = p[len(p)//2:]

    a = daq_help_function(first_half)
    b = daq_help_function(second_half)

    # Compute
    upper_a, upper_b = upper_tangent(a, b)
    lower_a, lower_b = lower_tangent(a, b)

    # Merge
    if lower_b == 0:
        b_list = b[upper_b:] + b[:1]
    else:
        b_list = b[upper_b:lower_b + 1]

    if lower_a == 0:
        a_list = []
    else:
        a_list = a[lower_a:]

    return a[:upper_a + 1] + b_list + a_list


def upper_tangent(a, b):
    index_a = rightmost_point_index(a)
    index_b = leftmost_point_index(b)
    done = False
    # get the upper points
    while not done:
        done = True
        while not right_turn([a[index_a], b[index_b], b[get_next_index(b, index_b)]]): #and not right_turn([a[index_a], b[index_b], b[get_prev_index(b, index_b)]]):         # check if line is above b
            index_b = get_next_index(b, index_b)
        while right_turn([b[index_b], a[index_a], a[get_prev_index(a, index_a)]]): #and right_turn([b[index_b], a[index_a], a[get_next_index(a, index_a)]]):     # check if line is above a
            index_a = get_prev_index(a, index_a)
            done = False

    return index_a, index_b


def lower_tangent(a, b):
    index_a = rightmost_point_index(a)
    index_b = leftmost_point_index(b)
    done = False
    # get the lower points
    while not done:
        done = True
        while not right_turn([b[index_b], a[index_a], a[get_next_index(a, index_a)]]): #and not right_turn([b[index_b], a[index_a], a[get_prev_index(a, index_a)]]):      # check if line is below a
            index_a = get_next_index(a, index_a)
        while right_turn([a[index_a], b[index_b], b[get_prev_index(b, index_b)]]): #and right_turn([a[index_a], b[index_b], b[get_next_index(b, index_b)]]):  # check if line is above a
            index_b = get_prev_index(b, index_b)
            done = False

    return index_a, index_b


def get_next_index(p, index):
    if index + 1 < len(p):
        return index + 1
    else:
        return 0


def get_prev_index(p, index):
    if index - 1 >= 0:
        return index - 1
    else:
        return len(p) - 1


def rightmost_point_index(p):
    rmp = - math.inf
    rmp_index = 0
    for i in range(0, len(p)):
        if p[i][0] > rmp:
            rmp = p[i][0]
            rmp_index = i
    return rmp_index

def leftmost_point_index(p):
    rmp = math.inf
    rmp_index = 0
    for i in range(0, len(p)):
        if p[i][0] < rmp:
            rmp = p[i][0]
            rmp_index = i
    return rmp_index


# list = [(0, 0),(50, 50),(0, 50),(100, 50),(100,500),(100, 500),(300, 200),(100, 50),(100,500),(100, 500),(300, 200)]
# print(daq_convex_hull(list))
