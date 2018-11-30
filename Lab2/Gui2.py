#!/usr/bin/python3
# -*- coding: utf-8 -*-

from tkinter import *
from Lab2.GenerateRandomPoints import generate_random_points
from Lab2.Smallest_circle_brute import smallest_circle_brute
from Lab2.Smallest_circle_brute import smallest_circle_randomized
import sys

import nil as nil

_author__ = "Jesper Svensson"
_date__= "2018-11-14"


class Gui(Frame):
    list_of_points = []
    canvas = nil
    b_compute = nil
    b_alg = nil
    alg_opt = 1
    number_of_points = 100
    xmax = 900
    width = 500
    scale = (2**16)-1
    margin = 10

    def __init__(self, number_of_points, xmax, ymax):
        super().__init__()
        self.ymax = ymax - 40
        self.xmax = xmax - 10
        self.number_of_points = number_of_points
        self.init_ui()

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw_point(self, point, color):
        radius = 2
        x1, y1 = self.scale_point_x(point[0]) - radius, self.scale_point_y(point[1]) - radius
        x2, y2 = self.scale_point_x(point[0]) + radius, self.scale_point_y(point[1]) + radius
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def scale_point_x(self, i):
        return (i + self.margin) * self.xmax/self.scale

    def scale_point_y(self, i):
        return (i + self.margin) * self.ymax / self.scale

    def draw_line(self, point1, point2, color):
        self.canvas.create_line(self.scale_point_x(point1[0]),
                                self.scale_point_y(point1[1]),
                                self.scale_point_x(point2[0]),
                                self.scale_point_y(point2[1]), fill=color)

    def draw_circle(self, mid_point, radius, color):
        self.canvas.create_oval(self.scale_point_x(mid_point[0] - radius),
                                self.scale_point_y(mid_point[1] + radius),
                                self.scale_point_x(mid_point[0] + radius),
                                self.scale_point_y(mid_point[1] - radius))

    def generate_and_draw_rnd_points(self):
        self.b_compute.config(state="normal")
        self.clear_canvas()
        self.list_of_points.clear()
        self.list_of_points = generate_random_points(self.number_of_points, self.scale, self.scale)
        color = "#000000"
        for i in range(self.number_of_points):
            self.draw_point(self.list_of_points[i], color)

    def from_file(self):
        self.b_compute.config(state="normal")
        filename = "input.txt"
        color = "#000000"
        file = open(filename, "r")
        self.clear_canvas()
        self.list_of_points.clear()
        for line in file:
            try:
                temp = line.split(" ")
                point = (int(temp[0]), int(temp[1]))
                self.list_of_points.append(point)
                self.draw_point(point, color)
            except():
                print("Wrong file format")

    def compute_smallest_circle(self):
        color = "red"
        if self.alg_opt == 1:
            circle = smallest_circle_brute(self.list_of_points)
            print(circle)
            print(circle.midpoint)
            print(circle.radius)
            print(circle.p1)
            print(circle.p2)

        else:
            circle = smallest_circle_randomized(self.list_of_points)
        #self.draw_circle((self.scale/2, self.scale/2), 0.5*self.scale, "red")
        self.draw_circle(circle.midpoint, circle.radius, color)
        self.draw_point(circle.midpoint, color)

    def change_alg(self):
        self.alg_opt = (self.alg_opt + 1) % 2
        if self.alg_opt == 1:
            self.b_alg.config(text="MiniDisc")
        else:
            self.b_alg.config(text="BruteForce")

    def init_ui(self):
        self.master.title("Convex Hull")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)
        b_random = Button(self, compound=BOTTOM, text="Random", command=self.generate_and_draw_rnd_points)
        b_random.pack(side=LEFT, fill=BOTH, expand=1)
        b_file = Button(self, compound=BOTTOM, text="Load file", command=self.from_file)
        b_file.pack(side=LEFT, fill=BOTH, expand=1)
        self.b_compute = Button(self, compound=BOTTOM, text="Compute", state=DISABLED, command=self.compute_smallest_circle)
        self.b_compute.pack(side=LEFT, fill=BOTH, expand=1)
        self.b_alg = Button(self, compound=BOTTOM, text="MiniDisc", command=self.change_alg)
        self.b_alg.pack(side=LEFT, fill=BOTH, expand=1)


def main():
    root = Tk()

    width = 600
    height = 600

    if len(sys.argv) == 2:
        number_of_points = int(sys.argv[1])
    else:
        number_of_points = 10

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    # calculate x and y coordinates for the Tk root window
    x = (ws / 2) - (width / 2)
    y = (hs / 2) - (height / 2)

    gui = Gui(number_of_points, width, height)
    root.geometry('%dx%d+%d+%d' % (width, height, x - 10, y - 30))
    root.mainloop()


if __name__ == '__main__':
    main()
