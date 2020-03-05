from model.super_user import SuperUser
# from controller.address_controller import AddressController
# from controller.condominium_controller import CondominiumController
# from controller.resident_controller import ResidentController
# from controller.employee_controller import EmployeeController
# from controller.notification_controller import NotificationController
# from controller.rule_controller import RuleController
# from controller.guest_controller import GuestController
# from controller.service_controller import ServiceController
# from controller.event_controller import EventController
from helpers.permission_levels import PermissionLevel
# from helpers.condominium_builder import build
from sqlalchemy.sql import select
import time
from setup import db
import bcrypt


def _user_key_decorator(function):
    def check_user_key(self, *args, **kwargs):
        if args[1] not in self.users_permission_level:
            return False, 'User session not registered'

        return function(self, *args)

    return check_user_key


def _default_answer_decorator(function):
    def check_default_answer(self, *args, **kwargs):
        return function(self, *args) or (False, 'User does not have the necessary permission level')

    return check_default_answer


class PermissionManager:
    def __init__(self):
        self.employee_types = {1: 'employee', 2: 'super_employee'}
        self.users_permission_level = {}
        # self.address_controller = AddressController()
        # self.condominium_controller = CondominiumController()
        # self.resident_controller = ResidentController()
        # self.employee_controller = EmployeeController()
        # self.notification_controller = NotificationController()
        # self.rule_controller = RuleController()
        # self.guest_controller = GuestController()
        # self.service_controller = ServiceController()
        # self.event_controller = EventController()

    def register_key(self, key_type, session_key):
        if key_type == 'employee':
            self.users_permission_level[session_key] = PermissionLevel.EMPLOYEE

        elif key_type == 'resident':
            self.users_permission_level[session_key] = PermissionLevel.RESIDENT

        elif key_type == 'super_employee':
            self.users_permission_level[session_key] = PermissionLevel.SUPER_EMPLOYEE

        elif key_type == 'super_user':
            self.users_permission_level[session_key] = PermissionLevel.SYSTEM

        else:
            raise RuntimeError

    async def login_super_user(self, username, password):
        db_start_time = time.time()
        super_user = await db.fetch_one(select([SuperUser]).where(SuperUser.username == username))
        db_end_time = time.time()

        if super_user is None:
            return False, 'User not found', None

        if bcrypt.checkpw(password.encode('utf-8'), super_user.password.encode('utf-8')):
            return True, super_user, super_user.username, db_end_time - db_start_time

        return False, 'User passowrd does not match', None

    @_user_key_decorator
    @_default_answer_decorator
    def build_condominium_schema(self, schema, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.SYSTEM:
            return build(schema), None

    def login_resident(self, username, password):
        user = self.resident_controller.do_login(username)
        if user is None:
            return False, 'User not found.', None, None

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            return True, \
                   self.condominium_controller.get_resident_login_info(user.apartment_id), \
                   user.apartment_id, \
                   user.apartment.tower.condominium.name

        return False, 'User password does not match.', None, None

    def login_employee(self, username, password):
        user = self.employee_controller.do_login(username)

        if user is None:
            return False, 'User not found.', None

        elif bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            employee = user.employee
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address], self.employee_types[employee.type]
        else:
            return False, 'User password does not match.', None

    @_user_key_decorator
    @_default_answer_decorator
    def register_resident_user(self, username, hash_password, apartment_id, father_id, user_key):
        if PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            for tower in self.employee_controller.get_employee_by_id(father_id).condominium:
                for apartment in tower.apartments:
                    if apartment.id == apartment_id:
                        return self.resident_controller.register_user(username, hash_password, apartment_id), None

            return False, 'User does not have the privileges to do such operation'

    @_user_key_decorator
    @_default_answer_decorator
    def register_resident(self, cpf, name, birthday, photo_location, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            resident = self.resident_controller.register_resident(cpf, name, birthday, photo_location, father_id)

            if resident is None:
                return False, 'Resident could not be registered'

            else:
                return True, [resident,
                              resident.apartment,
                              resident.apartment.tower,
                              resident.apartment.tower.condominium,
                              resident.apartment.tower.condominium.address]

    @_user_key_decorator
    def register_employee(self, employee_type, username, hash_password, cpf, name, birthday, photo_location, role,
                          father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.SUPER_EMPLOYEE and employee_type == 1:
            condominium_id = self.employee_controller.get_employee_by_id(father_id).condominium_id

            employee = self.employee_controller.register_employee(employee_type,
                                                                  username, hash_password,
                                                                  cpf, name, birthday, photo_location, role,
                                                                  condominium_id)

        elif self.users_permission_level[user_key] == PermissionLevel.SYSTEM:
            employee = self.employee_controller.register_employee(employee_type,
                                                                  username, hash_password,
                                                                  cpf, name, birthday, photo_location, role,
                                                                  father_id)

        else:
            return None

        if employee is None:
            return False, 'Employee could not be registered'

        else:
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address]

    @_user_key_decorator
    @_default_answer_decorator
    def get_employees(self, user_id, user_key):
        if PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            return True, self.employee_controller.get_employee_by_id(user_id).condominium.employees

    @_user_key_decorator
    @_default_answer_decorator
    def get_residents(self, user_id, apartment_number, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            apartment = self.condominium_controller.get_apartment_by_id(father_id)
            if apartment is None:
                return False, 'ID not found'

            elif apartment.apt_number == apartment_number:
                return True, apartment.residents

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(user_id).condominium_id
            return True, self.condominium_controller.get_apartment_residents_by_condominium_id_and_apt_number(condominium_id, apartment_number)

    @_user_key_decorator
    @_default_answer_decorator
    def get_notifications(self, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            condominium_id = self.condominium_controller.get_apartment_condominium_id(father_id)
            return True, self.condominium_controller.get_condominium_by_id(condominium_id).notifications

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            return True, self.employee_controller.get_employee_by_id(father_id).condominium.notifications

    @_user_key_decorator
    @_default_answer_decorator
    def get_guests(self, apartment_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            return True, self.condominium_controller.get_apartment_by_id(father_id).guests

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            if apartment_id is None:
                return False, 'User does not have the privileges to do such operation'

            for tower in self.employee_controller.get_employee_by_id(father_id).condominium:
                for apartment in tower.apartments:
                    if apartment.id == apartment_id:
                        return True, apartment.guests

            return False, 'Apartment not found'

    @_user_key_decorator
    @_default_answer_decorator
    def get_services(self, apartment_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            return True, self.condominium_controller.get_apartment_by_id(father_id).services

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            if apartment_id is None:
                return False, 'User does not have the privileges to do such operation'

            for tower in self.employee_controller.get_employee_by_id(father_id).condominium:
                for apartment in tower.apartments:
                    if apartment.id == apartment_id:
                        return True, apartment.services

            return False, 'Apartment not found'

    @_user_key_decorator
    @_default_answer_decorator
    def get_rules(self, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            return True, self.condominium_controller.get_apartment_by_id(father_id).tower.condominium.rules

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            return True, self.employee_controller.get_employee_by_id(father_id).condominium.rules

    @_user_key_decorator
    @_default_answer_decorator
    def get_apartment_events(self, apartment_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            return True, self.condominium_controller.get_apartment_by_id(father_id).events

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            if apartment_id is None:
                return False, 'User does not have the privileges to do such operation'

            for tower in self.employee_controller.get_employee_by_id(father_id).condominium:
                for apartment in tower.apartments:
                    if apartment.id == apartment_id:
                        return True, apartment.events

            return False, 'Apartment not found'

    @_user_key_decorator
    @_default_answer_decorator
    def get_all_events(self, start, end, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            condominium_id = self.condominium_controller.get_apartment_by_id(father_id).tower.apartment_id
            return True, self.event_controller.get_condominium_events(start, end, condominium_id)

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(father_id).condominium_id
            return True, self.event_controller.get_condominium_events(start, end, condominium_id)

    @_user_key_decorator
    @_default_answer_decorator
    def get_event_types(self, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            condominium_id = self.condominium_controller.get_apartment_by_id(father_id).tower.apartment_id
            return True, self.event_controller.get_condominium_event_types(condominium_id)

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(father_id).condominium_id
            return True, self.event_controller.get_condominium_event_types(condominium_id)

    @_user_key_decorator
    @_default_answer_decorator
    def register_notification(self, notification_type, title, text, finish_date, father_id, user_key):
        if PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(father_id).condominium_id
            result = self.notification_controller.register_notification(notification_type, title, text, finish_date,
                                                                        father_id, condominium_id)
            if result:
                return True, None

            return False, 'Notification could not be registered'

    @_user_key_decorator
    @_default_answer_decorator
    def register_guest(self, guest_name, guest_arrival, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            result = self.guest_controller.register_guest(guest_name, guest_arrival, father_id)
            if result:
                return True, 'Guest registered'

            return False, 'Guest could not be registered'

    @_user_key_decorator
    @_default_answer_decorator
    def register_service(self, service_name, employee_name, service_arrival, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            result = self.service_controller.register_service(service_name, employee_name, service_arrival, father_id)
            if result:
                return True, 'Service registered'

            return False, 'Service could not be registered'

    @_user_key_decorator
    @_default_answer_decorator
    def register_rule(self, text, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            result = self.rule_controller.register_rule(text, father_id, self.employee_controller.get_employee_by_id(father_id).condominium_id)
            if result:
                return True, 'Rule registered'

            return False, 'Rule could not be registered'

    @_user_key_decorator
    @_default_answer_decorator
    def register_event(self, start, end, event_type_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            result = self.event_controller.register_event(start, end, event_type_id, father_id)
            if result:
                return True, 'Event registered'

            return False, 'Event could not be registered'

    @_user_key_decorator
    @_default_answer_decorator
    def remove_notification(self, notification_id, father_id, user_key):
        if PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            for notification in self.employee_controller.get_employee_by_id(father_id).condominium.notifications:
                if notification.id == notification_id:
                    result = self.notification_controller.remove_notification(notification)
                    if result:
                        return True, None

                    return False, 'Notification could not be deleted'

            return None, 'Notification not found'

    @_user_key_decorator
    @_default_answer_decorator
    def remove_guest(self, guest_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            for guest in self.condominium_controller.get_apartment_by_id(father_id).guests:
                if guest.id == guest_id:
                    result = self.guest_controller.remove_guest(guest)
                    if result:
                        return True, None

                    return False, 'Guest could not be deleted'

            return None, 'Guest not found'

    @_user_key_decorator
    @_default_answer_decorator
    def remove_service(self, service_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            for service in self.condominium_controller.get_apartment_by_id(father_id).services:
                if service.id == service_id:
                    result = self.service_controller.remove_service(service)
                    if result:
                        return True, None

                    return False, 'Service could not be deleted'

            return None, 'Service not found'

    @_user_key_decorator
    @_default_answer_decorator
    def remove_rule(self, rule_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            for rule in self.employee_controller.get_employee_by_id(father_id).condominium.rules:
                if rule.id == rule_id:
                    result = self.rule_controller.remove_rule(rule)
                    if result:
                        return True, None

                    return False, 'Rule could not be deleted'

            return None, 'Rule not found'

    @_user_key_decorator
    @_default_answer_decorator
    def remove_event(self, event_id, father_id, user_key):
        if self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            for event in self.condominium_controller.get_apartment_by_id(father_id).events:
                if event.id == event_id:
                    result = self.event_controller.remove_event(event)
                    if result:
                        return True, None

                    return False, 'Event could not be deleted'

            return None, 'Event not found'

    def drop_session(self, session_key):
        if session_key not in self.users_permission_level:
            return False

        del self.users_permission_level[session_key]
        return True
