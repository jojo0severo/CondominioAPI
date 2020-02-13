from setup import db


class Username(db.Model):
    __tablename__ = 'username'

    username = db.Column(db.String(30), primary_key=True)
