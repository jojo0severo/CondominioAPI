from setup import db


class Guest(db.Model):
    __tablename__ = 'guest'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)

    apartment = db.relationship('Apartment', backref='guests', lazy=True)

    def __repr__(self):
        return f'Guest(id={self.id}, name={self.name}, arrival={self.arrival})'
