from random import *
from tkinter import *
import nil
#from win32api import GetSystemMetrics
from Lab2.Smallest_circle import smallest_circle_brute, smallest_circle_randomized
from Lab2.Smallest_rectangle import smallest_rectangle
from Lab2.Visibility_polygon import Visibility_polygon_class
from Lab1.Convex_hull import convex_hull
from Lab1.DivideAndConquerConvexHull import daq_convex_hull
from Project.Generate_polygon import generate_polygon
from Project.Ear_clipping import ear_clip
from sympy import Point, Segment, Line, Ray, pi, Polygon, evalf, tan, atan, oo

# GUI


class Gui(Frame):
    list = []
    canvas = nil
    scale = (2**28 - 1)
    #screen_width = GetSystemMetrics(0) - 30
    screen_height = 500
    margin = 3*10**6
    filename = "input.txt"
    origin = (0, 0)

    def __init__(self):
        super().__init__()
        self.initUI()

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_point(self, point):
        python_green = "#476042"
        radius = 1.5
        x1, y1 = point[0] - radius, \
                 point[1] - radius
        x2, y2 = point[0] + radius, \
                 point[1] + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    def draw_segment(self, point):
        python_green = "#476042"
        radius = 1.5
        p1 = point.p1
        p2 = point.p2
        x1, y1 = p1.x - radius, \
                 p1.y - radius
        x2, y2 = p1.x + radius, \
                 p1.y + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)
        x1, y1 = p2.x - radius, \
                 p2.y - radius
        x2, y2 = p2.x + radius, \
                 p2.y + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)
        self.draw_line(p1, p2, width=2)

    def randomize_points(self):
        self.clear_canvas()
        self.list.clear()
        for i in range(10):
            self.list.append((randint(200, 800), randint(130, 500)))
            self.draw_point(self.list[i])

    def randomize_segments(self):
        self.clear_canvas()
        self.list.clear()
        i = 0
        while i < 5:
            segment = Segment( Point(randint(200, 600), randint(130, 400)), Point(randint(200, 600), randint(130, 400)) )
            if self.intersects(segment):
                continue
            self.list.append(segment)
            self.draw_segment(self.list[i])
            i += 1
        self.origin = (randint(200, 600), randint(130, 400))
        self.draw_point(self.origin)

    def randomize_polygon(self):
        self.clear_canvas()
        self.list.clear()
        i = 0
        self.list = generate_polygon(10)
        while i < len(self.list):
            self.draw_point(self.list[i])
            self.draw_line(self.list[i - 1], self.list[i])
            i += 1

    def from_file(self):
        self.clear_canvas()
        self.list.clear()
        file = open(self.filename, "r")
        for line in file:
            try:
                point = line.split(" ")
                tuple = (int(point[0]), int(point[1]))
                self.list.append(tuple)
            except():
                print("Wrong file format")

        for point in self.list:
            self.draw_point(point)

    def draw_line(self, point1, point2, color="#000000", width = 1):
        self.canvas.create_line(float(point1[0]),
                                float(point1[1]),
                                float(point2[0]),
                                float(point2[1]), fill=color, width=width)

    def draw_circle(self, mid_point, radius):
        self.canvas.create_oval(mid_point[0] - radius,
                                mid_point[1] + radius,
                                mid_point[0] + radius,
                                mid_point[1] - radius)

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

        b1 = Button(self, compound=TOP, text="Randomize Points", command=self.randomize_points)
        b8 = Button(self, compound=TOP, text="Randomize Segments", command=self.randomize_segments)
        b10 = Button(self, compound=TOP, text="Randomize Polygon", command=self.randomize_polygon)
        b2 = Button(self, compound=TOP, text="From File", command=self.from_file)
        b3 = Button(self, compound=TOP, text="Smallest Circle with Brute Force", command=self.compute_smallest_circle_brute)
        b4 = Button(self, compound=TOP, text="Smallest Circle with Randomization", command=self.compute_smallest_circle_randomized)
        b5 = Button(self, compound=TOP, text="Smallest rectangle RC", command=self.compute_smallest_rectangle)
        b6 = Button(self, compound=TOP, text="Convex Hull Inc", command=self.compute_convex_hull)
        b7 = Button(self, compound=TOP, text="Convex Hull DaQ", command=self.compute_convex_hull_daq)
        b9 = Button(self, compound=TOP, text="Visibility Polygon", command=self.compute_visibility_polygon)
        b11 = Button(self, compound=TOP, text="Triangulate", command=self.compute_triangulation)

        b1.pack(side=LEFT, fill=BOTH, expand=1)
        b8.pack(side=LEFT, fill=BOTH, expand=1)
        b10.pack(side=LEFT, fill=BOTH, expand=1)
        b2.pack(side=LEFT, fill=BOTH, expand=1)
        b3.pack(side=LEFT, fill=BOTH, expand=1)
        b4.pack(side=LEFT, fill=BOTH, expand=1)
        b5.pack(side=LEFT, fill=BOTH, expand=1)
        b6.pack(side=LEFT, fill=BOTH, expand=1)
        b7.pack(side=LEFT, fill=BOTH, expand=1)
        b9.pack(side=LEFT, fill=BOTH, expand=1)
        b11.pack(side=LEFT, fill=BOTH, expand=1)



    def compute_smallest_circle_brute(self):
        circle = smallest_circle_brute(self.list)
        self.draw_circle(circle.midpoint, circle.radius)
        self.draw_point(circle.midpoint)

    def compute_smallest_circle_randomized(self):
        circle = smallest_circle_randomized(self.list)
        self.draw_circle(circle.midpoint, circle.radius)
        self.draw_point(circle.midpoint)

    def compute_smallest_rectangle(self):
        rectangle = smallest_rectangle(self.list)
        print(rectangle.area)
        vertices = rectangle.vertices
        for i in range(0, len(vertices)):
            self.draw_line(vertices[i - 1], vertices[i])

    def compute_convex_hull(self):
        ch = convex_hull(self.list)
        for i in range(0, len(ch)):
            self.draw_line(ch[i - 1], ch[i])

    def compute_convex_hull_daq(self):
        ch = daq_convex_hull(self.list)
        for i in range(0, len(ch)):
            self.draw_line(ch[i - 1], ch[i])

    def compute_visibility_polygon(self):
        vpc = Visibility_polygon_class()
        vp = vpc.get_visibility_polygon(self.list, self.origin)
        #vp = vpc.get_visibility_polygon(self.list, self.origin).values()
        #for i in vp:
           #self.draw_line(i.p1.p, i.p2.p, "red")
        for i in range(0, len(vp)):
            self.draw_line(vp[i - 1], vp[i], "red")

    def compute_triangulation(self):
        triangulation = ear_clip(self.list)
        for t in triangulation:
            self.draw_line(t.p1.p, t.p2.p, "red")
            self.draw_line(t.p2.p, t.p3.p, "red")
            self.draw_line(t.p3.p, t.p1.p, "red")
        for i in range(0, len(self.list)):
            self.draw_line(self.list[i-1], self.list[i])


    def intersects(self, segment):
        for s in self.list:
            if not segment.intersection(s) == []:
                return True
        return False


def main():
    root = Tk()
    ex = Gui()
    root.geometry("400x250+300+300")
    root.mainloop()


main()


