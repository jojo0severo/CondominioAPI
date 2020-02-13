from setup import db


class ResidentUser(db.Model):
    __tablename__ = 'residentuser'
    __table_args__ = (db.UniqueConstraint('resident_id'), db.UniqueConstraint('username'))

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), db.ForeignKey('username.username', ondelete='CASCADE'), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id', ondelete='CASCADE'), nullable=False)

    resident = db.relationship('Resident', backref=db.backref('user', lazy=True, cascade='all, delete', uselist=False), lazy=False, uselist=False)
    _username = db.relationship('Username', backref=db.backref('resident_user', lazy=True, cascade='all, delete', uselist=False), lazy=True, uselist=False)

    def __repr__(self):
        return f'ResidentUser(username={self.username})'
