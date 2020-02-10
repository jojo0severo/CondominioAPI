from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from setup import db
from sqlalchemy import exc


class CondominiumController:
    def get_condominium_by_id(self, condominium_id):
        cond = Condominium.query.get(condominium_id)
        if not cond:
            raise ReferenceError

        return cond

    def get_tower_by_id(self, tower_id):
        tower = Tower.query.get(tower_id)
        if not tower:
            raise ReferenceError

        return tower

    def get_apartment_by_id(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if not apartment:
            raise ReferenceError

        return apartment

    def register_condominium(self, name, street_number, photo_location, address_id):
        try:
            condominium = Condominium(name=name, street_number=street_number, photo_location=photo_location, address_id=address_id)
            db.session.add(condominium)
            db.session.commit()

            return condominium.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def register_tower(self, name, condominium_id):
        try:
            tower = Tower(name=name, condominium_id=condominium_id)
            db.session.add(tower)
            db.session.commit()

            return tower.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def register_apartment(self, apt_number, tower_id):
        try:
            apartment = Apartment(apt_number=apt_number, tower_id=tower_id)
            db.session.add(apartment)
            db.session.commit()

            return apartment.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_condominium(self, condominium_id):
        condominium = Condominium.query.get(condominium_id)
        if not condominium:
            raise ReferenceError

        db.session.delete(condominium)
        db.session.commit()

    def remove_tower(self, tower_id):
        tower = Tower.query.get(tower_id)
        if not tower:
            raise ReferenceError

        db.session.delete(tower)
        db.session.commit()

    def remove_apartment(self, apartment_id):
        apartment = Apartment.query.get(apartment_id)
        if not apartment:
            raise ReferenceError

        db.session.delete(apartment)
        db.session.commit()
