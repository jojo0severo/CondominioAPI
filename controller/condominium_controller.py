from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from setup import db
from sqlalchemy import exc


class CondominiumController:
    def __init__(self, system_session):
        self.system_session_key = system_session
        self.session_keys = {system_session}

    def get_condominium_by_id(self, condominium_id):
        return Condominium.query.get(condominium_id)

    def get_tower_by_id(self, tower_id):
        return Tower.query.get(tower_id)

    def get_apartment_by_id(self, apartment_id):
        return Apartment.query.get(apartment_id)

    def get_condominium_employees(self, condominium_id):
        cond = Condominium.query.get(condominium_id)
        if cond is not None:
            return cond.employees

        raise ReferenceError

    def get_condominium_rules(self, condominium_id):
        cond = Condominium.query.get(condominium_id)
        if cond is not None:
            return cond.rules

        raise ReferenceError

    def get_condominium_notifications(self, condominium_id):
        cond = Condominium.query.get(condominium_id)
        if cond is not None:
            return cond.notifications

        raise ReferenceError

    def get_condominium_event_types(self, condominium_id):
        cond = Condominium.query.get(condominium_id)
        if cond is not None:
            return cond.event_types

        raise ReferenceError

    def get_condominium_towers(self, session_key, condominium_id):
        if session_key not in self.session_keys:
            raise PermissionError

        cond = Condominium.query.get(condominium_id)
        if cond is not None:
            return cond.towers

        raise ValueError

    def get_tower_apartments(self, session_key, tower_id):
        if session_key not in self.session_keys:
            raise PermissionError

        tower = Tower.query.get(tower_id)
        if tower is not None:
            return tower.apartments

        raise ReferenceError

    def get_apartment_residents(self, session_key, apartment_id):
        if session_key not in self.session_keys:
            raise PermissionError

        apartment = Apartment.query.get(apartment_id)
        if apartment is not None:
            return apartment.residents

        raise ReferenceError

    def register_condominium(self, session_key, name, street_number, photo_location, address_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            condominium = Condominium(name=name, street_number=street_number, photo_location=photo_location, address_id=address_id)
            db.session.add(condominium)
            db.session.commit()

            return condominium

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def register_tower(self, session_key, name, condominium_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            tower = Tower(name=name, condominium_id=condominium_id)
            db.session.add(tower)
            db.session.commit()

            return tower

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def register_apartment(self, session_key, apt_number, tower_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            apartment = Apartment(apt_number=apt_number, tower_id=tower_id)
            db.session.add(apartment)
            db.session.commit()

            return apartment

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_condominium(self, session_key, condominium_id):
        if session_key not in self.session_keys:
            raise PermissionError

        condominium = Condominium.query.get(condominium_id)
        if condominium is not None:
            db.session.delete(condominium)
            db.session.commit()
            return True
        return False

    def remove_tower(self, session_key, tower_id):
        if session_key not in self.session_keys:
            raise PermissionError

        tower = Tower.query.get(tower_id)
        if tower is not None:
            db.session.delete(tower)
            db.session.commit()
            return True
        return False

    def remove_apartment(self, session_key, apartment_id):
        if session_key not in self.session_keys:
            raise PermissionError

        apartment = Apartment.query.get(apartment_id)
        if apartment is not None:
            db.session.delete(apartment)
            db.session.commit()
            return True
        return False

    def drop_session(self, session):
        if session not in self.session_keys or session == self.system_session_key:
            raise ValueError

        self.session_keys.remove(session)
        return True
