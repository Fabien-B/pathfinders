from typing import List, Tuple
from math import atan2, pi
from point import Point

class Polygon(list):
    NO = 0
    YES = 1
    COLLINEAR = 2
    COLLINEAR_THRESHOLD = 10**-5
    
    def get_tangent_points(self, pt:Point):
        def get_angle(ver):
            dx = ver.x - pt.x
            dy = ver.y - pt.y
            angle = atan2(dy, dx)
            return ver, angle
        
        angles = list(map(get_angle, self))    #type: List[Tuple[Point, float]]
        angles = sorted(angles, key=lambda elt:elt[1])           # tri croissant de la liste
        
        max_diff = 0
        index = 0
        for i in range(len(angles)):
            j = (i+1)%len(angles)
            diff = angles[j][1] - angles[i][1]
            if diff < 0:
                diff += 2*pi
            if diff > max_diff:
                max_diff = diff
                index = i
        ordonnated_list = angles[index + 1:] + angles[:index + 1]
        #print(ordonnated_list)
        return (ordonnated_list[0], ordonnated_list[-1])
    
    @staticmethod
    def segment_intersect(p11: Point, p12: Point, p21: Point, p22: Point) :
        # Convert vector 1 to a line (line 1) of infinite length.
        # We want the line in linear equation standard form: A*x + B*y + C = 0
        # See: http://en.wikipedia.org/wiki/Linear_equation
        
        v1x1, v1y1 = p11.x, p11.y
        v1x2, v1y2 = p12.x, p12.y
        v2x1, v2y1 = p21.x, p21.y
        v2x2, v2y2 = p22.x, p22.y
        
        a1 = v1y2 - v1y1
        b1 = v1x1 - v1x2
        c1 = (v1x2 * v1y1) - (v1x1 * v1y2)

        # Every point (x,y), that solves the equation above, is on the line,
        # every point that does not solve it, is not. The equation will have a
        # positive result if it is on one side of the line and a negative one 
        # if is on the other side of it. We insert (x1,y1) and (x2,y2) of vector
        # 2 into the equation above.
        d1 = (a1 * v2x1) + (b1 * v2y1) + c1
        d2 = (a1 * v2x2) + (b1 * v2y2) + c1

        # If d1 and d2 both have the same sign, they are both on the same side
        # of our line 1 and in that case no intersection is possible. Careful, 
        # 0 is a special case, that's why we don't test ">=" and "<=", 
        # but "<" and ">".
        if d1 > 0 and d2 > 0: return Polygon.NO
        if d1 < 0 and d2 < 0: return Polygon.NO

        # The fact that vector 2 intersected the infinite line 1 above doesn't 
        # mean it also intersects the vector 1. Vector 1 is only a subset of that
        # infinite line 1, so it may have intersected that line before the vector
        # started or after it ended. To know for sure, we have to repeat the
        # the same test the other way round. We start by calculating the 
        # infinite line 2 in linear equation standard form.
        a2 = v2y2 - v2y1
        b2 = v2x1 - v2x2
        c2 = (v2x2 * v2y1) - (v2x1 * v2y2)

        # Calculate d1 and d2 again, this time using points of vector 1.
        d1 = (a2 * v1x1) + (b2 * v1y1) + c2
        d2 = (a2 * v1x2) + (b2 * v1y2) + c2

        # Again, if both have the same sign (and neither one is 0),
        # no intersection is possible.
        if d1 > 0 and d2 > 0: return Polygon.NO
        if d1 < 0 and d2 < 0: return Polygon.NO

        # If we get here, only two possibilities are left. Either the two
        # vectors intersect in exactly one point or they are collinear, which
        # means they intersect in any number of points from zero to infinite.
        #if (a1 * b2) - (a2 * b1) == 0.0f: return COLLINEAR
        if abs((a1 * b2) - (a2 * b1)) < Polygon.COLLINEAR_THRESHOLD: return Polygon.COLLINEAR

        # If they are not collinear, they must intersect in exactly one point.
        return Polygon.YES
        
    def intersect(self, source_pt: Point, dest_pt: Point):
        nb_vertices = len(self)
        for v1,v2 in SegmentIterator(self):
            result = Polygon.segment_intersect(source_pt, dest_pt, v1, v2)
            if result == Polygon.COLLINEAR:
                print("Attention !")
            if result != Polygon.NO:        # may be better use result == YES
                return True
        return False


class SegmentIterator:
    def __init__(self, indexable):
        self.indexable = indexable
        self.i = 0
        self.max = len(indexable)

    def __iter__(self):
        return self

    def __next__(self):
        j = (self.i+1)%self.max
        if self.i >= self.max:
            raise StopIteration
        v1 = self.indexable[self.i]
        v2 = self.indexable[j]
        self.i += 1
        return (v1, v2)


   
