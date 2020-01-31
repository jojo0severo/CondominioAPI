from model.condominium import Condominium
from setup import db
from sqlalchemy import exc, and_


class CondominiumController:
    def __init__(self, system_session):
        self.sessions = {system_session}

    def get_condominium_by_id(self, condominium_id):
        return Condominium.query.filter_by(id=condominium_id).first()

    def get_condominium_by_name_and_address_id(self, condominium_name, address_id):
        return Condominium.query.filter(and_(Condominium.name == condominium_name, Condominium.address_id == address_id)).first()

    def get_condominium_rules(self, condominium_id):
        cond = Condominium.query.filter_by(id=condominium_id).first()
        if cond is not None:
            return cond.rules

        raise ValueError

    def get_condominium_notifications(self, condominium_id):
        cond = Condominium.query.filter_by(id=condominium_id).first()
        if cond is not None:
            return cond.notifications

        raise ValueError

    def get_condominium_event_types(self, condominium_id):
        cond = Condominium.query.filter_by(id=condominium_id).first()
        if cond is not None:
            return cond.event_types

        raise ValueError

    def get_condominium_towers(self, session, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        cond = Condominium.query.filter_by(id=condominium_id).first()
        if cond is not None:
            return cond.towers

        raise ValueError

    def register_condominium(self, session, name, street_number, photo_location, address_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            condominium = Condominium(name=name, street_number=street_number, photo_location=photo_location, address_id=address_id)
            db.session.add(condominium)
            db.session.commit()

            return condominium

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_condominium(self, session, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Condominium.query.filter_by(id=condominium_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
