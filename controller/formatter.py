import json
from controller.super_user_controller import SuperUserController
from controller.address_controller import AddressController
from controller.condominium_controller import CondominiumController
from controller.tower_controller import TowerController
from controller.apartment_controller import ApartmentController
from controller.resident_controller import ResidentController
from controller.employee_controller import EmployeeController
from controller.notification_controller import NotificationController
from controller.rule_controller import RuleController
from controller.guest_controller import GuestController
from controller.service_controller import ServiceController
from controller.event_controller import EventController


class JSONFormatter:
    def get_super_country(self, country_id):
        result = SuperUserController.get_country(country_id)
        return result

    def get_super_countries(self):
        result = SuperUserController.get_countries()
        return result

    def get_super_state(self):
        pass

