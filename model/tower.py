from setup import db


class Tower(db.Model):
    __tablename__ = 'tower'
    __table_args__ = (db.UniqueConstraint('tower_name', 'condominium_id'),)

    id = db.Column(db.Integer, primary_key=True)
    tower_name = db.Column(db.String(10), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    apartments = db.relationship('Apartment', backref='tower', lazy=True)

    def __repr__(self):
        return f'Tower(id={self.id}, ' \
               f'tower_name={self.tower_name})'
