from setup import db


class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = (db.UniqueConstraint('country_name'),)

    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(40), nullable=False)

    states = db.relationship('State', backref='country', lazy=True)

    def __repr__(self):
        return f'Country(id={self.id}, ' \
               f'country_name={self.country_name})'
