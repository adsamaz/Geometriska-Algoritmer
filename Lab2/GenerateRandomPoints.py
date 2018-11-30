from random import randint


def generate_random_points(number_of_points, xmax, ymax):
    temp = []
    margin = 0
    for i in range(number_of_points):
        temp.append((randint(margin, xmax), randint(margin, ymax)))
    return temp
