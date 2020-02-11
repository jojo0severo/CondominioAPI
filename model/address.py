from setup import db


class Address(db.Model):
    __tablename__ = 'address'
    __table_args__ = (db.UniqueConstraint('street_name', 'city_id'), db.Index('address_idx', 'street_name', 'city_id'))

    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(150), nullable=False)
    neighbourhood = db.Column(db.String(150), nullable=False)
    city_id = db.Column(db.String(60), db.ForeignKey('city.id', ondelete='CASCADE'), nullable=False)

    city = db.relationship('City', backref=db.backref('addresses', lazy=True, cascade='all, delete'), lazy=False)

    def __repr__(self):
        return f'Address(id={self.id}, ' \
               f'street_name={self.street_name}, ' \
               f'neighbourhood={self.neighbourhood}, ' \
               f'city_name={self.city.name})'
