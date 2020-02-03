from controller.address_controller import AddressController
from controller.condominium_controller import CondominiumController
from controller.resident_controller import ResidentController
from controller.employee_controller import EmployeeController
from controller.notification_controller import NotificationController
from controller.rule_controller import RuleController
from controller.guest_controller import GuestController
from controller.service_controller import ServiceController
from controller.event_controller import EventController
import json


class JSONFormatter:
    def __init__(self, system_session_key):
        self.address_controller = AddressController(system_session_key)
        self.condominium_controller = CondominiumController(system_session_key)
        self.notification_controller = NotificationController(system_session_key)
        self.rule_controller = RuleController(system_session_key)
        self.guest_controller = GuestController(system_session_key)
        self.service_controller = ServiceController(system_session_key)

    def formatted_get_country_states(self, session_key, country_id):
        return self.address_controller.get_country_states(session_key, country_id)

    def formatted_get_state_cities(self, session_key, state_id):
        return self.address_controller.get_state_cities(session_key, state_id)

    def formatted_get_city_addresses(self, session_key, city_id):
        return self.address_controller.get_city_addresses(session_key, city_id)

    def formatted_get_address_by_id(self, session_key, address_id):
        return self.address_controller.get_address_by_id(session_key, address_id)

    def formatted_get_condominium_by_id(self, condominium_id):
        return self.condominium_controller.get_condominium_by_id(condominium_id)

    def formatted_get_tower_by_id(self, tower_id):
        return self.condominium_controller.get_tower_by_id(tower_id)

    def formatted_get_apartment_by_id(self, apartment_id):
        return self.condominium_controller.get_apartment_by_id(apartment_id)

    def formatted_get_condominium_employees(self, condominium_id):
        return self.condominium_controller.get_condominium_employees(condominium_id)

    def formatted_get_condominium_rules(self, condominium_id):
        return self.condominium_controller.get_condominium_rules(condominium_id)

    def formatted_get_get_condominium_event_types(self, condominium_id):
        return self.condominium_controller.get_condominium_event_types(condominium_id)

    def formatted_get_condominium_towers(self, session_key, condominium_id):
        return self.condominium_controller.get_condominium_towers(session_key, condominium_id)

    def formatted_get_tower_apartments(self, session_key, tower_id):
        return self.condominium_controller.get_tower_apartments(session_key, tower_id)

    def formatted_get_apartment_residents(self, session_key, apartment_id):
        return self.condominium_controller.get_apartment_residents(session_key, apartment_id)

    def formatted_get_notification_by_id(self, notification_id):
        return self.notification_controller.get_notification_by_id(notification_id)

    def formatted_get_rule_by_id(self, rule_id):
        return self.rule_controller.get_rule_by_id(rule_id)

    def formatted_get_guest_by_id(self, guest_id):
        return self.guest_controller.get_guest_by_id(guest_id)

    def formatted_get_guests_by_date(self, condominium_id, start_datetime, end_datetime):
        return self.guest_controller.get_guests_by_date(condominium_id, start_datetime, end_datetime)

    def formatted_get_service_by_id(self, service_id):
        return self.service_controller.get_service_by_id(service_id)

    def formatted_get_service_by_date(self, condominium_id, start_datetime, end_datetime):
        return self.service_controller.get_service_by_date(condominium_id, start_datetime, end_datetime)

    def formatted_register_address_by_names(self, session_key, street_name, neighbourhood, city_name, state_name, country_name):
        return self.address_controller.register_address_by_names(session_key, street_name, neighbourhood, city_name, state_name, country_name)

    def formatted_register_condominium(self, session_key, name, street_number, photo_location, address_id):
        return self.condominium_controller.register_condominium(session_key, name, street_number, photo_location, address_id)

    def formatted_register_tower(self, session_key, name, condominium_id):
        return self.condominium_controller.register_tower(session_key, name, condominium_id)

    def formatted_register_apartment(self, session_key, apt_number, tower_id):
        return self.condominium_controller.register_apartment(session_key, apt_number, tower_id)

    def formatted_register_notification(self, session_key, noti_type, title, text, finish_date, condominium_id):
        return self.notification_controller.register_notification(session_key, noti_type, title, text, finish_date, condominium_id)

    def formatted_register_rule(self, session_key, text, condominium_id):
        return self.rule_controller.register_rule(session_key, text, condominium_id)

    def formatted_register_guest(self, session_key, name, arrival, apartment_id):
        return self.guest_controller.register_guest(session_key, name, arrival, apartment_id)

    def formatted_register_service(self, session_key, name, employee, arrival, apartment_id):
        return self.service_controller.register_service(session_key, name, employee, arrival, apartment_id)

    def formatted_remove_address_by_id(self, session_key, address_id):
        return self.address_controller.remove_address_by_id(session_key, address_id)

    def formatted_remove_condominium(self, session_key, condominium_id):
        return self.condominium_controller.remove_condominium(session_key, condominium_id)

    def formatted_remove_tower(self, session_key, tower_id):
        return self.condominium_controller.remove_tower(session_key, tower_id)

    def formatted_remove_apartment(self, session_key, apartment_id):
        return self.condominium_controller.remove_apartment(session_key, apartment_id)

    def formatted_remove_notification(self, session_key, notification_id):
        return self.notification_controller.remove_notification(session_key, notification_id)

    def formatted_remove_rule(self, session_key, rule_id):
        return self.rule_controller.remove_rule(session_key, rule_id)

    def formatted_remove_guest(self, session_key, guest_id):
        return self.guest_controller.remove_guest(session_key, guest_id)

    def formatted_remove_service(self, session_key, service_id):
        return self.service_controller.remove_service(session_key, service_id)

    def drop_session(self, session_type, session):
        if session_type == 'resident':
            self.guest_controller.drop_session(session)
            self.service_controller.drop_session(session)

        elif session == 'employee':
            self.condominium_controller.drop_session(session)
            self.notification_controller.drop_session(session)
            self.rule_controller.drop_session(session)

        else:
            print('Wrong session type received', session_type)
