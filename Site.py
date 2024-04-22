#Saving the site
class Site:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def equal(self,other):
        return self.x == other.x and self.y == other.y
    
    def debug(self):
        print(f"(x,y): ({self.x},{self.y})")