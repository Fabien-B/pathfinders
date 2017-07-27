from typing import List, Tuple
from math import atan2, pi
from point import Point

class Polygon:
    
    def __init__(self, point_list: List[Point]):
        self.vertices = point_list
    
    def get_tangent_points(self, pt:Point):
        def get_angle(ver):
            dx = ver.x - pt.x
            dy = ver.y - pt.y
            angle = atan2(dy, dx)
            return ver, angle
        
        angles = list(map(get_angle, self.vertices))    #type: List[Tuple[Point, float]]
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
        print(ordonnated_list)
        return (ordonnated_list[0], ordonnated_list[-1])
