from model.apartment import Apartment
from setup import db
from sqlalchemy import exc, and_


class ApartmentController:
    def __init__(self, system_session):
        self.system_session = system_session
        self.sessions = {system_session}

    def get_apartment_by_id(self, apartment_id):
        return Apartment.query.filter_by(id=apartment_id).first()

    def get_apartment_by_name_and_tower_id(self, apt_number, tower_id):
        return Apartment.query.filter(and_(Apartment.apt_number == apt_number and Apartment.tower_id == tower_id)).first()

    def get_apartment_residents(self, session, apartment_id):
        if session != self.system_session:
            raise PermissionError

        apartment = Apartment.query.filter_by(id=apartment_id)
        if apartment is not None:
            return apartment.residents

        raise ValueError

    def register_apartment(self, session, apt_number, tower_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            apartment = Apartment(apt_number=apt_number, tower_id=tower_id)
            db.session.add(apartment)
            db.session.commit()

            return apartment

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_apartment(self, session, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Apartment.query.filter_by(id=apartment_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
