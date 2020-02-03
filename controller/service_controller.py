from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from model.service import Service
from setup import db
from sqlalchemy import exc, and_
from multiprocessing import Process
import datetime
import time


def clear_old_services():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Service.query.filter(Service.arrival > datetime.datetime.today()).delete()
        db.session.commit()
        time.sleep(3600 * 24 * 2)


class ServiceController:
    def __init__(self, system_session_key):
        self.system_session_key = system_session_key
        self.session_keys = {system_session_key}
        # Process(target=clear_old_services).start()

    def get_service_by_id(self, service_id):
        return Service.query.get(service_id)

    def get_service_by_date(self, condominium_id, start_datetime, end_datetime):
        return Condominium.query.filter_by(id=condominium_id)\
            .join(Tower)\
            .join(Apartment)\
            .join(Service)\
            .filter(and_(Service.arrival >= start_datetime, Service.arrival <= end_datetime))\
            .with_entities(Service.id, Service.name, Service.employee, Service.arrival, Service.apartment_id).all()

    def register_service(self, session_key, name, employee, arrival, apartment_id):
        if session_key not in self.session_keys:
            raise PermissionError

        try:
            arrival = datetime.datetime.strptime(arrival, '%Y-%m-%d %H:%M')
            service = Service(name=name, employee=employee, arrival=arrival, apartment_id=apartment_id)
            db.session.add(service)
            db.session.commit()

            return service

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_service(self, session_key, service_id):
        if session_key not in self.session_keys:
            raise PermissionError

        service = Service.query.get(service_id)
        if service is not None:
            db.session.delete(service)
            db.session.commit()
            return True
        return False

    def drop_session(self, session_key):
        if session_key not in self.session_keys or session_key == self.system_session_key:
            raise ValueError

        self.session_keys.remove(session_key)
        return True
