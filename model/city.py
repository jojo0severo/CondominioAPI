from setup import db


class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = (db.UniqueConstraint('city_name', 'state_id'),)
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(60), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state'), nullable=False)

    addresses = db.relationship('Address', backref='city', lazy=True)

    def __repr__(self):
        return f'City(id={self.id}, ' \
               f'city_name={self.city_name})'
