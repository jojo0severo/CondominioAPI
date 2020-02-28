from setup import db


class ResidentUser(db.Model):
    __tablename__ = 'resident_user'
    __table_args__ = (db.UniqueConstraint('apartment_id'), db.UniqueConstraint('username'))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('username.username', ondelete='CASCADE'), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'), nullable=False)

    apartment = db.relationship('Apartment',
                                backref=db.backref('user', lazy=True, cascade='all, delete', uselist=False),
                                lazy=True,
                                uselist=False,
                                primaryjoin='and_(ResidentUser.apartment_id == Apartment.id, Apartment.active == 1)')

    _username = db.relationship('Username',
                                backref=db.backref('resident_user', lazy=True, cascade='all, delete', uselist=False),
                                lazy=True,
                                uselist=False)

    def __repr__(self):
        return f'ResidentUser(username={self.username})'
