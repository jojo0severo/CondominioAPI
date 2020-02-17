from setup import db


class Notification(db.Model):
    __tablename__ = 'notification'
    __table_args__ = (
        db.UniqueConstraint('title', 'condominium_id'),
        db.Index('date_idx', 'finish_date'),
        db.Index('notification_idx', 'title', 'condominium_id')
    )

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    finish_date = db.Column(db.Date, nullable=True)
    active = db.Column(db.SmallInteger, default=1)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id', ondelete='CASCADE'), nullable=False)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id', ondelete='CASCADE'), nullable=False)

    author = db.relationship('Employee',
                             backref=db.backref('notifications',
                                                lazy=True,
                                                cascade='all, delete',
                                                primaryjoin='and_(Notification.employee_id == Employee.id, Notification.active == 1)'),
                             lazy=True)

    condominium = db.relationship('Condominium',
                                  backref=db.backref('notifications',
                                                     lazy=True,
                                                     cascade='all, delete',
                                                     primaryjoin='and_(Notification.condominium_id == Condominium.id, Notification.active == 1)'),
                                  lazy=True,
                                  primaryjoin='and_(Notification.condominium_id == Condominium.id, Condominium.active == 1)')

    def __repr__(self):
        return f'Notification(id={self.id}, ' \
               f'type={self.type}, ' \
               f'title={self.title}, ' \
               f'text={self.text}, ' \
               f'finish_date={self.finish_date})'
