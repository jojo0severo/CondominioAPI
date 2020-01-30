from setup import db


class Service(db.Model):
    __tablename__ = 'service'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    employee = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.DateTime, nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)

    apartment = db.relationship('Apartment', backref='services', lazy=True)

    def __repr__(self):
        return f'Service(id={self.id}, ' \
            f'service_name={self.name}, ' \
            f'employee_name={self.employee}, ' \
            f'arrival={self.arrival})'
