from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from model.service import Service
from setup import db
from sqlalchemy import exc, and_
import datetime
import time


def clear_old_services():
    while datetime.datetime.now().hour != 1:
        time.sleep(30 * 60)

    while True:
        Service.query.filter(Service.arrival > datetime.datetime.today()).update({Service.active: 0})
        db.session.commit()
        time.sleep(3600 * 24 * 2)


class ServiceController:
    def get_service_by_id(self, service_id):
        return Service.query.filter(and_(Service.id == service_id, Service.active == 1))

    def get_service_by_date(self, condominium_id, start_datetime, end_datetime):
        return Condominium.query.filter_by(id=condominium_id)\
            .join(Tower)\
            .join(Apartment)\
            .join(Service)\
            .filter(and_(Service.arrival >= start_datetime, Service.arrival <= end_datetime, Service.active == 1))\
            .with_entities(Service.id, Service.name, Service.employee, Service.arrival, Service.apartment_id).all()

    def register_service(self, name, employee, arrival, apartment_id):
        try:
            arrival = datetime.datetime.strptime(arrival, '%Y-%m-%d %H:%M')
            service = Service(name=name, employee=employee, arrival=arrival, apartment_id=apartment_id)
            db.session.add(service)
            db.session.commit()

            return service.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_service(self, service):
        try:
            db.session.delete(service)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
