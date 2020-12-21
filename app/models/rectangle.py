from app import db
from flask import url_for


class Rectangle(db.Model):
    """
    Create a Rectangle table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'rectangles'

    rectangle_id = db.Column(db.Integer, primary_key=True)
    length = db.Column(db.Float)
    width = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    def __init__(self, length=None, width=None, user_id=None):
        self.length = length
        self.width = width
        self.user_id = user_id

    def __repr__(self):
        return '<Rectangle: {} x {}>'.format(self.length, self.width)

    def get_area(self):
        area = self.length * self.width
        data = {'Area': area}
        return data

    def get_perimeter(self):
        perimeter = (self.length + self.width) * 2
        data = {'Perimeter': perimeter}
        return data

    def to_dict(self):
        data = {
            'rectangle_id': self.rectangle_id,
            'user_id': self.user_id,
            'length': self.length,
            'width': self.width,
            '_links': {
                'owner': url_for('api.get_user_by_user_id', user_id=self.user_id),
                'self': url_for('api.get_rectangle', rectangle_id=self.rectangle_id),
                'area': url_for('api.get_rectangle_area', rectangle_id=self.rectangle_id),
                'perimeter': url_for('api.get_rectangle_perimeter', rectangle_id=self.rectangle_id),
                'update': url_for('api.update_rectangle', rectangle_id=self.rectangle_id),
                'delete': url_for('api.del_rectangle', rectangle_id=self.rectangle_id)
            }
        }
        return data

    def from_dict(self, data, user_id):
        for field in ['length', 'width']:
            if field in data and data[field]:
                setattr(self, field, data[field])
        self.user_id = user_id
