from setup import db


class Apartment(db.Model):
    __tablename__ = 'apartment'
    __table_args__ = (db.UniqueConstraint('apt_number', 'tower_id'), db.Index('apt_idx', 'apt_number', 'tower_id'))

    id = db.Column(db.Integer, primary_key=True)
    apt_number = db.Column(db.Integer, nullable=False)
    tower_id = db.Column(db.Integer, db.ForeignKey('tower.id', ondelete='CASCADE'), nullable=False)
    active = db.Column(db.SmallInteger, default=1)

    tower = db.relationship('Tower',
                            backref=db.backref('apartments', lazy=True, cascade='all, delete'),
                            lazy=True,
                            primaryjoin='and_(Apartment.tower_id == Tower.id, Tower.active == 1)')

    def __repr__(self):
        return f'Apartment(id={self.id},' \
               f'apt_number={self.apt_number})'
