from setup import db


class State(db.Model):
    __tablename__ = 'state'
    __table_args__ = (db.UniqueConstraint('name', 'country_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='CASCADE'), nullable=False)

    country = db.relationship('Country', backref=db.backref('states', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'State(id={self.id}, name={self.name})'
