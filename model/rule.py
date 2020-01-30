from setup import db


class Rule(db.Model):
    __tablename__ = 'rule'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    condominium = db.relationship('Condominium', backref='rules', lazy=True)

    def __repr__(self):
        return f'Rule(text={self.text})'
