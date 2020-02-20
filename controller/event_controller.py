from model.condominium import Condominium
from model.event_type import EventType
from model.event import Event
from setup import db
from sqlalchemy import exc, and_
import datetime


class EventController:
    def get_condominium_event_types(self, condominium_id):
        return EventType.query.join(Condominium).filter(Condominium.id == condominium_id).all()

    def get_condominium_events(self, start, end, condominium_id):
        start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
        end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')

        return Event.query.join(EventType).join(Condominium).filter(
            and_(Condominium.id == condominium_id, Event.start_datetime >= start, Event.end_datetime <= end, Event.active == 1)
        ).all()

    def register_event(self, start, end, event_type_id, apartment_id):
        try:
            start = datetime.datetime.strptime(start, '%Y-%m-%d %H:%M')
            end = datetime.datetime.strptime(end, '%Y-%m-%d %H:%M')
            event = Event(start_datetime=start, end_datetime=end, event_type_id=event_type_id, apartment_id=apartment_id)

            db.session.add(event)
            db.session.commit()

            return event.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_event(self, event):
        try:
            db.session.delete(event)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
