from setup import db


class Tower(db.Model):
    __tablename__ = 'tower'
    __table_args__ = (db.UniqueConstraint('name', 'condominium_id'), db.Index('tower_idx', 'name', 'condominium_id'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id', ondelete='CASCADE'), nullable=False)
    active = db.Column(db.SmallInteger, default=1)

    condominium = db.relationship('Condominium',
                                  backref=db.backref('towers', lazy=True, cascade='all, delete'),
                                  lazy=True,
                                  primaryjoin='and_(Tower.condominium_id == Condominium.id, Condominium.active == 1)')

    def __repr__(self):
        return f'Tower(id={self.id}, ' \
               f'tower_name={self.name})'
