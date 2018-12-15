

class Leaf:

    def __init__(self, point):
        self.p = point[0]
        self.w = point[1]

    def report(self):
        return [(self.p, self.w)]

class Node:

    def __init__(self, left_subtree, right_subtree, splitting_value, max_value):
        self.left_subtree = left_subtree
        self.right_subtree = right_subtree
        self.splitting_value = splitting_value  # Largest point in the left subtree
        self.max_value = max_value              # Largest p in the subtree

        self.number_of_points = 0
        self.max_weight = 0                     # Largest w in the subtree

class Range_tree:

    def __init__(self, input_points):
        points = sorted(input_points)
        self.root = self.create_tree(points)
        self.add_properties(self.root)          # Traverse the tree and add number of points and max weight to all nodes

    def create_tree(self, points):
        length = len(points)
        if length == 1:
            return Leaf(points[0])
        else:
            mid = length // 2
            left_subtree = self.create_tree(points[:mid])
            right_subtree = self.create_tree(points[mid:])

            if isinstance(left_subtree, Node):
                splitting_value = left_subtree.max_value
            else:
                splitting_value = left_subtree.p

            if isinstance(right_subtree, Node):
                max_value = right_subtree.max_value
            else:
                max_value = right_subtree.p

            return Node(left_subtree, right_subtree, splitting_value, max_value)


    def range_query(self, interval):
        v_split = self.find_split_node(interval)
        if isinstance(v_split, Leaf):
            if v_split.p >= interval[0] and v_split.p <= interval[1]:
                return v_split.report()
            else:
                print("No node value could be found")
                return False
        else:
            reported_leaves = []

            # Follow the path to x and report the points in subtrees right of the path
            v = v_split.left_subtree
            while isinstance(v, Node):
                if interval[0] <= v.splitting_value:
                    reported_leaves = self.report_subtree(v.right_subtree) + reported_leaves
                    v = v.left_subtree
                else:
                    v = v.right_subtree
            if v.p >= interval[0] and v.p <= interval[1]:
                reported_leaves = v.report() + reported_leaves

            # follow the path to x' and report the points in subtrees left of the path
            v = v_split.right_subtree
            while isinstance(v, Node):
                if interval[1] >= v.splitting_value:
                    reported_leaves.extend(self.report_subtree(v.left_subtree))
                    v = v.right_subtree
                else:
                    v = v.left_subtree
            if v.p >= interval[0] and v.p <= interval[1]:
                reported_leaves =  reported_leaves + v.report()

        return reported_leaves

    def number_in_range(self, interval):
        v_split = self.find_split_node(interval)
        if isinstance(v_split, Leaf):
            if v_split.p >= interval[0] and v_split.p <= interval[1]:
                return 1
            else:
                print("No node value could be found")
                return False
        else:
            count = v_split.number_of_points

            # Follow the path to x and report the points in subtrees right of the path
            v = v_split.left_subtree
            while isinstance(v, Node):
                if interval[0] <= v.splitting_value:
                    v = v.left_subtree
                else:
                    if isinstance(v.left_subtree, Node):
                        count -= v.left_subtree.number_of_points
                    else:
                        count -= 1
                    v = v.right_subtree
            if not (v.p >= interval[0] and v.p <= interval[1]):
                count -= 1

            # follow the path to x' and report the points in subtrees left of the path
            v = v_split.right_subtree
            while isinstance(v, Node):
                if interval[1] >= v.splitting_value:
                    v = v.right_subtree
                else:
                    if isinstance(v.right_subtree, Node):
                        count -= v.right_subtree.number_of_points
                    else:
                        count -= 1
                    v = v.left_subtree
            if not( v.p >= interval[0] and v.p <= interval[1]):
                count -= 1

        return count

    def max_weight_in_range(self, interval):
        v_split = self.find_split_node(interval)
        if isinstance(v_split, Leaf):
            if v_split.p >= interval[0] and v_split.p <= interval[1]:
                return v_split.w
            else:
                print("No node value could be found")
                return False
        else:
            # Follow the path to x and report the points in subtrees right of the path
            max_weight_left = v_split.max_weight
            v = v_split.left_subtree
            while isinstance(v, Node):
                if interval[0] <= v.splitting_value:
                    v = v.left_subtree
                else:
                    if isinstance(v.right_subtree, Node):
                        max_weight_left = v.right_subtree.max_weight
                    else:
                        max_weight_left = v.right_subtree.w
                    v = v.right_subtree
            if v.p >= interval[0] and v.p <= interval[1]:
                max_weight_left = max(v.w, max_weight_left)

            # follow the path to x' and report the points in subtrees left of the path
            max_weight_right = v_split.max_weight
            v = v_split.right_subtree
            while isinstance(v, Node):
                if interval[1] >= v.splitting_value:
                    v = v.right_subtree
                else:
                    if isinstance(v.left_subtree, Node):
                        max_weight_right = v.left_subtree.max_weight
                    else:
                        max_weight_right = v.left_subtree.w
                    v = v.left_subtree
            if v.p >= interval[0] and v.p <= interval[1]:
                max_weight_right = max(v.w, max_weight_right)

        return max(max_weight_left, max_weight_right)

    def find_split_node(self, interval):
        v = self.root
        while isinstance(v, Node) and (interval[1] < v.splitting_value or interval[0] > v.splitting_value):
            if interval[1] <= v.splitting_value:
                v = v.left_subtree
            else:
                v = v.right_subtree
        return v

    def report_subtree(self, node):
        if isinstance(node, Leaf):
            return node.report()
        return self.report_subtree(node.left_subtree) + self.report_subtree(node.right_subtree)

    def add_properties(self, v):
        if isinstance(v, Leaf):
            return 1, v.w

        left_properties = self.add_properties(v.left_subtree)
        right_properties = self.add_properties(v.right_subtree)

        v.number_of_points = left_properties[0] + right_properties[0]
        v.max_weight = max(left_properties[1], right_properties[1])

        return v.number_of_points, v.max_weight

"""list = [(1, 2), (3, 1), (2, 1), (5, 1), (4, 4), (1, 1), (2, 5), (4, 1), (9, 4), (8, 4), (4, 5), (2, 4) ]
tree = Range_tree(list)
interval = [5, 8]
print(tree.range_query(interval))
print(tree.number_in_range(interval))
print(tree.max_weight_in_range(interval))"""