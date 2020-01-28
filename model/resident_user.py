from setup import db


class ResidentUser(db.Model):
    __tablename__ = 'residentuser'
    __table_args__ = (db.UniqueConstraint('resident_id'))

    username = db.Column(db.String(25), primary_key=True)
    password = db.Column(db.String(30), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident'), nullable=False)

    def __repr__(self):
        return f'ResidentUser(username={self.username})'