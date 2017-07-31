from polygon import Polygon
from point import Point
from math import sqrt

MAX_RECURSION_DEPTH = 5

class Map(list):
    
    def get_obstacles(self, source: Point, dest: Point):
        found_paths = []
        def g(p, path):
            if len(path) > MAX_RECURSION_DEPTH:     #stop algo if recursion is too deep
                return
            poly = self.get_closest(p, dest)
            if poly is None:                #if the objective is reachable in straight line, we have a path !
                path += obj                 #if we want the objective in the path
                found_path.append(path)     #we could also stop the algo here, but it will not be the shortest path
            else:
                t1, t2 = poly.get_tangente(p)   # get the "tangent" polygon points on the left and right side
                g(t1, obj, path+t1)             # search path from these points to the objective while recording the path
                g(t2, obj, path+t2)

        g(dep, [dep])       # launch the search from the departure point. Initialise the path.

        return min(found_paths, key=lambda x : compute_lenght(x))  # on retourne le chemin le plus court parmi ceux trouvés    
    
    def get_closest(self, source, dest: Point):
        closest = None
        min_dist = float('inf')
        for poly in self:
            dist = poly.get_distance(source, dest)
            if dist is not None and dist < min_dist:
                min_dist = dist
                closest = poly
        return closest
    
    @staticmethod
    def compute_length(path):
        lenght = 0
        for i in range(len(path)-1):
            dx = path[i+1].x + path[i].x
            dy = path[i+1].y + path[i].y
            lenght += sqrt(dx**2 + dy **2)
        
