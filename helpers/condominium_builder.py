from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from setup import db
from sqlalchemy import exc, and_


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

    parse_apartments(tower_obj, 1)


def parse_apartments(tower_obj, tower_id):
    if 'apartments' in tower_obj:
        for i in range(tower_obj['apartments'][-1]):
            db.session.add(Apartment(apt_number=i, tower_id=tower_id))

    else:
        for i in range(tower_obj['floors']):
            apt_number = tower_obj['start'] + (i * tower_obj['start'])
            for j in range(tower_obj['apartments_by_floor'] + 1):
                db.session.add(Apartment(apt_number=apt_number + j, tower_id=tower_id))


def build_address(condominium_obj):
    try:
        country = Country(name=condominium_obj['country_name'])
        db.session.add(country)

    except exc.IntegrityError:
        db.session.rollback()
        country = Country.query.filter_by(name=condominium_obj['country_name'])

    try:
        state = State(name=condominium_obj['state_name'], country_id=country.id)
        db.session.add(state)

    except exc.IntegrityError:
        db.session.rollback()
        state = State.query.filter(and_(State.name == condominium_obj['state_name'], State.country_id == country.id))

    try:
        city = City(name=condominium_obj['city_name'], state_id=state.id)
        db.session.add(city)

    except exc.IntegrityError:
        db.session.rollback()
        city = City.query.filter(and_(City.name == condominium_obj['city_name'], City.state_id == state.id))

    try:
        address = Address(street_name=condominium_obj['street_name'], neighbourhood=condominium_obj['neighbourhood'], city_id=city.id)
        db.session.add(address)

        return address.id

    except exc.IntegrityError as e:
        db.session.rollback()
        raise ValueError(e)


def build(json_structure):
    for condominium in json_structure:
        condominium_obj = json_structure[condominium]

        address_id = build_address(condominium_obj)

        condominium = Condominium(name=condominium, address_id=address_id)
        db.session.add(condominium)

        for key in condominium_obj:
            if key == 'Towers':
                parse_tower_list(condominium_obj[key], condominium.id)
            else:
                parse_tower(condominium_obj[key], key, condominium.id)

    try:
        db.session.commit()
        return True

    except exc.IntegrityError:
        db.session.rollback()
        return False
