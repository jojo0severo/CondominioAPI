from setup import db


class Country(db.Model):
    __tablename__ = 'country'
    __table_args__ = (db.UniqueConstraint('name'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f'Country(id={self.id}, name={self.name})'
