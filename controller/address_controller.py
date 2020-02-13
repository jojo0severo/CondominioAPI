from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from setup import db
from sqlalchemy import exc, and_


class AddressController:
    def get_country_states(self, country_identifier):
        if isinstance(country_identifier, str):
            return Country.query.filter_by(name=country_identifier).first().states
        elif isinstance(country_identifier, int):
            return Country.query.get(country_identifier).states
        else:
            raise ValueError(f'country_identifier: {type(country_identifier)}')

    def get_state_cities(self, state_id):
        return State.query.get(state_id)

    def get_city_addresses(self, city_id):
        return City.query.get(city_id)

    def get_address_by_id(self, address_id):
        return Address.query.filter_by(id=address_id).join(City).join(State).join(Country).first()

    def register_address_by_names(self, street_name, neighbourhood, city_name, state_name, country_name):
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

            return address.id

        except exc.IntegrityError:
            db.session.rollback()
            return None

    def remove_address_by_id(self, address):
        try:
            db.session.delete(address)
            db.session.commit()

            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False
