from setup import db


class Condominium(db.Model):
    __tablename__ = 'condominium'
    __table_args__ = (db.UniqueConstraint('street_number', 'address_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    photo_location = db.Column(db.String(200), nullable=True, default='data/photos/default/condominium.png')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id', ondelete='CASCADE'), nullable=False)

    address = db.relationship('Address', backref=db.backref('condominiums', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Condominium(id={self.id}, ' \
               f'condominium_name={self.name})'
