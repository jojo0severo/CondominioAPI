from setup import db


class Rule(db.Model):
    __tablename__ = 'rule'
    __table_args = (
        db.UniqueConstraint('text', 'condominium_id'),
        db.Index('rule_idx', 'text')
    )

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id', ondelete='CASCADE'), nullable=False)

    author = db.relationship('Employee',
                             backref=db.backref('rules', lazy=True, cascade='all, delete'),
                             lazy=False)

    condominium = db.relationship('Condominium',
                                  backref=db.backref('rules', lazy=True, cascade='all, delete'),
                                  lazy=True,
                                  primaryjoin='and_(Rule.condominium_id == Condominium.id, Condominium.active == 1)')

    def __repr__(self):
        return f'Rule(text={self.text})'
