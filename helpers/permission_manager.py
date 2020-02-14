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

    def login_resident(self, username, password):
        user = self.resident_controller.do_login(username)
        if user is None:
            return False, 'User not found.'

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            return True, \
                   self.condominium_controller.get_resident_login_info(user.apartment_id), \
                   user.apartment_id, \
                   user.apartment.tower.condominium.name

        return False, 'User password does not match.'

    def login_employee(self, username, password):
        user = self.employee_controller.do_login(username)

        if user is None:
            return False, 'User not found.'

        if bcrypt.checkpw(password.encode('utf-8'), user.password):
            employee = user.employee
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address], self.employee_types[employee.type]
        else:
            return False, 'User password does not match.'

    def register_resident_user(self, username, hash_password, father_id, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        if self.users_permission_level[user_key] < PermissionLevel.EMPLOYEE or self.users_permission_level[user_key] == PermissionLevel.SYSTEM:
            return False, 'User does not have the necessary permission'

        else:
            return self.resident_controller.register_user(username, hash_password, father_id), None

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

        elif self.users_permission_level[user_key] == PermissionLevel.SYSTEM and employee_type == 2:
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

        elif self.users_permission_level[user_key] < PermissionLevel.EMPLOYEE:
            return False, 'User does not have the necessary permission level'

        return True, self.employee_controller.get_employee_by_id(user_id).condominium.employees

    def get_residents(self, user_id, apartment_number, user_key):
        if user_key not in self.users_permission_level:
            return False, 'User session not registered'

        elif self.users_permission_level[user_key] < PermissionLevel.EMPLOYEE:
            return False, 'User does not have the necessary permission level'

        condominium_id = self.employee_controller.get_employee_by_id(user_id).condominium_id
        return True, self.condominium_controller.get_apartment_residents_by_condominium_id_and_apt_number(
            condominium_id, apartment_number)

    def drop_session(self, session_key):
        if session_key not in self.users_permission_level:
            return False

        del self.users_permission_level[session_key]
        return True
