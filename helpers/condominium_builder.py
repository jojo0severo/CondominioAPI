from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from sqlalchemy import exc, and_
from setup import db


def parse_tower_list(tower_list_obj, condominium_id):
    if 'apartments' in tower_list_obj:
        tower_obj = {'apartments': tower_list_obj['apartments']}
    else:
        tower_obj = {
            'floors': tower_list_obj['floors'],
            'apartments_by_floor': tower_list_obj['apartments_by_floor'],
            'start': tower_list_obj['start']
        }

    for tower_name in tower_list_obj["names"]:
        parse_tower(tower_obj, tower_name, condominium_id)


def parse_tower(tower_obj, tower_name, condominium_id):
    tower = Tower(name=tower_name, condominium_id=condominium_id)
    db.session.add(tower)
    db.session.flush()

    parse_apartments(tower_obj, tower.id)


def parse_apartments(tower_obj, tower_id):
    if 'apartments' in tower_obj:
        for apt_number in tower_obj['apartments']:
            db.session.add(Apartment(apt_number=apt_number, tower_id=tower_id))

    else:
        for i in range(tower_obj['start'], (tower_obj['floors'] + 1) * tower_obj['start'], tower_obj['start']):
            for j in range(tower_obj['apartments_by_floor'] + 1):
                db.session.add(Apartment(apt_number=i+j, tower_id=tower_id))


def build_address(condominium_obj):
    try:
        country = Country(name=condominium_obj['CountryName'])
        db.session.add(country)
        db.session.flush()

    except exc.IntegrityError:
        db.session.rollback()
        country = Country.query.filter_by(name=condominium_obj['CountryName']).first()

    try:
        state = State(name=condominium_obj['StateName'], country_id=country.id)
        db.session.add(state)
        db.session.flush()

    except exc.IntegrityError:
        db.session.rollback()
        state = State.query.filter(and_(State.name == condominium_obj['StateName'], State.country_id == country.id)).first()

    try:
        city = City(name=condominium_obj['CityName'], state_id=state.id)
        db.session.add(city)
        db.session.flush()

    except exc.IntegrityError:
        db.session.rollback()
        city = City.query.filter(and_(City.name == condominium_obj['CityName'], City.state_id == state.id)).first()

    address = Address(street_name=condominium_obj['StreetName'], neighbourhood=condominium_obj['Neighbourhood'], city_id=city.id)
    db.session.add(address)
    db.session.flush()

    return address.id


def build(json_structure):
    try:
        for condominium_name in json_structure:
            condominium_obj = json_structure[condominium_name]

            address_id = build_address(condominium_obj)

            condominium = Condominium(name=condominium_name,
                                      street_number=condominium_obj['StreetNumber'],
                                      photo_location=condominium_obj.get('PhotoLocation'),
                                      address_id=address_id)
            db.session.add(condominium)
            db.session.flush()

            for key in condominium_obj['Condominium']:
                if key == 'Towers':
                    parse_tower_list(condominium_obj['Condominium'][key], condominium.id)
                else:
                    parse_tower(condominium_obj['Condominium'][key], key, condominium.id)

            db.session.commit()
            return True

    except exc.IntegrityError:
        db.session.rollback()
        return False
