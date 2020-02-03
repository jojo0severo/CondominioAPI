from setup import db


class EmployeeUser(db.Model):
    __tablename__ = 'employeeuser'
    __table_args__ = (db.UniqueConstraint('employee_id'),)

    username = db.Column(db.String(25), primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)

    employee = db.relationship('Employee', backref=db.backref('user', lazy=True, cascade='all, delete'), lazy=True, uselist=False)

    def __repr__(self):
        return f'EmployeeUser(username={self.username})'
