from setup import db


class Tower(db.Model):
    __tablename__ = 'tower'
    __table_args__ = (db.UniqueConstraint('name', 'condominium_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id', ondelete='CASCADE'), nullable=False)

    condominium = db.relationship('Condominium', backref=db.backref('towers', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Tower(id={self.id}, ' \
               f'tower_name={self.name})'
