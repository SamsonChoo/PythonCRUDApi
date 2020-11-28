import math

class Diamond:
    """Diamond class, assuming diamond to have the same properties as a Rhombus"""
      
    def __init__(self, diagonal1, diagonal2):
        self.diagonal1 = diagonal1
        self.diagonal2 = diagonal2
          
    def __str__(self):
        """For printf() and str()"""
      
    def __repr__(self):
        """For repr() and interactive prompt"""
      
    def get_area(self):
        return self.diagonal1 * self.diagonal2 / 2

    def get_perimeter(self):
        area = 2 * math.sqrt(self.diagonal1 ** 2 + self.diagonal2 ** 2)
        return area

