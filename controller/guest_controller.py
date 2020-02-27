from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from model.guest import Guest
from setup import db
from sqlalchemy import exc, and_
from multiprocessing import Process
import datetime
import time


def clear_old_guests():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Guest.query.filter(Guest.arrival > datetime.datetime.today()).update({Guest.active: 0})
        db.session.commit()
        time.sleep(3600 * 24)


class GuestController:
    def __init__(self):
        Process(target=clear_old_guests).start()

    def get_guest_by_id(self, guest_id):
        return Guest.query.filter(and_(Guest.id == guest_id, Guest.active == 1))

    def get_guests_by_date(self, condominium_id, start_datetime, end_datetime):
        return Condominium.query.filter_by(id=condominium_id) \
            .join(Tower) \
            .join(Apartment) \
            .join(Guest) \
            .filter(and_(Guest.arrival >= start_datetime, Guest.arrival <= end_datetime, Guest.active == 1)) \
            .with_entities(Guest.id, Guest.name, Guest.arrival, Guest.apartment_id).all()

    def register_guest(self, name, arrival, apartment_id):
        try:
            arrival = datetime.datetime.strptime(arrival, '%Y-%m-%d %H:%M')
            guest = Guest(name=name, arrival=arrival, apartment_id=apartment_id)
            db.session.add(guest)
            db.session.commit()

            return guest.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_guest(self, guest):
        try:
            db.session.delete(guest)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
