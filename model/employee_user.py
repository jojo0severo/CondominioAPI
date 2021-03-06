from setup import db


class EmployeeUser(db.Model):
    __tablename__ = 'employee_user'
    __table_args__ = (db.UniqueConstraint('employee_id'), db.UniqueConstraint('username'))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), db.ForeignKey('username.username', ondelete='CASCADE'), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)

    employee = db.relationship('Employee',
                               backref=db.backref('user', lazy=True, cascade='all, delete', uselist=False),
                               lazy=False,
                               uselist=False,
                               primaryjoin='and_(EmployeeUser.employee_id == Employee.id, Employee.active == 1)')

    _username = db.relationship('Username',
                                backref=db.backref('employee_user', lazy=True, cascade='all, delete', uselist=False),
                                lazy=True,
                                uselist=False)

    def __repr__(self):
        return f'EmployeeUser(username={self.username})'
