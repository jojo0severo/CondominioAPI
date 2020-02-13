from setup import db


class Event(db.Model):
    __tablename__ = 'event'
    __table_args__ = (
        db.UniqueConstraint('event_type_id', 'start_datetime', 'end_datetime'),
        db.Index('event_idx', 'event_type_id', 'start_datetime', 'end_datetime')
    )

    id = db.Column(db.Integer, primary_key=True)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.SmallInteger, default=1)
    event_type_id = db.Column(db.Integer, db.ForeignKey('eventtype.id', ondelete='CASCADE'), nullable=False)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id', ondelete='CASCADE'), nullable=False)

    apartment = db.relationship('Apartment', backref=db.backref('events', lazy=True, cascade='all, delete'), lazy=True)
    event_type = db.relationship('EventType', backref=db.backref('events', lazy=True, cascade='all, delete'), lazy=True)

    def __repr__(self):
        return f'Event(id={self.id}, ' \
            f'start_datetime={self.start_datetime}, ' \
            f'end_datetime={self.end_datetime})'
