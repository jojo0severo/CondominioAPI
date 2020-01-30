from setup import db


class Condominium(db.Model):
    __tablename__ = 'condominium'
    __table_args__ = (db.UniqueConstraint('street_number', 'address_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)

    address = db.relationship('Address', backref='condominiums', lazy=True)

    def __repr__(self):
        return f'Condominium(id={self.id}, ' \
               f'condominium_name={self.name})'
