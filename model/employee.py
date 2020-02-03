from setup import db


class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = (db.UniqueConstraint('cpf', 'role', 'condominium_id'), db.UniqueConstraint('photo_location'))

    id = db.Column(db.Integer, primary_key=True)
    cpf = db.Column(db.String(11), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    photo_location = db.Column(db.String(200), nullable=True, default='data/photos/default/employee.png')
    role = db.Column(db.String(50), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id', ondelete='CASCADE'), nullable=False)

    condominium = db.relationship('Condominium', backref=db.backref('employees', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Employee(id={self.id}, ' \
            f'cpf={self.cpf}, ' \
            f'name={self.name}, ' \
            f'birthday={self.birthday}, ' \
            f'role={self.role})'
