from sympy import Line, Ray, Point, pi, Polygon, evalf, tan, atan, oo, Segment, intersection
#from pybst import avltree
from bintrees import FastAVLTree
import math
# from Lab1.DivideAndConquerConvexHull import rightmost_point_index, leftmost_point_index
# from Lab2.Smallest_rectangle import uppermost_point_index, lowermost_point_index
from Lab2.Smallest_circle import distance

# Global constants
START_VERTEX = 0
END_VERTEX = 1
DEFAULT_VERTEX = -1

# Event-Point class
class EventPoint(object):
    p = (0, 0)
    x = 0
    y = 0
    twin = 0
    status_segment = 0
    type = DEFAULT_VERTEX

    def __init__(self, p):
        self.p = p
        self.x = p[0]
        self.y = p[1]
        self.type = DEFAULT_VERTEX

# Status-Segment class
class StatusSegment(object):
    p1 = (0, 0)
    p2 = (0, 0)

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

# Main
class Visibility_polygon_class(object):

    def __init__(self):
        self.origin = (0, 0)
        self.refvec = (0, 1)
        self.segments = []
        self.event_queue = []
        self.status = 0
        self.status = FastAVLTree()
        self.visibility_polygon = []

    # Starts here!
    def get_visibility_polygon(self, segments, origin):
        self.origin = origin
        self.segments = segments
        self.add_bounding_box()
        self.create_event_queue_from_segments()
        self.sort_event_queue()
        self.initialize_status()
        self.perform_sweep()
        print(self.visibility_polygon)
        return self.visibility_polygon

    def add_bounding_box(self):
        # Find extreme points
        margin = 40
        top_y = 400 + margin #uppermost_point_index(self.event_queue)
        bottom_y = 130 - margin #lowermost_point_index(self.event_queue)
        right_x = 600 + margin #rightmost_point_index(self.event_queue)
        left_x = 200 - margin #leftmost_point_index(self.event_queue)
        # Create the bounding box and add it to event queue
        s1 = Segment(Point(right_x, top_y), Point(right_x, bottom_y))
        s2 = Segment(Point(right_x, bottom_y - 1), Point(left_x, bottom_y))
        s3 = Segment(Point(left_x, bottom_y + 1), Point(left_x, top_y))
        s4 = Segment(Point(left_x, top_y + 1), Point(right_x, top_y + 1))

        p = [s1, s2, s3, s4]
        self.segments.extend(p)

    # Create an event queue with all points and their connections (not sorted yet!)
    def create_event_queue_from_segments(self):
        for s in self.segments:
            p1 = EventPoint(s.p1)
            p2 = EventPoint(s.p2)
            p1.twin = p2
            p2.twin = p1
            self.event_queue.append(p1)
            self.event_queue.append(p2)

    # Create event queue
    def sort_event_queue(self):
        # Sort the points in clockwise order
        self.event_queue = sorted(self.event_queue, key=self.get_key)

    def initialize_status(self):
        sweep_ray = Ray(self.origin, self.event_queue[0].p)
        intersections = []
        for ep in self.event_queue:
            segment = Segment(ep.p, ep.twin.p)
            intersection_point = sweep_ray.intersection(segment)

            if len(intersection_point) > 0:
                intersections.extend(intersection_point)
                sorted_s = self.sort_one_segment_cw(segment)
                # If the segments first point is the current event-point
                if sorted_s.p1 == ep:
                    status_segment = StatusSegment(ep, ep.twin)
                    ep.status_segment = status_segment
                    ep.twin.status_segment = status_segment
                    ep.type = START_VERTEX
                    ep.twin.type = END_VERTEX
                    self.status.insert(distance(ep.p, self.origin), status_segment)
                    # If the segments second point is the current event-point
                else:
                    status_segment = StatusSegment(ep.twin, ep)
                    ep.status_segment = status_segment
                    ep.twin.status_segment = status_segment
                    ep.type = END_VERTEX
                    ep.twin.type = START_VERTEX
                    self.status.insert(distance(ep.twin.p, self.origin), status_segment)
            else:
                # Event-points not hit by the ray gets a type
                if ep.type == DEFAULT_VERTEX:
                    ep.type = START_VERTEX
                    ep.twin.type = END_VERTEX
        print(self.status)

    def perform_sweep(self):
        print(self.status.min_item())
        self.visibility_polygon.append(self.status.min_item()[1].p1)   # Add closest point in status to the visibility polygon


        for ep in self.event_queue[1:]:
            if ep.type == START_VERTEX:
                status_segment = StatusSegment(ep, ep.twin)
                ep.status_segment = status_segment
                ep.twin.status_segment = status_segment
                self.status.insert(distance(ep.p, self.origin), status_segment)
                #current_ray = Ray(self.origin, ep.p)
                self.visibility_polygon.append(self.status.min_item()[1].p1)

            elif ep.type == END_VERTEX:
                self.status.remove(distance(ep.status_segment.p1.p, self.origin))
                self.visibility_polygon.append(self.status.min_item()[1].p1)

    def sort_one_segment_cw(self, segment):
        points = sorted([segment.p1, segment.p2], key=self.clockwiseangle_and_distance)
        return Segment(points[0], points[1])

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
#pts = [Point(2,3), Point(5,2), Point(4,1), Point(3,1), Point(1,2), Point(2,1), Point(3,1)]
# = Visibility_polygon_class()

#print(pts)
#print(sorted(pts, key=v.clockwiseangle_and_distance))