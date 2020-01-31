from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from setup import db
from sqlalchemy import exc, and_


class AddressController:
    def __init__(self, system_session):
        self.system_session = system_session
        self.sessions = {system_session}

    def get_country_states(self, session, country_identifier):
        if session not in self.sessions:
            raise PermissionError

        if isinstance(country_identifier, str):
            return Country.query.filter_by(name=country_identifier).first().states
        elif isinstance(country_identifier, int):
            return Country.query.filter_by(id=country_identifier).first().states
        else:
            raise TypeError

    def get_state_cities(self, session, state_id):
        if session not in self.sessions:
            raise PermissionError

        return State.query.filter_by(id=state_id).first().cities

    def get_city_addresses(self, session, city_id):
        if session not in self.sessions:
            raise PermissionError

        return City.query.filter_by(id=city_id).first().addresses

    def get_address_by_id(self, address_id):
        return Address.query.filter_by(id=address_id).first()

    def get_address_by_names(self, street_name, city_name, state_name, country_name):
        return Address.query.filter_by(street_name=street_name) \
            .join(City).filter_by(name=city_name) \
            .join(State).filter_by(name=state_name) \
            .join(Country).filter_by(name=country_name).first()

    def register_address_by_names(self, session, street_name, neighbourhood, city_name, state_name, country_name):
        if session not in self.sessions:
            raise PermissionError

        try:
            country = Country(name=country_name)
            db.session.add(country)
            db.session.commit()

        except exc.IntegrityError:
            db.session.rollback()
            country = Country.query.filter_by(name=country_name).first()

        try:
            state = State(name=state_name, country_id=country.id)
            db.session.add(state)
            db.session.commit()

        except exc.IntegrityError:
            db.session.rollback()
            state = State.query.filter(and_(State.name == state_name, State.country_id == country.id)).first()

        try:
            city = City(name=city_name, state_id=state.id)
            db.session.add(city)
            db.session.flush()

        except exc.IntegrityError:
            db.session.rollback()
            city = City.query.filter(and_(City.name == city_name, City.state_id == state.id)).first()

        try:
            address = Address(street_name=street_name, neighbourhood=neighbourhood, city_id=city.id)
            db.session.add(address)
            db.session.commit()

            return address

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_address_by_id(self, session, address_id):
        if session != self.system_session:
            raise PermissionError

        deleted = Address.query.filter_by(id=address_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False
