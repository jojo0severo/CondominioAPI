from model.super_user import SuperUser
from controller.address_controller import AddressController
from controller.condominium_controller import CondominiumController
from controller.resident_controller import ResidentController
from controller.employee_controller import EmployeeController
from controller.notification_controller import NotificationController
from controller.rule_controller import RuleController
from controller.guest_controller import GuestController
from controller.service_controller import ServiceController
from helpers.permission_levels import PermissionLevel
from controller.event_controller import EventController
import bcrypt


class PermissionManager:
    def __init__(self):
        self.employee_types = {1: 'employee', 2: 'super_employee'}
        self.users_permission_level = {}
        self.address_controller = AddressController()
        self.condominium_controller = CondominiumController()
        self.resident_controller = ResidentController()
        self.employee_controller = EmployeeController()
        self.notification_controller = NotificationController()
        self.rule_controller = RuleController()
        self.guest_controller = GuestController()
        self.service_controller = ServiceController()
        self.event_controller = EventController()

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

    def login_super_user(self, username, password):
        super_user = SuperUser.query.get(username)
        if super_user is None:
            return False, 'User not found', None

        if bcrypt.checkpw(password.encode('utf-8'), super_user.password):
            return True, super_user, super_user.username

        return False, 'User passowrd does not match', None

    def login_resident(self, username, password):
        user = self.resident_controller.do_login(username)
        if user is None:
            return False, 'User not found.', None, None

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True, \
                   self.condominium_controller.get_resident_login_info(user.apartment_id), \
                   user.apartment_id, \
                   user.apartment.tower.condominium.name

        return False, 'User password does not match.', None, None

    def login_employee(self, username, password):
        user = self.employee_controller.do_login(username)

        if user is None:
            return False, 'User not found.', None

        elif bcrypt.checkpw(password.encode('utf-8'), user.password):
            employee = user.employee
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address], self.employee_types[employee.type]
        else:
            return False, 'User password does not match.', None

    def register_resident_user(self, username, hash_password, apartment_id, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        if self.users_permission_level[user_key] < PermissionLevel.EMPLOYEE:
            return False, 'User does not have the necessary permission'

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            for tower in self.employee_controller.get_employee_by_id(father_id).condominium:
                for apartment in tower.apartments:
                    if apartment.id == apartment_id:
                        return self.resident_controller.register_user(username, hash_password, apartment_id), None

            return False, 'User does not have the privileges to do such operation'

        return self.resident_controller.register_user(username, hash_password, apartment_id), None

    def register_resident(self, cpf, name, birthday, photo_location, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif self.users_permission_level[user_key] > PermissionLevel.RESIDENT:
            return False, 'User does not have the necessary permission'

        resident = self.resident_controller.register_resident(cpf, name, birthday, photo_location, father_id)

        if resident is None:
            return False, 'Resident could not be registered'

        else:
            return True, [resident,
                          resident.apartment,
                          resident.apartment.tower,
                          resident.apartment.tower.condominium,
                          resident.apartment.tower.condominium.address]

    def register_employee(self, employee_type, username, hash_password, cpf, name, birthday, photo_location, role, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif self.users_permission_level[user_key] == PermissionLevel.SUPER_EMPLOYEE and employee_type == 1:
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
            return False, 'User does not have the necessary permission'

        if employee is None:
            return False, 'Employee could not be registered'

        else:
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address]

    def get_employees(self, user_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            return True, self.employee_controller.get_employee_by_id(user_id).condominium.employees

        return False, 'User does not have the necessary permission level'

    def get_residents(self, user_id, apartment_number, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            apartment = self.condominium_controller.get_apartment_by_id(father_id)
            if apartment is None:
                return False, 'ID not found'

            elif apartment.apt_number == apartment_number:
                return True, apartment.residents

            return False, 'User does not have the necessary permission level'

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(user_id).condominium_id
            return True, self.condominium_controller.get_apartment_residents_by_condominium_id_and_apt_number(condominium_id, apartment_number)

        return False, 'User does not have the necessary permission level'

    def get_notifications(self, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif self.users_permission_level[user_key] == PermissionLevel.RESIDENT:
            condominium_id = self.condominium_controller.get_apartment_condominium_id(father_id)
            return True, self.condominium_controller.get_condominium_by_id(condominium_id).notifications

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            return True, self.employee_controller.get_employee_by_id(father_id).condominium.notifications

        return False, 'User does not have the necessary permission level'

    def register_notification(self, notification_type, title, text, finish_date, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            condominium_id = self.employee_controller.get_employee_by_id(father_id).condominium_id
            return True, self.notification_controller.register_notification(notification_type, title, text, finish_date, father_id, condominium_id)

        return False, 'User does not have the necessary permission level'

    def remove_notification(self, notification_id, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif PermissionLevel.EMPLOYEE <= self.users_permission_level[user_key] <= PermissionLevel.SUPER_EMPLOYEE:
            for notification in self.employee_controller.get_employee_by_id(father_id).condominium.notifications:
                if notification.id == notification_id:
                    self.notification_controller.remove_notification(notification)
                    return True, None

            return None, 'Notification not found'

        return False, 'User does not have the necessary permission level'

    def drop_session(self, session_key):
        if session_key not in self.users_permission_level:
            return False

        del self.users_permission_level[session_key]
        return True
