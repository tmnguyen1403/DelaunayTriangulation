from DebugUtils import generate_random_points,read_data_file
class Site:
    @staticmethod
    def generate_random_sites(num_sites, min_xy, max_xy):
        points = generate_random_points(num_sites,min_xy,max_xy)
        S = [Site.create_site(p) for p in points[:num_sites]]
        return S
    
    @staticmethod
    def create_site(p, precise=2):
        round_x,round_y = round(p[0],precise),round(p[1], precise)
        return Site(round_x,round_y)
    
    @staticmethod
    def generate_from_file(num_sites, data_file):
        points = read_data_file(data_file)
        S = [Site.create_site(p) for p in points[:num_sites]]
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