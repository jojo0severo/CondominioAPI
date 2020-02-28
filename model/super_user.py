from setup import db


class SuperUser(db.Model):
    __tablename__ = 'super_user'
    __table_args__ = (db.UniqueConstraint('username'), db.UniqueConstraint('password'))

    username = db.Column(db.String(100), primary_key=True)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'SuperUser(username={self.username})'
