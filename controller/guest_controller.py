from model.guest import Guest
from setup import db
from multiprocessing import Process
from sqlalchemy import exc, and_
import datetime
import time


def clear_old_guests():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Guest.query.filter(Guest.arrival > datetime.datetime.today()).delete()
        db.session.commit()
        time.sleep(3600 * 24)


class GuestController:
    def __init__(self, system_session):
        self.sessions = {system_session}
        Process(target=clear_old_guests).start()

    def get_guest_by_id(self, guest_id):
        return Guest.query.filter_by(id=guest_id).first()

    def get_guests_by_date(self, start_datetime, end_datetime):
        return Guest.query.filter(and_(start_datetime <= Guest.arrival <= end_datetime))

    def register_guest(self, session, name, arrival, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            guest = Guest(name=name, arrival=arrival, apartment_id=apartment_id)
            db.session.add(guest)
            db.session.commit()

            return guest

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_guest(self, session, guest_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Guest.query.filter_by(id=guest_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
