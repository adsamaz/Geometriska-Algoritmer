
def smallest_circle_brute(p):
    circle = Circle((2, 1), 5)
    print(circle.center)
    print(circle.radius)





class Circle(object):
    def __init__(self, center, radius):
        self.center, self.radius = center, radius


smallest_circle_brute([])