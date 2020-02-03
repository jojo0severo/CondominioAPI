from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
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
        self.system_session = system_session
        self.sessions = {system_session}
        # Process(target=clear_old_guests).start()

    def get_guest_by_id(self, guest_id):
        return Guest.query.get(guest_id)

    def get_guests_by_date(self, condominium_id, start_datetime, end_datetime):
        return Condominium.query.filter_by(id=condominium_id) \
            .join(Tower) \
            .join(Apartment) \
            .join(Guest) \
            .filter(and_(Guest.arrival >= start_datetime, Guest.arrival <= end_datetime)) \
            .with_entities(Guest.id, Guest.name, Guest.arrival, Guest.apartment_id).all()

    def register_guest(self, session_key, name, arrival, apartment_id):
        if session_key not in self.sessions:
            raise PermissionError

        try:
            arrival = datetime.datetime.strptime(arrival, '%Y-%m-%d %H:%M')
            guest = Guest(name=name, arrival=arrival, apartment_id=apartment_id)
            db.session.add(guest)
            db.session.commit()

            return guest

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_guest(self, session_key, guest_id):
        if session_key not in self.sessions:
            raise PermissionError

        guest = Guest.query.get(guest_id)
        if guest:
            db.session.delete(guest)
            db.session.commit()
            return True
        return False

    def drop_session(self, session_key):
        if session_key not in self.sessions or session_key == self.system_session:
            raise ValueError

        self.sessions.remove(session_key)
        return True
