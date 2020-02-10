from setup import db


class Guest(db.Model):
    __tablename__ = 'guest'
    __table_args__ = (
        db.UniqueConstraint('name', 'arrival', 'apartment_id'),
        db.Index('guest_idx', 'name', 'arrival', 'apartment_id')
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'), nullable=False)

    apartment = db.relationship('Apartment', backref=db.backref('guests', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Guest(id={self.id}, name={self.name}, arrival={self.arrival})'
