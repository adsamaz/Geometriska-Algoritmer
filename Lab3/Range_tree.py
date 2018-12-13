import types


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
        self.splitting_value = splitting_value # Largest point in the left subtree
        self.max_value = max_value


class Range_tree:

    def __init__(self, points):
        self.root = self.create_tree(points)


    def create_tree(self, input_points):
        points = sorted(input_points)
        length = len(points)
        if length == 1:
            return Leaf(points.pop())
        else:
            left_subtree = Range_tree(points[:length//2])
            right_subtree = Range_tree(points[length//2:])

            splitting_value = 0
            max_value = 0
            if isinstance(left_subtree.root, Node):
                splitting_value = left_subtree.root.max_value
            else:
                splitting_value = left_subtree.root.p
            if isinstance(right_subtree.root, Node):
                max_value = right_subtree.root.max_value
            else:
                max_value = right_subtree.root.p

            return Node(left_subtree, right_subtree, splitting_value, max_value)


    def range_query(self, interval):
        v_split = self.find_split_node(interval)
        if isinstance(v_split, Leaf):
            if v_split.p >= interval[0] and v_split.p <= interval[1]:
                return [v_split]
            else:
                print("No node value could be found")
        else:
            reported_leaves = []
            v = v_split.left_subtree.root
            while isinstance(v, Node):
                if interval[0] <= v.splitting_value:
                    reported_leaves.extend(self.report_subtree(v.right_subtree.root))
                    v = v.left_subtree.root
                else:
                    v = v.right_subtree.root



    #def __repr__(self):
        #return "Splitting value: " + str(self.root.splitting_value) + " Max value: " + str(self.root.max_value)

    def find_split_node(self, interval):
        v = self.root
        while isinstance(v, Node) and (interval[1] <= v.splitting_value or interval[0] > v.splitting_value):
            if interval[1] <= v.splitting_value:
                v = v.left_subtree.root
            else:
                v = v.right_subtree.root
        return v


    def report_subtree(self, root):
        if isinstance(root, Leaf):
            return root.report()
        return self.report_subtree(root.left_subtree.root) + self.report_subtree(root.right_subtree.root)


list = [(1, 2), (3, 1), (2, 1), (5, 1), (6, 4), (4, 4)]
root = Range_tree(list)
print(root.range_query([0, 1]))