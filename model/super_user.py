from setup import db


class SuperUser(db.Model):
    __tablename__ = 'superuser'

    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'SuperUser()'
