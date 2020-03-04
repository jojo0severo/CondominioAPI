from sqlalchemy import UniqueConstraint, Column, String
from setup import Base


class SuperUser(Base):
    __tablename__ = 'super_user'
    __table_args__ = (UniqueConstraint('username'), UniqueConstraint('password'))

    username = Column(String(100), primary_key=True)
    password = Column(String(200), nullable=False)

    def __repr__(self):
        return f'SuperUser(username={self.username})'
