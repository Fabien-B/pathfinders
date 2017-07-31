from polygon import Polygon
from point import Point

class Map(list):
    
    def get_obstacles(self, source: Point, dest: Point):
        poly = get_closest(source, dest)        #type: None or Polygon
        
    
    def get_closest(self, source, dest: Point):
        closest = None
        min_dist = float('inf')
        for poly in self:
            dist = poly.get_distance(source, dest)
            if dist is not None and dist < min_dist:
                min_dist = dist
                closest = poly
        return closest
