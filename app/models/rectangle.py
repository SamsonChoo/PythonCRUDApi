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
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'users.user_id'), nullable=False)

    def __repr__(self):
        return '<Rectangle: {} x {}>'.format(self.length, self.width)

    def get_area(self):
        return self.length * self.width

    def get_perimeter(self):
        return (self.length + self.width) * 2

    def to_dict(self):
        data = {
            'rectangle_id': self.rectangle_id,
            'user_id': self.user_id,
            'length': self.length,
            'width': self.width
            # '_links': {
            #     'self_by_user_name': url_for('api.get_user_by_user_name', user_name=self.user_name),
            #     'self_by_id': url_for('api.get_user_by_id', user_id=self.user_id)
            # }
        }
        return data
