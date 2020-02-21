from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from setup import db
from sqlalchemy import exc


def parse_tower_list(tower_list_obj, condominium_id):
    tower_obj = {}

    if 'apartments' in tower_list_obj:
        tower_obj['apartments'] = tower_list_obj['apartments']
    else:
        tower_obj['floors'] = tower_list_obj['floors']
        tower_obj['apartments_by_floor'] = tower_list_obj['apartments_by_floor']
        tower_obj['start'] = tower_list_obj['start']
        tower_obj['end'] = tower_list_obj['end']

    for tower_name in tower_list_obj["names"]:
        parse_tower(tower_obj, tower_name, condominium_id)


def parse_tower(tower_obj, tower_name, condominium_id):
    tower = Tower(tower_name, condominium_id)
    db.session.add(tower)

    parse_apartments(tower_obj, tower.id)


def parse_apartments(tower_obj, tower_id):
    if 'apartments' in tower_obj:
        for i in range(tower_obj['apartments'][-1]):
            db.session.add(Apartment(apt_number=i, tower_id=tower_id))

    else:
        for i in range(tower_obj['start'], tower_obj['end']):
            pass


def build(json_structure):
    for condominium in json_structure:

        condominium = Condominium(name=condominium)
        db.session.add(condominium)

        condominium_obj = json_structure[condominium]
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
