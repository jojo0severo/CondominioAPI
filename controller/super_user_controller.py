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
from setup import db
from sqlalchemy import exc


class SuperUserController:
    def __init__(self):
        self.sessions = set()

    def add_session(self, session):
        self.sessions.add(session)

    def get_super_users(self, session):
        if session not in self.sessions:
            raise PermissionError

        return SuperUser.query.all()

    def get_super_user(self, session, username, password):
        if session != 'login' and session not in self.sessions:
            raise PermissionError

        user = SuperUser.query.get(username)
        return user is not None and user.password == password

    def register_super_user(self, session, username, password):
        if session not in self.sessions:
            return False

        try:
            db.session.add(SuperUser(username=username, password=password))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def delete_super_user(self, session, username):
        if session not in self.sessions:
            raise PermissionError

        deleted = SuperUser.query.filter_by(username=username).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_countries(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Country.query.all()

    def get_country(self, session, country_id):
        if session not in self.sessions:
            raise PermissionError

        return Country.query.get(country_id)

    def register_country(self, session, country_name):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Country(name=country_name))
            db.session.commit()
            return True

        except exc.IntegrityError:
            return False

    def remove_country(self, session, country_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Country.query.filter_by(id=country_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_states(self, session):
        if session not in self.sessions:
            raise PermissionError

        return State.query.all()

    def get_state(self, session, state_id):
        if session not in self.sessions:
            raise PermissionError

        return State.query.filter(State.id == state_id).join(Country)

    def register_state(self, session, state_name, country_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(State(name=state_name, country_id=country_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_state(self, session, state_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = State.query.filter_by(id=state_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_cities(self, session):
        if session not in self.sessions:
            raise PermissionError

        return City.query.all()

    def get_city(self, session, city_id):
        if session not in self.sessions:
            raise PermissionError

        return City.query.filter(City.id == city_id).join(State).join(Country)

    def register_city(self, session, city_name, state_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(City(name=city_name, state_id=state_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_city(self, session, city_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = City.query.filter_by(id=city_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_addresses(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Address.query.all()

    def get_address(self, session, address_id):
        if session not in self.sessions:
            raise PermissionError

        return Address.query.filter(Address.id == address_id).join(City).join(State).join(Country)

    def register_address(self, session, street_name, neighbourhood, city_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Address(street_name=street_name, neighbourhood=neighbourhood, city_id=city_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            return False

    def remove_address(self, session, address_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Address.query.filter_by(id=address_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_condominiums(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Condominium.query.all()

    def get_condominium(self, session, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        return Condominium.query.filter(Condominium.id == condominium_id).join(Address).join(City).join(State).join(Country)

    def register_condominium(self, session, name, street_number, address_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Condominium(name=name, street_number=street_number, address_id=address_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_condominium(self, session, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Condominium.query.filter_by(id=condominium_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_towers(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Tower.query.all()

    def get_tower(self, session, tower_id):
        if session not in self.sessions:
            raise PermissionError

        return Tower.query.filter(Tower.id == tower_id).join(Condominium).join(Address)

    def register_tower(self, session, name, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Tower(name=name, condominium_id=condominium_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_tower(self, session, tower_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Tower.query.filter_by(id=tower_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_apartments(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Apartment.query.all()

    def get_apartment(self, session, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        return Apartment.query.filter(Apartment.id == apartment_id).join(Tower).join(Condominium).join(Address)

    def register_apartment(self, session, apt_number, tower_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Apartment(apt_number=apt_number, tower_id=tower_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_apartment(self, session, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Apartment.query.filter_by(id=apartment_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_residents(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Resident.query.all()

    def get_resident(self, session, resident_id):
        if session not in self.sessions:
            raise PermissionError

        return Resident.query.filter(Resident.id == resident_id).join(Apartment).join(Tower).join(Condominium).join(Address)

    def register_resident(self, session, cpf, name, birthday, photo_location, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Resident(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, apartment_id=apartment_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_resident(self, session, resident_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Resident.query.filter_by(id=resident_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_resident_users(self, session):
        if session not in self.sessions:
            raise PermissionError

        return ResidentUser.query.all()

    def get_resident_user(self, session, username):
        if session not in self.sessions:
            raise PermissionError

        return ResidentUser.query.filter(ResidentUser.username == username).join(Resident)

    def register_resident_user(self, session, username, password, resident_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(ResidentUser(username=username, password=password, resident_id=resident_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_resident_user(self, session, username):
        if session not in self.sessions:
            raise PermissionError

        deleted = ResidentUser.query.filter_by(username=username).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_employees(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Employee.query.all()

    def get_employee(self, session, employee_id):
        if session not in self.sessions:
            raise PermissionError

        return Employee.query.filter(Employee.id == employee_id).join(Condominium).join(Address)

    def register_employee(self, session, cpf, name, birthday, photo_location, role, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Employee(cpf=cpf, name=name, birthday=birthday, photo_location=photo_location, role=role, condominium_id=condominium_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_employee(self, session, employee_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Employee.query.filter_by(id=employee_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_employee_users(self, session):
        if session not in self.sessions:
            raise PermissionError

        return EmployeeUser.query.all()

    def get_employee_user(self, session, username):
        if session not in self.sessions:
            raise PermissionError

        return EmployeeUser.query.filter(EmployeeUser.username == username).join(Employee)

    def register_employee_user(self, session, username, password, employee_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(EmployeeUser(username=username, password=password, employee_id=employee_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_employee_user(self, session, username):
        if session not in self.sessions:
            raise PermissionError

        deleted = EmployeeUser.query.filter_by(username=username).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_notifications(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Notification.query.all()

    def get_notification(self, session, notification_id):
        if session not in self.sessions:
            raise PermissionError

        return Notification.query.filter(Notification.id == notification_id).join(Condominium).join(Address)

    def register_notification(self, session, notification_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Notification.query.filter_by(id=notification_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def remove_notification(self, session, noti_type, title, text, finish_date, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Notification(type=noti_type, title=title, text=text, finish_date=finish_date, condominium_id=condominium_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def get_guests(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Guest.query.all()

    def get_guest(self, session, guest_id):
        if session not in self.sessions:
            raise PermissionError

        return Guest.query.filter(Guest.id == guest_id).join(Condominium).join(Address)

    def register_guest(self, session, name, arrival, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Guest(name=name, arrival=arrival, apartment_id=apartment_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_guest(self, session, guest_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Guest.query.filter_by(id=guest_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_services(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Service.query.all()

    def get_service(self, session, service_id):
        if session not in self.sessions:
            raise PermissionError

        return Service.query.filter(Service.id == service_id).join(Condominium).join(Address)

    def register_service(self, session, name, employee, arrival, apartment_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Service(name=name, employee=employee, arrival=arrival, apartment_id=apartment_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_service(self, session, service_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Service.query.filter_by(id=service_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def get_rules(self, session):
        if session not in self.sessions:
            raise PermissionError

        return Rule.query.all()

    def get_rule(self, session, rule_id):
        if session not in self.sessions:
            raise PermissionError

        return Rule.query.filter(Rule.id == rule_id).join(Condominium).join(Address)

    def register_rule(self, session, text, condominium_id):
        if session not in self.sessions:
            raise PermissionError

        try:
            db.session.add(Rule(text=text, condominium_id=condominium_id))
            db.session.commit()
            return True

        except exc.IntegrityError:
            db.session.rollback()
            return False

    def remove_rule(self, session, rule_id):
        if session not in self.sessions:
            raise PermissionError

        deleted = Rule.query.filter_by(id=rule_id).delete()
        if deleted:
            db.session.commit()
            return True
        return False

    def clear(self, session):
        self.sessions.remove(session)
