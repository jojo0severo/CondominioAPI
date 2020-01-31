from model.tower import Tower
from setup import db
from sqlalchemy import exc, and_


class TowerController:
    def __init__(self, system_sessions):
        self.sessions = {system_sessions}

    def get_tower_by_id(self, tower_id):
        return Tower.query.filter_by(id=tower_id).first()

    def get_tower_by_name_and_condominium_id(self, tower_name, condominium_id):
        return Tower.query.filter(and_(Tower.name == tower_name, Tower.condominium_id == condominium_id)).first()

    def get_tower_apartments(self, session, tower_id):
        if session not in self.sessions:
            raise PermissionError

        tower = Tower.query.filter_by(id=tower_id).first()
        if tower is not None:
            return tower.apartments

        raise ValueError

    def register_tower(self, session, name, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            tower = Tower(name=name, condominium_id=condominium_id)
            db.session.add(tower)
            db.session.commit()

            return tower

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_tower(self, session, tower_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Tower.query.filter_by(id=tower_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
