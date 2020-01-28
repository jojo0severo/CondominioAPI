from setup import db


class State(db.Model):
    __tablename__ = 'state'
    __table_args__ = (db.UniqueConstraint('state_name', 'country_id'),)

    id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(60), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)

    cities = db.relationship('City', backref='state', lazy=True)

    def __repr__(self):
        return f'State(id={self.id}, ' \
               f'state_name={self.state_name})'
