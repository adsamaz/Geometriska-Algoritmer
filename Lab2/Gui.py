from random import *
from tkinter import *
import nil
#from win32api import GetSystemMetrics
from Lab2.Smallest_circle import smallest_circle_brute, smallest_circle_randomized
from Lab2.Smallest_rectangle import smallest_rectangle

# GUI


class Gui(Frame):
    list = []
    canvas = nil
    scale = (2**28 - 1)
    #screen_width = GetSystemMetrics(0) - 30
    screen_height = 500
    margin = 3*10**6
    filename = "input.txt"

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

    def randomize(self):
        self.clear_canvas()
        self.list.clear()
        for i in range(100):
            self.list.append((randint(200, 600), randint(130, 400)))
            self.draw_point(self.list[i])

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

    def draw_line(self, point1, point2):
        self.canvas.create_line(point1[0],
                                point1[1],
                                point2[0],
                                point2[1])

    def draw_circle(self, mid_point, radius):
        self.canvas.create_oval(mid_point[0] - radius,
                                mid_point[1] + radius,
                                mid_point[0] + radius,
                                mid_point[1] - radius)

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        b1 = Button(self, text="Randomize", command=self.randomize)
        b2 = Button(self, text="From File", command=self.from_file)
        b3 = Button(self, text="Smallest Circle with Brute Force", command=self.compute_smallest_circle_brute)
        b4 = Button(self, text="Smallest Circle with Randomization", command=self.compute_smallest_circle_randomized)
        b5 = Button(self, text="Smallest rectangle with Rotating Callipers", command=self.compute_smallest_rectangle)
        b1.pack()
        b2.pack()
        b3.pack()
        b4.pack()
        b5.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

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
        for i in range(0, 4):
            self.draw_line(vertices[i - 1], vertices[i])


def main():
    root = Tk()
    ex = Gui()
    root.geometry("400x250+300+300")
    root.mainloop()


main()


