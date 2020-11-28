class Rectangle:
    """Rectangle class"""
      
    def __init__(self, width, height):
        self.width = width
        self.height = height
          
    def __str__(self):
        """For printf() and str()"""
      
    def __repr__(self):
        """For repr() and interactive prompt"""
      
    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return (self.width + self.height) * 2

