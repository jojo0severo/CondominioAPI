from setup import db


class Service(db.Model):
    __tablename__ = 'service'
    __table_args__ = (
        db.UniqueConstraint('name', 'arrival', 'apartment_id'),
        db.Index('service_idx', 'name', 'arrival', 'apartment_id')
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    employee = db.Column(db.String(50), nullable=True)
    arrival = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.SmallInteger, default=1)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'), nullable=False)

    apartment = db.relationship('Apartment', backref=db.backref('services', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Service(id={self.id}, ' \
            f'service_name={self.name}, ' \
            f'employee_name={self.employee}, ' \
            f'arrival={self.arrival})'
