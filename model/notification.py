from setup import db


class Notification(db.Model):
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(50), nullable=False)
    text = db.Column(db.String(300), nullable=False)
    finish_date = db.Column(db.Date, nullable=True)
    condominium_id = db.Column(db.Integer, db.ForeignKey('condominium.id'), nullable=False)

    condominium = db.relationship('Condominium', backref='notifications', lazy=True)

    def __repr__(self):
        return f'Notification(id={self.id}, ' \
            f'type={self.type}, ' \
            f'title={self.title}, ' \
            f'text={self.text}, ' \
            f'finish_date={self.finish_date})'
