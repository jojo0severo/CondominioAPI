from setup import db


class Resident(db.Model):
    __tablename__ = 'resident'
    __table_args__ = (db.UniqueConstraint('cpf', 'apartment_id'), db.UniqueConstraint('photo_location'))

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    photo_location = db.Column(db.String(200), nullable=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment'), nullable=False)

    resident_users = db.relationship('ResidentUser', backref='resident', lazy=True, uselist=False)

    def __repr__(self):
        return f'Resident(id={self.id}, ' \
               f'name={self.name}, ' \
               f'birthday={self.birthday})'
