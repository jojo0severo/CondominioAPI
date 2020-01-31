from model.service import Service
from setup import db
from multiprocessing import Process
from sqlalchemy import exc, and_
import datetime
import time


def clear_old_services():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Service.query.filter(Service.arrival > datetime.datetime.today()).delete()
        db.session.commit()
        time.sleep(3600 * 24)


class ServiceController:
    def __init__(self, system_session):
        self.sessions = {system_session}
        Process(target=clear_old_services).start()

    def get_service_by_id(self, service_id):
        return Service.query.filter_by(id=service_id).first()

    def get_service_by_date(self, start_datetime, end_datetime):
        return Service.query.filter(and_(start_datetime <= Service.arrival <= end_datetime))

    def register_service(self, session, name, employee, arrival, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            service = Service(name=name, employee=employee, arrival=arrival, apartment_id=apartment_id)
            db.session.add(service)
            db.session.commit()

            return service

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_service(self, session, service_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Service.query.filter_by(service_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
