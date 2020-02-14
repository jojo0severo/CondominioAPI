from setup import db

from model.super_user import SuperUser
from model.notification import Notification
from model.rule import Rule
from model.guest import Guest
from model.service import Service
from model.event import Event
from model.event_type import EventType
from model.username import Username
from model.resident_user import ResidentUser
from model.resident import Resident
from model.employee_user import EmployeeUser
from model.employee import Employee
from model.apartment import Apartment
from model.tower import Tower
from model.condominium import Condominium
from model.address import Address
from model.city import City
from model.state import State
from model.country import Country


db.drop_all()
db.create_all()

db.session.query(SuperUser).delete()
db.session.query(Notification).delete()
db.session.query(Rule).delete()
db.session.query(Guest).delete()
db.session.query(Service).delete()
db.session.query(Event).delete()
db.session.query(EventType).delete()
db.session.query(Username).delete()
db.session.query(ResidentUser).delete()
db.session.query(Resident).delete()
db.session.query(EmployeeUser).delete()
db.session.query(Employee).delete()
db.session.query(Apartment).delete()
db.session.query(Tower).delete()
db.session.query(Condominium).delete()
db.session.query(Address).delete()
db.session.query(City).delete()
db.session.query(State).delete()
db.session.query(Country).delete()

db.session.commit()
