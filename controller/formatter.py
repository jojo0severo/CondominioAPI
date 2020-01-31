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
import json


class JSONFormatter:
    def __init__(self):
        self.super_user = SuperUserController()

    def clear(self, session):
        self.super_user.clear(session)
