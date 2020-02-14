from setup import db


class Condominium(db.Model):
    __tablename__ = 'condominium'
    __table_args__ = (db.UniqueConstraint('street_number', 'address_id'), db.Index('cond_idx', 'street_number', 'address_id'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    street_number = db.Column(db.Integer, nullable=False)
    photo_location = db.Column(db.String(200), nullable=True, default='data/photos/default/condominium.png')
    address_id = db.Column(db.Integer, db.ForeignKey('address.id', ondelete='CASCADE'), nullable=False)
    active = db.Column(db.SmallInteger, default=1)

    address = db.relationship('Address',
                              backref=db.backref('condominiums',
                                                 lazy=True,
                                                 cascade='all, delete',
                                                 primaryjoin='and_(Address.id == Condominium.address_id, Condominium.active == 1)'),
                              lazy=True,
                              primaryjoin='and_(Condominium.address_id == Address.id, Condominium.active == 1)')

    def __repr__(self):
        return f'Condominium(id={self.id}, ' \
               f'condominium_name={self.name})'
