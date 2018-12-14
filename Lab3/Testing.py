from random import randint, uniform

from Lab3.Range_tree import *
import math

points = []
for i in range(10**6):
    points.append((randint(0, 10**6), uniform(0, 10**6)))


class Brute_range_tree:

    def __init__(self, points):
        self.points = sorted(points)

    def query(self, interval):
        a = self.get_lower_index(interval[0])
        a = self.get_upper_index(interval[1])

    def get_lower_index(self, bound):
        length = len(self.points)
        if length
        if self.points[length//2] < bound:



"""tree = Range_tree(list)
interval = [5, 8]
print(tree.range_query(interval))
print(tree.number_in_range(interval))
print(tree.max_weight_in_range(interval))"""