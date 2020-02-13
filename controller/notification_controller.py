from model.notification import Notification
from setup import db
from sqlalchemy import exc, and_
import datetime
import time


def clear_old_notifications():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Notification.query.filter(Notification.finish_date > datetime.datetime.today()).update({Notification.active: 0})
        db.session.commit()
        time.sleep(3600 * 24 * 2)


class NotificationController:
    def get_notification_by_id(self, notification_id):
        return Notification.query.filter(and_(Notification.id == notification_id, Notification.active == 1))

    def register_notification(self, noti_type, title, text, finish_date, condominium_id):
        try:
            finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d')
            notification = Notification(type=noti_type, title=title, text=text, finish_date=finish_date, condominium_id=condominium_id)
            db.session.add(notification)
            db.session.commit()

            return notification.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_notification(self, notification):
        try:
            db.session.delete(notification)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
