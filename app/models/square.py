from flask import url_for
from .rectangle import Rectangle


class Square(Rectangle):
    def __repr__(self):
        return '<Square: {} x {}>'.format(self.length, self.width)

    def to_dict(self):
        data = {
            'square_id': self.rectangle_id,
            'user_id': self.user_id,
            'length': self.length,
            '_links': {
                'owner': url_for('api.get_user_by_user_id', user_id=self.user_id),
                'self': url_for('api.get_square', rectangle_id=self.rectangle_id),
                'area': url_for('api.get_square_area', rectangle_id=self.rectangle_id),
                'perimeter': url_for('api.get_square_perimeter', rectangle_id=self.rectangle_id)
            }
        }
        return data

    def from_dict(self, data, user_id):
        self.length = data['length']
        self.width = data['length']
        self.user_id = user_id
