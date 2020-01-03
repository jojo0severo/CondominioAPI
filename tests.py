
import os
from datetime import datetime
from model.database import setup_database

setup_database()

from model.complex import Complex
from model.tower import Tower
from model.apartment import Apartment
from model.resident import Resident
from model.event import Event
from model.complex_event import ComplexEvent
from model.resident_event import ResidentEvent
from model.shop import Shop
from model.shop_item import Item
from model.service import Service
from model.service_day import ServiceDay
from model.rule import Rule
from model.warning import Warning
from model.employee import Employee

date_format = '%Y-%m-%d %H:%M:%S'

os.remove('data/database.db')
setup_database()

print('\nTrying Complex')
Complex.insert('condominio1')
Complex.select_all()
Complex.select_one('condominio1')
print('Complex passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Tower')
Tower.insert('c1', 'condominio1')
Tower.select_all()
Tower.select_all_from_parent('condominio1')
print('Tower passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Apartment')
Apartment.insert(101, 'c1', 'condominio1')
Apartment.select_all()
Apartment.select_all_from_parent('c1', 'condominio1')
print('Apartment passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Resident')
Resident.insert('02044556006', 'jojo', 'jojo@jojo.com', '5199456722', 101, 'c1', 'condominio1')
Resident.select_all()
Resident.select_all_from_parent(202, 'c1', 'condominio1')
print('Resident passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Event')
Event.insert('vaga', 'vaga 1c', '', 'condominio1')
Event.select_all()
Event.select_all_from_parent('condominio1')
print('Event passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying ComplexEvent')
ComplexEvent.insert('02044556006', 'sindico', 30, 'jojo', 'vaga', 'vaga 2c', '', str(datetime.now().strftime(format)), str(datetime.now().strftime(format)), 'condominio1')
ComplexEvent.select_all()
ComplexEvent.select_all_from_parent('condominio1')
print('ComplexEvent passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying ResidentEvent')
ResidentEvent.insert(303, 'c1', 'vaga', 'vaga 2c', '', str(datetime.now().strftime(format)), str(datetime.now().strftime(format)), 'condominio1')
ResidentEvent.select_all()
ResidentEvent.select_all_from_parent('condominio1')
print('ResidentEvent passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Shop')
Shop.insert('carros', 'condominio1')
Shop.select_all()
Shop.select_all_from_parent('condominio1')
print('Shop passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Item')
Item.insert('aviões', 101, 'boing 737', 500.0, 'avião de uso empresarial', 'images/aviões/boing737', 'c1', 'condominio1')
Item.select_all()
Item.select_all_from_parent('aviões', 'condominio1')
print('Item passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Service')
Service.insert('jojo', 'encanadores SA', 'encanador', 101, 'c1', 'condominio1')
Service.select_all()
Service.select_all_from_parent(606, 'c1', 'condominio1')
print('Service passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying ServiceDay')
ServiceDay.insert(1, str(datetime.now().strftime(format)), str(datetime.now().strftime(format)), 'jojones', 'desentupidores SA', 'desentupidor', 101, 'c1', 'condominio1')
ServiceDay.select_all()
ServiceDay.select_all_from_parent(707, 'c1', 'condominio1')
print('ServiceDay passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Rule')
Rule.insert('Não é permitido explodir o condomínio', 'condominio1')
Rule.select_all()
Rule.select_all_from_parent('condominio1')
print('Rule passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Warning')
Warning.insert(5, 'Alguém explodiu o condomńio', 'c2', 'condominio1')
Warning.select_all()
Warning.select_all_from_parent('condominio1')
print('Warning passed')

# os.remove('data/database.db')
# setup_database()

print('\nTrying Employee')
Employee.insert('02044556006', 'jojow', 31, 'porteiro', 'condominio1')
Employee.select_all()
Employee.select_all_from_parent('condominio1')
print('Employee passed')

os.remove('data/database.db')