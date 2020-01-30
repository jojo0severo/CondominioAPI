from setup import db
from model.country import Country
from model.state import State
from model.city import City
from model.address import Address
from model.condominium import Condominium
from model.tower import Tower
from model.apartment import Apartment
from model.resident import Resident
from model.resident_user import ResidentUser
from model.employee import Employee
from model.employee_user import EmployeeUser
from model.notification import Notification
from model.guest import Guest
from model.service import Service
from model.rule import Rule
from model.super_user import SuperUser


class SuperUserController:
    @staticmethod
    def get_super_users():
        return SuperUser.query.all()

    @staticmethod
    def get_super_user(username):
        return SuperUser.query.get(username)

    @staticmethod
    def register_super_user(username, password):
        db.session.add(SuperUser(username=username, password=password))
        db.session.commit()
        return True

    @staticmethod
    def delete_super_user(username):
        deleted = SuperUser.query.filter_by(username=username).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_countries():
        return Country.query.all()

    @staticmethod
    def get_country(country_id):
        return Country.query.get(country_id)

    @staticmethod
    def register_country(country_name):
        db.session.add(Country(name=country_name))
        db.session.commit()
        return True

    @staticmethod
    def remove_country(country_id):
        deleted = Country.query.filter_by(id=country_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_states():
        return State.query.all()

    @staticmethod
    def get_state(state_id):
        return State.query.filter(State.id == state_id).join(Country)

    @staticmethod
    def register_state(state_name, country_id):
        db.session.add(State(name=state_name, country_id=country_id))
        db.session.commit()
        return True

    @staticmethod
    def remove_state(state_id):
        deleted = State.query.filter_by(id=state_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_cities():
        return City.query.all()

    @staticmethod
    def get_city(city_id):
        return City.query.filter(City.id == city_id).join(State).join(Country)

    @staticmethod
    def register_city(city_name, state_id):
        db.session.add(City(name=city_name, state_id=state_id))
        db.session.commit()
        return True

    @staticmethod
    def remove_city(city_id):
        deleted = City.query.filter_by(id=city_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_addresses():
        return Address.query.all()

    @staticmethod
    def get_address(address_id):
        return Address.query.filter(Address.id == address_id).join(City).join(State).join(Country)

    @staticmethod
    def register_address(street_name, neighbourhood, city_id):
        db.session.add(Address(street_name=street_name, neighbourhood=neighbourhood, city_id=city_id))
        db.session.commit()
        return True

    @staticmethod
    def remove_address(address_id):
        deleted = Address.query.filter_by(id=address_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_condominiums():
        return Condominium.query.all()

    @staticmethod
    def get_condominium(condominium_id):
        return Condominium.query.filter(Condominium.id == condominium_id).join(Address).join(City).join(State).join(Country)

    @staticmethod
    def get_towers():
        return Tower.query.all()

    @staticmethod
    def get_tower(tower_id):
        return Tower.query.filter(Tower.id == tower_id).join(Condominium).join(Address)

    @staticmethod
    def get_apartment(apartment_id):
        return Apartment.query.filter(Apartment.id == apartment_id).join(Tower).join(Condominium).join(Address)

    @staticmethod
    def get_apartments():
        return Apartment.query.all()

    @staticmethod
    def get_resident(resident_id):
        return Resident.query.filter(Resident.id == resident_id).join(Apartment).join(Tower).join(Condominium).join(Address)

    @staticmethod
    def get_residents():
        return Resident.query.all()

    @staticmethod
    def get_resident_user(resident_user_username):
        return ResidentUser.query.filter(ResidentUser.username == resident_user_username).join(Resident)

    @staticmethod
    def get_resident_users():
        return ResidentUser.query.all()

    @staticmethod
    def get_employee(employee_id):
        return Employee.query.filter(Employee.id == employee_id).join(Condominium).join(Address)

    @staticmethod
    def get_employees():
        return Employee.query.all()

    @staticmethod
    def get_employee_user(employee_user_username):
        return EmployeeUser.query.filter(EmployeeUser.username == employee_user_username).join(Employee)

    @staticmethod
    def get_employee_users():
        return EmployeeUser.query.all()

    @staticmethod
    def get_notification(notification_id):
        return Notification.query.filter(Notification.id == notification_id).join(Condominium).join(Address)

    @staticmethod
    def get_notifications():
        return Notification.query.all()

    @staticmethod
    def get_guest(guest_id):
        return Guest.query.filter(Guest.id == guest_id).join(Condominium).join(Address)

    @staticmethod
    def get_guests():
        return Guest.query.all()

    @staticmethod
    def get_service(service_id):
        return Service.query.filter(Service.id == service_id).join(Condominium).join(Address)

    @staticmethod
    def get_services():
        return Service.query.all()

    @staticmethod
    def get_rule(rule_id):
        return Rule.query.filter(Rule.id == rule_id).join(Condominium).join(Address)

    @staticmethod
    def get_rules():
        return Rule.query.all()
