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
        time.sleep(3600 * 24 * 2)


class NotificationController:
    def __init__(self, system_session_key):
        self.system_session_key = system_session_key
        self.session_keys = {system_session_key}
        # Process(target=clear_old_notifications).start()

    def get_notification_by_id(self, notification_id):
        return Notification.query.get(notification_id)

    def register_notification(self, session_key, noti_type, title, text, finish_date, condominium_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            finish_date = datetime.datetime.strptime(finish_date, '%Y-%m-%d')
            notification = Notification(type=noti_type, title=title, text=text, finish_date=finish_date, condominium_id=condominium_id)
            db.session.add(notification)
            db.session.commit()

            return notification

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_notification(self, session_key, notification_id):
        if session_key not in self.session_keys:
            raise PermissionError

        notification = Notification.query.get(notification_id)
        if notification is not None:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    def drop_session(self, session_key):
        if session_key not in self.session_keys or session_key == self.system_session_key:
            raise ValueError

        self.session_keys.remove(session_key)
        return True
