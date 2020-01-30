from setup import db


class EventType(db.Model):
    __tablename__ = 'eventtype'
    __table_args__ = (db.UniqueConstraint('name', 'condominium_id'),)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    condominium = db.relationship('Condominium', backref='event_types', lazy=True)

    def __repr__(self):
        return f'EventType(id={self.id}, name={self.name})'
