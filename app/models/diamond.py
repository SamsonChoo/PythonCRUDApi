# import math

# class Diamond:
#     """Diamond class, assuming diamond to have the same properties as a Rhombus"""

#     def __init__(self, diagonal1, diagonal2):
#         self.diagonal1 = diagonal1
#         self.diagonal2 = diagonal2

#     def __str__(self):
#         """For printf() and str()"""

#     def __repr__(self):
#         """For repr() and interactive prompt"""

#     def get_area(self):
#         return self.diagonal1 * self.diagonal2 / 2

#     def get_perimeter(self):
#         area = 2 * math.sqrt(self.diagonal1 ** 2 + self.diagonal2 ** 2)
#         return area
import math
from app import db
from flask import url_for


class Diamond(db.Model):
    """
    Create a Diamond table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'diamonds'

    diamond_id = db.Column(db.Integer, primary_key=True)
    diagonal1 = db.Column(db.Float)
    diagonal2 = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    def __repr__(self):
        return '<Diamond: {} x {}>'.format(self.diagonal1, self.diagonal2)

    def get_area(self):
        area = self.diagonal1 * self.diagonal2 / 2
        data = {'Area': area}
        return data

    def get_perimeter(self):
        perimeter = 2 * math.sqrt(self.diagonal1 ** 2 + self.diagonal2 ** 2)
        data = {'Perimeter': perimeter}
        return data

    def to_dict(self):
        data = {
            'diamond_id': self.diamond_id,
            'user_id': self.user_id,
            'diagonal1': self.diagonal1,
            'diagonal2': self.diagonal2,
            '_links': {
                'owner': url_for('api.get_user_by_user_id', user_id=self.user_id),
                'self': url_for('api.get_diamond', diamond_id=self.diamond_id),
                'area': url_for('api.get_diamond_area', diamond_id=self.diamond_id),
                'perimeter': url_for('api.get_diamond_perimeter', diamond_id=self.diamond_id),
                'update': url_for('api.update_diamond', diamond_id=self.diamond_id),
                'delete': url_for('api.del_diamond', diamond_id=self.diamond_id)
            }
        }
        return data

    def from_dict(self, data, user_id):
        for field in ['diagonal1', 'diagonal2']:
            if field in data and data[field]:
                setattr(self, field, data[field])
        self.user_id = user_id
