from sympy import Line, Ray, pi, Polygon, evalf, tan, atan, oo, Segment
from sympy import Point2D
import math

# Global constants
START_VERTEX = 0
END_VERTEX = 1
DEFAULT_VERTEX = -1

# Point class
class Point(object):
    p = (0, 0)
    x = 0
    y = 0
    twin = 0
    type = DEFAULT_VERTEX

    def __init__(self, p, twin):
        self.p = p
        self.x = p.x
        self.y = p.y
        self.twin = twin

# Main
class Visibility_polygon_class(object):
    origin = (0, 0)
    refvec = (0, 1)
    segments = []
    event_queue = []
    status = 0

    def __init__(self):
        self.origin = (0, 0)
        self.refvec = (0, 1)
        self.segments = []
        self.event_queue = []
        self.status = 0

    # Starts here!
    def visibility_polygon(self, segments, origin):
        self.origin = origin
        self.segments = segments
        self.create_event_queue()
        return self.event_queue

    # Create event queue
    def create_event_queue(self):
        # Create a event queue with all points and their connections
        for s in self.segments:
            self.event_queue.append(Point(p=s.p1, twin=s.p2))
            self.event_queue.append(Point(p=s.p2, twin=s.p1))

        # Sort the points in clockwise order
        self.event_queue = sorted(self.event_queue, key=self.get_key)
        # Add type to each point and their connected point. START_VERTEX or END_VERTEX
        for p in self.event_queue:
            if p.type == DEFAULT_VERTEX:
                p.type = START_VERTEX
                p.twin.type = END_VERTEX

    # Gets key for sorting
    def get_key(self, point):
        return self.clockwiseangle_and_distance(point.p)

    # returns the angle and length vector from the origin to the point
    def clockwiseangle_and_distance(self, point):
        # Vector between point and the origin: v = p - o
        vector = [point[0] - self.origin[0], point[1] - self.origin[1]]
        # Length of vector: ||v||
        lenvector = math.hypot(vector[0], vector[1])
        # If length is zero there is no angle
        if lenvector == 0:
            return -math.pi, 0
        # Normalize vector: v/||v||
        normalized = [vector[0] / lenvector, vector[1] / lenvector]
        dotprod = normalized[0] * self.refvec[0] + normalized[1] * self.refvec[1]  # x1*x2 + y1*y2
        diffprod = self.refvec[1] * normalized[0] - self.refvec[0] * normalized[1]  # x1*y2 - y1*x2
        angle = math.atan2(diffprod, dotprod)
        # Negative angles represent counter-clockwise angles so we need to subtract them
        # from 2*pi (360 degrees)
        if angle < 0:
            return 2 * math.pi + angle, lenvector
        # I return first the angle because that's the primary sorting criterium
        # but if two vectors have the same angle then the shorter distance should come first.
        return angle, lenvector



# = [Segment(Point2D(2,3), Point2D(5,2)),Segment(Point2D(4,1), Point2D(3,1)), Segment(Point2D(1,2),Point2D(2,1)), Segment(Point2D(3,1),Point2D(3,3))]
pts = [Point2D(2,3), Point2D(5,2), Point2D(4,1), Point2D(3,1), Point2D(1,2), Point2D(2,1), Point2D(3,1)]
v = Visibility_polygon_class()

print(pts)
print(sorted(pts, key=v.clockwiseangle_and_distance))