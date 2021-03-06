from random import randint, uniform
from datetime import datetime
from Lab3.Range_tree import *
import math

class Brute_range_tree:

    def __init__(self, points):
        self.points = sorted(points)
        pass

    def query(self, interval):
        result = []
        for p in self.points:
            if p[0] >= interval[0] and p[0] <= interval[1]:
                result.append(p)
        return result

    def number_of_points(self, interval):
        result = self.query(interval)
        return len(result)

    def max_weight(self, interval):
        result = self.query(interval)
        max_weight = 0
        for i in result:
            if i[1] > max_weight:
                max_weight = i[1]
        return max_weight

    def get_lower_index(self, bound):
        length = len(self.points)
        if length == 1:
            return
        if self.points[length//2] < bound:
            pass

def print_tree(tree):
    if isinstance(tree, Leaf):
        print("Leafs: " + str(tree.report()))
        return tree
    left = print_tree(tree.left_subtree)
    right = print_tree(tree.right_subtree)



# ---------TESTING----------
def generate_points(n, max_p, max_w):
    points = []
    for i in range(n):
        points.append((randint(0, max_p), round(uniform(0, max_w), 2)))
    return points

def generate_interval(sorted_points, size):
    start_index = randint(0, len(sorted_points) - size)
    end_index = start_index + size - 1
    return sorted_points[start_index][0], sorted_points[end_index][0]


#points = []#[(68, 6594.018599353925), (128, 2753.3211224838806), (147, 9418.081213151996), (248, 3801.635204789278), (281, 1814.5108576105329), (330, 5544.207000476666), (508, 4034.815721269338), (528, 8624.518600203424), (759, 3834.958805222345), (767, 5462.398912624811), (813, 9122.229284181605), (845, 5573.129695742626), (848, 40.06249121166427), (862, 8142.230828015395), (873, 3438.2153801656978), (892, 4519.0822613798755), (997, 3031.502442901893), (1010, 9996.576671707622), (1127, 4708.5553360365175), (1273, 9127.391033197693), (1298, 4108.962254718757), (1319, 409.3386734430948), (1399, 1894.1424145989627), (1438, 8966.777457454393), (1485, 8876.720127997156), (1521, 8699.840551607136), (1715, 5317.736748908263), (1773, 1912.5621054777298), (1857, 228.8748577104638), (1880, 8706.478578771372), (1881, 1799.6254245089137), (1896, 6580.586911424607), (1907, 8310.0899009355), (1944, 4688.6568255791335), (2072, 9274.39733317251), (2075, 3614.810381978463), (2085, 561.3900076275735), (2135, 3833.644048513296), (2221, 4745.73995134976), (2245, 4621.034625839476), (2376, 6347.86010840347), (2419, 847.0651311494304), (2440, 4029.0323306121413), (2607, 5905.37763806946), (2728, 9550.861860360006), (2759, 1866.081691603998), (2767, 7047.974180208215), (2805, 7534.74031296014), (2892, 2702.80989551946), (2928, 527.8781594936821), (3026, 1067.9532244386314), (3029, 480.2587184419882), (3037, 1248.7633784273035), (3120, 7220.864502166686), (3182, 4602.339943644772), (3205, 6595.218703523406), (3210, 2549.167773886262), (3279, 2088.246646916093), (3340, 9365.434808729144), (3343, 1769.590553229734), (3346, 1760.8640819278587), (3408, 8738.073682234563), (3551, 831.6765395120628), (3613, 4187.737447753363), (3617, 2243.7827894005613), (3634, 1385.299943116951), (3652, 3132.9201852964948), (3808, 5194.162623690677), (3844, 7625.392773806215), (3856, 9736.432457615947), (3959, 7863.7500327025145), (4018, 1454.132420565538), (4034, 9186.564140339711), (4118, 4172.085161831705), (4191, 7045.512264976035), (4331, 8536.365877472112), (4397, 508.5807902873163), (4480, 8317.159339417913), (4486, 1016.239413467408), (4509, 7082.414063271543), (4518, 5004.595752591065), (4554, 1626.9130232326756), (4665, 9053.070440929807), (4744, 2086.119199033587), (4963, 890.8044211187128), (4995, 5751.265258019779), (5036, 4412.6681791615), (5041, 9457.230025233015), (5057, 8010.77444731533), (5073, 467.4620858927914), (5154, 6499.8938945686095), (5159, 2782.630550723001), (5315, 2775.3688527314926), (5329, 1748.804523460835), (5586, 1032.2553949844337), (5697, 4771.11546013437), (5746, 3123.5317454108904), (5970, 8903.409342151244), (5991, 2231.4087044050566), (6052, 9935.750073242803), (6304, 2064.533691239405), (6324, 9849.547175319627), (6325, 6415.36177183374), (6350, 7998.263946092337), (6608, 6875.00882043863), (6701, 7044.536621909836), (6757, 5327.129477508844), (6759, 9110.311958230048), (6832, 5583.661132110816), (6890, 8471.913688891405), (6913, 6882.288116321383), (6939, 7969.314092247772), (6961, 6249.757126517344), (7003, 6546.494229591807), (7071, 9585.962136651555), (7324, 1094.7248747737904), (7361, 4804.963072827957), (7412, 1167.5929702989097), (7482, 7627.43288623147), (7529, 7159.171906407166), (7537, 1167.347211768277), (7571, 4960.492122146342), (7661, 2997.109779175484), (7702, 7616.433844053484), (7783, 7491.906903459587), (7870, 4321.795320820681), (7993, 4071.8525548162365), (8237, 3274.7540500138407), (8296, 5403.488590090907), (8300, 5594.250019508684), (8336, 8747.461372771597), (8448, 7648.420972239836), (8588, 4293.118681994331), (8618, 684.8228736530559), (8838, 9748.107645750777), (8887, 9997.07793436737), (8922, 7892.860568901106), (9299, 9669.545328669205), (9316, 6832.303073593646), (9323, 789.9377820854181), (9401, 2895.58575004112), (9437, 3762.024128486514), (9503, 7166.969395719607), (9530, 5354.736924766883), (9612, 6747.313710988626), (9769, 7099.277654966219), (9797, 296.0815207183576), (9808, 2112.4102586732383), (9906, 7958.375748090215), (9948, 769.444623799952)]
def correctness_test():
    n = 10**5
    max_p = 10**5
    max_w = 10**5

    error = False
    number_of_tests = 1
    for i in range(number_of_tests):
        k = randint(1, 10**5) #10**4
        points = generate_points(n, max_p, max_w)
        sorted_points = sorted(points)
        interval = generate_interval(sorted_points, k)
        print("Points: " + str(sorted_points))
        print("Interval: " + str(interval))


        print("\n\nCreating Brute list")
        brute = Brute_range_tree(points)
        print("Brute list done")
        print("Creating range tree")
        tree = Range_tree(points)
        print("Range tree done\n")


        print("---------BRUTE FORCE vs RANGE TREE----------")

        print("-----Query results-----")
        brute_result = brute.query(interval)
        tree_result = tree.range_query(interval)
        print("Brute Results: " + str(brute_result))
        print("Tree Results: " + str(tree_result))
        if brute_result == tree_result:
            print("Both implementations returned the same result!")
        else:
            print("OOPS, Different results??")
            error = True

        print("\n-----Number of points-----")
        brute_result = brute.number_of_points(interval)
        tree_result = tree.number_in_range(interval)
        print("Brute: " + str(brute_result) + ", Range tree: " + str(tree_result))
        if brute_result != tree_result:
            error = True

        print("\n-----Max weight-----")
        brute_result = brute.max_weight(interval)
        tree_result = tree.max_weight_in_range(interval)
        print("Brute: " + str(brute_result) + ", Range tree: " + str(tree_result))
        if brute_result != tree_result:
            error = True

    print("\nError == " + str(error))


def test_number_of_points():
    n = 10**6
    k = 10**6
    max_p = 10 ** 5
    max_w = 10 ** 5
    number_of_tests = 20
    total_average = 0
    margin = 2
    counter = 0
    non_zero_runs = 0
    while True:
        print(counter)
        current_average = 0
        non_zero_runs_inner = 0
        points = generate_points(n, max_p, max_w)
        sorted_points = sorted(points)

        brute = Brute_range_tree(points)
        tree = Range_tree(points)
        for i in range(number_of_tests):
            print("inner loop")

            interval = generate_interval(sorted_points, k)

            time = datetime.now()
            for i in range(20):
                brute.number_of_points(interval)
            brute_time = datetime.now() - time

            time = datetime.now()
            for i in range(20):
                tree.number_in_range(interval)
            tree_time = (datetime.now() - time)

            try:
                print("Brute time: " + str(brute_time) + ", Tree time: " + str(tree_time))
                ratio = brute_time / tree_time
                current_average += ratio
                non_zero_runs_inner += 1
            except ZeroDivisionError:
                pass


        if current_average == 0:
            pass
        else:
            non_zero_runs += 1
            total_average += current_average / non_zero_runs_inner

        try:
            print("Current Average: " + str(current_average/non_zero_runs_inner))
            print("Total Average: " + str(total_average/non_zero_runs))
            if current_average/non_zero_runs_inner > total_average/non_zero_runs - margin and current_average/non_zero_runs_inner < total_average/non_zero_runs + margin and current_average != 0 and non_zero_runs >= 2:
                break
        except ZeroDivisionError:
            print("Zero run")


        counter += 1


    try:
        print(total_average/non_zero_runs)
    except ZeroDivisionError:
        print("No nonzero runs found")


correctness_test()
#test_number_of_points()