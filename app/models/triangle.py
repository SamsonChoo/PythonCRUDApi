import math
from flask import url_for
from app import db


class Triangle(db.Model):
    """
    Create a Triangle table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'triangles'

    triangle_id = db.Column(db.Integer, primary_key=True)
    side1 = db.Column(db.Float)
    side2 = db.Column(db.Float)
    side3 = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    def __repr__(self):
        return '<Triangle: {} - {} - {}>'.format(self.side1, self.side2, self.side3)

    def get_area(self):
        halfPerimeter = (self.side1 + self.side2 + self.side3) / 2
        area = math.sqrt(halfPerimeter * (halfPerimeter - side1)
                         * (halfPerimeter - side2) * (halfPerimeter - side3))
        data = {'Area': area}
        return data

    def get_perimeter(self):
        perimeter = self.side1 + self.side2 + self.side3
        data = {'Perimeter': perimeter}
        return data

    def to_dict(self):
        data = {
            'triangle_id': self.triangle_id,
            'user_id': self.user_id,
            'side1': self.side1,
            'side2': self.side2,
            'side3': self.side3,
            '_links': {
                'owner': url_for('api.get_user_by_user_id', user_id=self.user_id),
                'self': url_for('api.get_triangle', triangle_id=self.triangle_id),
                'area': url_for('api.get_triangle_area', triangle_id=self.triangle_id),
                'perimeter': url_for('api.get_triangle_perimeter', triangle_id=self.triangle_id),
                'update': url_for('api.update_triangle', triangle_id=self.triangle_id),
                'delete': url_for('api.del_triangle', triangle_id=self.triangle_id)
            }
        }
        return data

    def from_dict(self, data, user_id):
        for field in ['side1', 'side2', 'side3']:
            if field in data and data[field]:
                setattr(self, field, data[field])
        self.user_id = user_id
