from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from setup import db
from sqlalchemy import exc, and_


class AddressController:
    def __init__(self, system_session_key):
        self.system_session_key = system_session_key

    def get_country_states(self, session_key, country_identifier):
        if session_key != self.system_session_key:
            raise PermissionError

        if isinstance(country_identifier, str):
            country = Country.query.filter_by(name=country_identifier).first()
        elif isinstance(country_identifier, int):
            country = Country.query.get(country_identifier)
        else:
            raise TypeError

        if country is not None:
            return country.states

        raise ReferenceError

    def get_state_cities(self, session_key, state_id):
        if session_key != self.system_session_key:
            raise PermissionError

        state = State.query.get(state_id)
        if state is not None:
            return state.cities

        raise ReferenceError

    def get_city_addresses(self, session_key, city_id):
        if session_key != self.system_session_key:
            raise PermissionError

        city = City.query.get(city_id)
        if city is not None:
            return city.addresses

        raise ReferenceError

    def get_address_by_id(self, session_key, address_id):
        if session_key != self.system_session_key:
            raise PermissionError

        return Address.query.filter_by(id=address_id).join(City).join(State).join(Country).first()

    def register_address_by_names(self, session_key, street_name, neighbourhood, city_name, state_name, country_name):
        if session_key != self.system_session_key:
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

    def remove_address_by_id(self, session_key, address_id):
        if session_key != self.system_session_key:
            raise PermissionError

        address = Address.query.get(address_id)
        if address is not None:
            db.session.delete(address)
            db.session.commit()
            return True
        return False
