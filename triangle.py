import math

class Triangle:
    """Triangle class"""
      
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
  
    def __str__(self):
        """For printf() and str()"""
      
    def __repr__(self):
        """For repr() and interactive prompt"""
      
    def get_area(self):
        halfPerimeter = (self.side1 + self.side2 + self.side3) / 2
        area = math.sqrt(halfPerimeter * (halfPerimeter - side1) * (halfPerimeter - side2) * (halfPerimeter - side3))
        return area

    def get_perimeter(self):
        return self.side1 + self.side2 + self.side3

