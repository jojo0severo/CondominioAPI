from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from model.guest import Guest
from setup import db
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
    def get_guest_by_id(self, guest_id):
        guest = Guest.query.get(guest_id)
        if not guest:
            raise ReferenceError

        return guest

    def get_guests_by_date(self, condominium_id, start_datetime, end_datetime):
        guests = Condominium.query.filter_by(id=condominium_id) \
            .join(Tower) \
            .join(Apartment) \
            .join(Guest) \
            .filter(and_(Guest.arrival >= start_datetime, Guest.arrival <= end_datetime)) \
            .with_entities(Guest.id, Guest.name, Guest.arrival, Guest.apartment_id).all()

        if not guests:
            raise ReferenceError

        return guests

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

    def remove_guest(self, guest_id):
        guest = Guest.query.get(guest_id)
        if not guest:
            raise ReferenceError

        db.session.delete(guest)
        db.session.commit()
