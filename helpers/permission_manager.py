from controller.address_controller import AddressController
from controller.condominium_controller import CondominiumController
from controller.resident_controller import ResidentController
from controller.employee_controller import EmployeeController
from controller.notification_controller import NotificationController
from controller.rule_controller import RuleController
from controller.guest_controller import GuestController
from controller.service_controller import ServiceController
from controller.event_controller import EventController


class PermissionManager:
    def __init__(self, system_key):
        self.system_key = system_key
        self.users_cache = {}
        self.address_controller = AddressController()
        self.condominium_controller = CondominiumController()
        self.resident_controller = ResidentController()
        self.employee_controller = EmployeeController()
        self.notification_controller = NotificationController()
        self.rule_controller = RuleController()
        self.guest_controller = GuestController()
        self.service_controller = ServiceController()

    def add_session(self, session_key, obj):
        self.users_cache[session_key] = obj

    def login_resident(self, username, password, key):
        if key != self.system_key:
            raise PermissionError

        result, resident = self.resident_controller.do_login(username, password)
        if result:
            return True, [resident,
                          resident.apartment,
                          resident.apartment.tower,
                          resident.apartment.tower.condominium,
                          resident.apartment.tower.condominium.address]

        return False, []

    def login_employee(self, username, password, key):
        if key != self.system_key:
            raise PermissionError

        result, employee = self.employee_controller.do_login(username, password)
        if result:
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address]

        return False, []

    def register_resident(self, username, password, cpf, name, birthday, photo_location, apartment_id, key):
        if key != self.system_key:
            raise PermissionError

        result, resident = self.resident_controller.register_resident(username, password, cpf, name, birthday, photo_location, apartment_id)
        if result:
            return True, [resident,
                          resident.apartment,
                          resident.apartment.tower,
                          resident.apartment.tower.condominium,
                          resident.apartment.tower.condominium.address]

        return False, []

    def register_employee(self, username, password, cpf, name, birthday, photo_location, role, condominium_id, key):
        if key != self.system_key:
            raise PermissionError

        result, employee = self.employee_controller.register_employee(username, password, cpf, name, birthday, photo_location, role, condominium_id)
        if result:
            return True, [employee,
                          employee.condominium,
                          employee.condominium.address]

        return False, []

    def drop_session(self, system_key, session_key):
        if system_key != self.system_key:
            raise PermissionError

        if session_key not in self.users_cache:
            return False

        del self.users_cache[session_key]
        return True
