from setup import db


class City(db.Model):
    __tablename__ = 'city'
    __table_args__ = (db.UniqueConstraint('name', 'state_id'), db.Index('city_idx', 'name', 'state_id'))

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('state.id', ondelete='CASCADE'), nullable=False)

    state = db.relationship('State', backref=db.backref('cities', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'City(id={self.id}, name={self.name})'
