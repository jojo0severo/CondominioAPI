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
        self.resident_session_map = {}
        self.employee_session_map = {}
        self.address_controller = AddressController()
        self.condominium_controller = CondominiumController()
        self.resident_controller = ResidentController()
        self.employee_controller = EmployeeController()
        self.notification_controller = NotificationController()
        self.rule_controller = RuleController()
        self.guest_controller = GuestController()
        self.service_controller = ServiceController()

    def register_resident_session(self, session_key, resident_id):
        self.resident_session_map[session_key] = resident_id

    def register_employee_session(self, session_key, employee_id):
        self.employee_session_map[session_key] = employee_id

    def login_resident(self, key, user_session, username, password):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.resident_controller.do_login(username, password)

    def login_employee(self, key, user_session, username, password):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.employee_controller.do_login(username, password)

    def get_country_states(self, key, user_session, country_id):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.address_controller.get_country_states(country_id)

    def get_state_cities(self, key, user_session, state_id):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.address_controller.get_state_cities(state_id)

    def get_city_addresses(self, key, user_session, city_id):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.address_controller.get_city_addresses(city_id)

    def get_address_by_id(self, key, user_session, address_id):
        if key != self.system_key:
            raise PermissionError

        if user_session is not None:
            raise PermissionError

        return self.address_controller.get_address_by_id(address_id)

    def get_condominium_by_id(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                if employee.condominium_id == condominium_id:
                    return employee.condominium

                raise PermissionError
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)

            if resident.apartment.tower.condominium_id == condominium_id:
                return resident.apartment.tower.condominium

            raise PermissionError

    def get_condominium_employees(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.employee_session_map:
            raise PermissionError

        employee_id = self.employee_session_map[user_session]
        employee = self.employee_controller.get_employee_by_id(employee_id)
        if employee.condominium_id == condominium_id:
            return employee.condominium.employees

        raise PermissionError

    def get_condominium_rules(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                if employee.condominium_id == condominium_id:
                    return employee.condominium.rules

                raise PermissionError
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)
            tower = resident.apartment.tower
            if tower.condominium_id == condominium_id:
                return tower.condominium.rules

            raise PermissionError

    def get_condominium_notifications(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                if employee.condominium_id == condominium_id:
                    return employee.condominium.notifications

                raise PermissionError
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)
            tower = resident.apartment.tower
            if tower.condominium_id == condominium_id:
                return tower.condominium.notifications

            raise PermissionError

    def get_condominium_event_types(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                if employee.condominium_id == condominium_id:
                    return employee.condominium.event_types

                raise PermissionError
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)
            tower = resident.apartment.tower
            if tower.condominium_id == condominium_id:
                return tower.condominium.event_types

            raise PermissionError

    def get_condominium_towers(self, user_session, condominium_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.employee_session_map:
            raise PermissionError

        employee_id = self.employee_session_map[user_session]
        employee = self.employee_controller.get_employee_by_id(employee_id)
        if employee.condominium_id == condominium_id:
            return employee.condominium.towers

        raise PermissionError

    def get_tower_apartments(self, user_session, tower_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.employee_session_map:
            raise PermissionError

        employee_id = self.employee_session_map[user_session]
        employee = self.employee_controller.get_employee_by_id(employee_id)
        condominium = employee.condominium
        for tower in condominium.towers:
            if tower.id == tower_id:
                return tower.apartments

        raise PermissionError

    def get_apartment_residents(self, user_session, apartment_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.employee_session_map:
            raise PermissionError

        employee_id = self.employee_session_map[user_session]
        employee = self.employee_controller.get_employee_by_id(employee_id)
        condominium = employee.condominium
        for tower in condominium.towers:
            for apartment in tower.apartments:
                if apartment.id == apartment_id:
                    return apartment.residents

        raise PermissionError

    def get_notification_by_id(self, user_session, notification_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                condominium = employee.condominium
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)
            condominium = resident.apartment.tower.condominium

        for notification in condominium.notifications:
            if notification.id == notification_id:
                return notification

        raise PermissionError

    def get_rule_by_id(self, user_session, rule_id):
        if user_session is None:
            raise PermissionError

        if user_session not in self.resident_session_map:
            if user_session not in self.employee_session_map:
                raise PermissionError
            else:
                employee_id = self.employee_session_map[user_session]
                employee = self.employee_controller.get_employee_by_id(employee_id)
                condominium = employee.condominium
        else:
            resident_id = self.resident_session_map[user_session]
            resident = self.resident_controller.get_resident_by_id(resident_id)
            condominium = resident.apartment.tower.condominium

        for rule in condominium.rules:
            if rule.id == rule_id:
                return rule

        raise PermissionError

    def get_guest_by_id(self, guest_id):
        return self.guest_controller.get_guest_by_id(guest_id)

    def get_guests_by_date(self, condominium_id, start_datetime, end_datetime):
        return self.guest_controller.get_guests_by_date(condominium_id, start_datetime, end_datetime)

    def get_service_by_id(self, service_id):
        return self.service_controller.get_service_by_id(service_id)

    def get_service_by_date(self, condominium_id, start_datetime, end_datetime):
        return self.service_controller.get_service_by_date(condominium_id, start_datetime, end_datetime)

    def get_resident_by_id(self, resident_id):
        return self.resident_controller.get_resident_by_id(resident_id)

    def get_resident_user_by_resident(self, cpf, name, birthday, apartment_id):
        return self.resident_controller.get_resident_user_by_resident(cpf, name, birthday, apartment_id)

    def get_employee_by_id(self, employee_id):
        return self.employee_controller.get_employee_by_id(employee_id)
    
    def get_employee_user_by_employee(self, cpf, name, role, birthday, condominium_id):
        return self.employee_controller.get_employee_user_by_employee(cpf, name, role, birthday, condominium_id)

    def register_address_by_names(self, street_name, neighbourhood, city_name, state_name, country_name):
        return self.address_controller.register_address_by_names(street_name, neighbourhood, city_name, state_name, country_name)

    def register_condominium(self, name, street_number, photo_location, address_id):
        return self.condominium_controller.register_condominium(name, street_number, photo_location, address_id)

    def register_tower(self, name, condominium_id):
        return self.condominium_controller.register_tower(name, condominium_id)

    def register_apartment(self, apt_number, tower_id):
        return self.condominium_controller.register_apartment(apt_number, tower_id)

    def register_notification(self, noti_type, title, text, finish_date, condominium_id):
        return self.notification_controller.register_notification(noti_type, title, text, finish_date, condominium_id)

    def register_rule(self, text, condominium_id):
        return self.rule_controller.register_rule(text, condominium_id)

    def register_guest(self, name, arrival, apartment_id):
        return self.guest_controller.register_guest(name, arrival, apartment_id)

    def register_service(self, name, employee, arrival, apartment_id):
        return self.service_controller.register_service(name, employee, arrival, apartment_id)

    def register_resident(self, username, password, cpf, name, birthday, photo_location, apartment_id):
        return self.resident_controller.register_resident(username, password, cpf, name, birthday, photo_location, apartment_id)

    def register_employee(self, username, password, cpf, name, birthday, photo_location, role, condominium_id):
        return self.employee_controller.register_employee(username, password, cpf, name, birthday, photo_location, role, condominium_id)

    def remove_address_by_id(self, address_id):
        return self.address_controller.remove_address_by_id(address_id)

    def remove_condominium(self, condominium_id):
        return self.condominium_controller.remove_condominium(condominium_id)

    def remove_tower(self, tower_id):
        return self.condominium_controller.remove_tower(tower_id)

    def remove_apartment(self, apartment_id):
        return self.condominium_controller.remove_apartment(apartment_id)

    def remove_notification(self, notification_id):
        return self.notification_controller.remove_notification(notification_id)

    def remove_rule(self, rule_id):
        return self.rule_controller.remove_rule(rule_id)

    def remove_guest(self, guest_id):
        return self.guest_controller.remove_guest(guest_id)

    def remove_service(self, service_id):
        return self.service_controller.remove_service(service_id)

    def remove_resident(self, username, password, cpf, name, birthday, apartment_id):
        return self.resident_controller.remove_resident(username, password, cpf, name, birthday, apartment_id)

    def remove_employee(self, username, password, cpf, name, role, birthday, condominium_id):
        return self.employee_controller.remove_employee(username, password, cpf, name, role, birthday, condominium_id)
