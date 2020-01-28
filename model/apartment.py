from setup import db


class Apartment(db.Model):
    __tablename__ = 'apartment'
    __table_args__ = (db.UniqueConstraint('apt_number', 'tower_id'),)

    id = db.Column(db.Integer, primary_key=True)
    apt_number = db.Column(db.Integer, nullable=False)
    tower_id = db.Column(db.Integer, db.ForeignKey('tower'), nullable=False)

    residents = db.relationship('Resident', backref='apartment', lazy=True)

    def __repr__(self):
        return f'Apartment(id={self.id},' \
               f'apt_number={self.apt_number})'
