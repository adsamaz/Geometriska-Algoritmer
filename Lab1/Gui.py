from random import *
from tkinter import *
import nil
from Lab1 import Convex_hull
from Lab1.DivideAndConquerConvexHull import daq_convex_hull

# GUI



class Gui(Frame):
    list = []
    canvas = nil

    def __init__(self):
        super().__init__()
        self.initUI()

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_point(self, point):
        python_green = "#476042"
        radius = 3
        x1, y1 = (point[0] - radius), (point[1] - radius)
        x2, y2 = (point[0] + radius), (point[1] + radius)
        self.canvas.create_oval(x1, y1, x2, y2, fill=python_green)

    def randomize(self):
        self.clear_canvas()
        self.list.clear()
        self.list.append((1520, 900))
        self.list.append((1410, 500))
        for i in range(20000):
            self.list.append((randint(20, 1200), randint(20, 800)))
            self.draw_point(self.list[i])

    def from_file(self):
        self.clear_canvas()
        self.list.clear()
        filename = "input.txt"
        file = open(filename, "r")
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
        self.canvas.create_line(point1[0], point1[1], point2[0], point2[1])

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        b1 = Button(self, text="Randomize", command=self.randomize)
        b2 = Button(self, text="From File", command=self.from_file)
        b3 = Button(self, text="Compute with Alg 1", command=self.compute_convex_hull)
        b4 = Button(self, text="Compute with Alg 5", command=self.compute_convex_hull_daq)
        b1.pack()
        b2.pack()
        b3.pack()
        b4.pack()

        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def compute_convex_hull(self):
        convex_hull = Convex_hull.convex_hull(self.list)
        for i in range(0, len(convex_hull)):
            self.draw_line(convex_hull[i - 1], convex_hull[i])

    def compute_convex_hull_daq(self):
        convex_hull = daq_convex_hull(self.list)
        for i in range(0, len(convex_hull)):
            self.draw_line(convex_hull[i - 1], convex_hull[i])


def main():
    root = Tk()
    ex = Gui()
    root.geometry("400x250+300+300")
    root.mainloop()


main()


