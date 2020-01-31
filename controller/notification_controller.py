from model.notification import Notification
from setup import db
from multiprocessing import Process
from sqlalchemy import exc
import datetime
import time


def clear_old_notifications():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Notification.query.filter(Notification.finish_date > datetime.datetime.today()).delete()
        db.session.commit()
        time.sleep(3600 * 24)


class NotificationController:
    def __init__(self, system_session):
        self.sessions = {system_session}
        Process(target=clear_old_notifications).start()

    def get_notification_by_id(self, notification_id):
        return Notification.query.filter_by(id=notification_id).first()

    def register_notification(self, session, noti_type, title, text, finish_date, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            notification = Notification(type=noti_type, title=title, text=text, finish_date=finish_date, condominium_id=condominium_id)
            db.session.add(notification)
            db.session.commit()

            return notification

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_notification(self, session, notification_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Notification.query.filter_by(id=notification_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
