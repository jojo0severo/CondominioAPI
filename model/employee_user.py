from setup import db


class EmployeeUser(db.Model):
    __tablename__ = 'employeeuser'
    __table_args__ = (db.UniqueConstraint('employee_id'), db.UniqueConstraint('username'))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('username.username', ondelete='CASCADE'), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)

    employee = db.relationship('Employee', backref=db.backref('user', lazy=True, cascade='all, delete', uselist=False), lazy=False, uselist=False)
    _username = db.relationship('Username', backref=db.backref('employee_user', lazy=True, cascade='all, delete', uselist=False), lazy=True, uselist=False)

    def __repr__(self):
        return f'EmployeeUser(username={self.username})'
