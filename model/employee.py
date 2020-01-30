from setup import db


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = (db.UniqueConstraint('cpf', 'role', 'condominium_id'), db.UniqueConstraint('photo_location'))

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    photo_location = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    condominium = db.relationship('Condominium', backref='employee', lazy=True)

    def __repr__(self):
        return f'Employee(id={self.id}, ' \
            f'cpf={self.cpf}, ' \
            f'name={self.name}, ' \
            f'birthday={self.birthday}, ' \
            f'role={self.role})'
