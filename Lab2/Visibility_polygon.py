from sympy import Line, Ray, Point, pi, Polygon, evalf, tan, atan, oo, Segment, intersection
from sortedcontainers import SortedDict
import math

# Global constants
START_VERTEX = 0
END_VERTEX = 1
DEFAULT_VERTEX = -1

# Event-Point class
class EventPoint(object):


    def __init__(self, p):
        self.p = p
        self.x = p[0]
        self.y = p[1]
        self.type = DEFAULT_VERTEX
        self.status_segment = 0

# Status-Segment class
class StatusSegment(object):

    def __init__(self, p1, p2, origin):
        self.p1 = p1
        self.p2 = p2
        self.segment = Segment(p1.p, p2.p)
        self.current_distance = distance(p1.p, origin)

# Main



class Visibility_polygon_class(object):

    def __init__(self):
        self.origin = (0, 0)
        self.refvec = (0, 1)
        self.segments = []
        self.event_queue = []
        self.status = 0
        self.status = SortedDict()
        self.visibility_polygon = []

    def order_segments(self, arg):
        return arg

    # Starts here!
    def get_visibility_polygon(self, segments, origin):
        self.origin = origin
        self.segments = segments
        self.add_bounding_box()
        self.create_event_queue_from_segments()
        self.sort_event_queue()
        self.initialize_status()
        #return self.status
        self.perform_sweep()
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
        s2 = Segment(Point(right_x - 5, bottom_y), Point(left_x, bottom_y))
        s3 = Segment(Point(left_x, bottom_y + 5), Point(left_x, top_y))
        s4 = Segment(Point(left_x + 5, top_y), Point(right_x, top_y + 5))

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
        i = 0
        for ep in self.event_queue:
            if ep.type == DEFAULT_VERTEX:
                segment = Segment(ep.p, ep.twin.p)
                intersection_point = sweep_ray.intersection(segment)

                if len(intersection_point) > 0:
                    # If the segments first point is the current event-point
                    if intersection_point[0] == ep.p:   # if the point is on the initial ray
                        if len(Ray(self.origin, self.event_queue[i+1].p).intersection(segment)) > 0:    #if the point was a start point
                            self.initialize_segment(ep, intersection_point)
                        else:
                            self.initialize_segment(ep.twin, intersection_point)
                    else:
                        self.initialize_segment(ep.twin, intersection_point)
                else:
                    # Event-points not hit by the ray gets a type
                    ep.type = START_VERTEX
                    ep.twin.type = END_VERTEX
            i += 1

    def initialize_segment(self, ep, intersection_point):
        status_segment = StatusSegment(ep, ep.twin, self.origin)
        status_segment.current_distance = distance(intersection_point[0], self.origin)
        ep.status_segment = status_segment
        ep.twin.status_segment = status_segment
        ep.type = START_VERTEX
        ep.twin.type = END_VERTEX
        if ep != self.event_queue[0]:
            self.status.update({status_segment.current_distance: status_segment})

    def perform_sweep(self):
        print("\nStatus at start: " + str(len(self.status)))

        for ep in self.event_queue:
            print("\nStatus: " + str(len(self.status)))

            if ep.type == START_VERTEX:
                print("START_VERTEX")
                status_segment = StatusSegment(ep, ep.twin, self.origin)

                print("current segment: " + str(status_segment.segment) + str(status_segment.current_distance))

                ep.status_segment = status_segment
                ep.twin.status_segment = status_segment
                if self.status.__len__() == 0:
                    self.status.update({status_segment.current_distance: status_segment})
                    self.visibility_polygon.append(ep.p)
                    print("empty status. Append")
                else:
                    first_in_status = self.status.peekitem(index=0)

                    print("first in status and distance: " + str(first_in_status[1].segment) + ": " + str(
                        first_in_status[1].current_distance))

                    current_ray = Ray(self.origin, ep.p)
                    intersection_point = current_ray.intersection(first_in_status[1].segment)
                    first_in_status[1].current_distance = distance(intersection_point[0], self.origin)
                    print("First in status new distance: " + str( first_in_status[1].current_distance))
                    self.status.update({status_segment.current_distance: status_segment})     # insert the new segment to status
                    self.status.__delitem__(first_in_status[0])
                    self.status.update({first_in_status[1].current_distance: first_in_status[1]})    #update the key distance to the origin
                    new_first_in_status = self.status.peekitem(index=0)
                    if new_first_in_status[1] != first_in_status[1]:
                        self.visibility_polygon.append(intersection_point[0])
                        self.visibility_polygon.append(ep.p)
                        print("normal status. Append")

            elif ep.type == END_VERTEX:
                print("END_VERTEX")
                first_in_status = self.status.peekitem(index=0)
                print("first in status and distance: " + str(first_in_status[1].segment) + ": " + str(first_in_status[1].current_distance))
                self.status.__delitem__(ep.status_segment.current_distance)
                print("ep status segment and distance: " + str(ep.status_segment.segment) + ": " + str(ep.status_segment.current_distance))
                if self.status.__len__() == 0:
                    self.visibility_polygon.append(ep.p)
                    print("empty status. Append")
                else:
                    new_first_in_status = self.status.peekitem(index=0)
                    if new_first_in_status[1] != first_in_status[1]:
                        current_ray = Ray(self.origin, ep.p)
                        intersection_point = current_ray.intersection(new_first_in_status[1].segment)
                        self.visibility_polygon.append(ep.p)
                        self.visibility_polygon.append(intersection_point[0])
                        print("normal status. Append")

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

def distance(p1, p2):
    return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2

# = [Segment(Point2D(2,3), Point2D(5,2)),Segment(Point2D(4,1), Point2D(3,1)), Segment(Point2D(1,2),Point2D(2,1)), Segment(Point2D(3,1),Point2D(3,3))]
#pts = [Point(2,3), Point(5,2), Point(4,1), Point(3,1), Point(1,2), Point(2,1), Point(3,1)]
# = Visibility_polygon_class()

#print(pts)
#print(sorted(pts, key=v.clockwiseangle_and_distance))