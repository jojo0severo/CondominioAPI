from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from setup import db
from sqlalchemy import exc


class CondominiumController:
    def get_condominium_by_id(self, condominium_id):
        return Condominium.query.get(condominium_id)

    def get_tower_by_id(self, tower_id):
        return Tower.query.get(tower_id)

    def get_apartment_by_id(self, apartment_id):
        return Apartment.query.get(apartment_id)

    def get_apartment_residents_by_condominium_id_and_apt_number(self, condominium_id, apartment_number):
        return Apartment.query.filter(Apartment.apt_number == apartment_number).join(Tower).join(Condominium).filter(Condominium.id == condominium_id).first().residents

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

    def remove_condominium(self, condominium):
        try:
            db.session.delete(condominium)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_tower(self, tower):
        try:
            db.session.delete(tower)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_apartment(self, apartment):
        try:
            db.session.delete(apartment)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
