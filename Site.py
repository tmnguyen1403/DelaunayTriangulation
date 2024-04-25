from DebugUtils import generate_random_points
class Site:
    @staticmethod
    def generate_random_sites(num_sites, min_xy, max_xy):
        points = generate_random_points(num_sites,min_xy,max_xy)
        S = []
        for p in points:
            S.append(Site(p[0],p[1]))
        return S
    
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def equal(self,other):
        return self.x == other.x and self.y == other.y
    
    def plus(self,other):
        x = self.x + other.x
        y = self.y + other.y
        return Site(x,y)
    
    def minus(self,other):
        x = self.x - other.x
        y = self.y - other.y
        return Site(x,y)
    
    def divide_scalar(self,k):
        x = self.x / k
        y = self.y / k
        return Site(x,y)
    
    def mid(self,other):
        s = self.plus(other)
        s = s.divide_scalar(2)
        return s

    def minus(self,other):
        x = self.x - other.x
        y = self.y - other.y
        return Site(x,y)
    
    def debug(self):
        print(f"(x,y): ({self.x},{self.y})")
    
    def getXY(self):
        return (self.x,self.y)