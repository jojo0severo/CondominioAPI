from controller.login_controller import LoginController
from controller.warning_controller import WarningController
from controller.rule_controller import RuleController
from controller.shop_controller import ShopController
from controller.shop_item_controller import ItemController
from controller.tower_controller import TowerController
from controller.apartment_controller import ApartmentController
from controller.resident_controller import ResidentController
from controller.employee_controller import EmployeeController
from controller.event_controller import EventController
from controller.complex_event_controller import ComplexEventController
from controller.resident_event_controller import ResidentEventController
from controller.service_controller import ServiceController
from controller.service_day_controller import ServiceDayController

date_format = '%Y-%m-%d %H:%M:%S'


class JSONFormatter:
    def __init__(self):
        self.login_controller = LoginController()
        self.warning_controller = WarningController()
        self.rule_controller = RuleController()
        self.shop_controller = ShopController()
        self.item_controller = ItemController()
        self.tower_controller = TowerController()
        self.apartment_controller = ApartmentController()
        self.resident_controller = ResidentController()
        self.employee_controller = EmployeeController()
        self.event_controller = EventController()
        self.complex_event_controller = ComplexEventController()
        self.resident_event_controller = ResidentEventController()
        self.service_controller = ServiceController()
        self.service_day_controller = ServiceDayController()

    def login(self, data):
        if self.login_controller.do_login(data):
            return {'result': True, 'message': 'User successfully logged'}

        return {'result': False, 'message': 'User could not be logged'}

    def get_employee(self, username, data):
        employee = self.employee_controller.get_employee(data)
        if employee and username == employee[0]:
            return {'result': True,
                    'message': 'Employee recovered',
                    'object': {
                        'cpf': employee[0],
                        'name': employee[1],
                        'age': employee[2],
                        'role': employee[3]
                    }}

        raise PermissionError

    def register_employee(self, username, data):
        pass

    def edit_employee(self, username, data):
        pass

    def delete_employee(self, username, data):
        pass

    def get_resident(self, username, data):
        pass

    def register_resident(self, username, data):
        pass

    def edit_resident(self, username, data):
        pass

    def delete_resident(self, username, data):
        pass

    def get_all_apartment(self, data):
        pass

    def get_apartment(self, data):
        pass

    def register_apartment(self, data):
        pass

    def edit_apartment(self, data):
        pass

    def delete_apartment(self, data):
        pass

    def get_all_tower(self, data):
        pass

    def get_tower(self, data):
        pass

    def register_tower(self, data):
        pass

    def edit_tower(self, data):
        pass

    def remove_tower(self, data):
        pass

    def get_all_event(self, data):
        pass

    def get_event(self, data):
        pass

    def register_event(self, data):
        pass

    def edit_event(self, data):
        pass

    def remove_event(self, data):
        pass

    def get_all_complex_event(self, data):
        pass

    def get_complex_event(self, data):
        pass

    def register_complex_event(self, data):
        pass

    def edit_complex_event(self, data):
        pass

    def delete_complex_event(self, data):
        pass

    def get_all_resident_event(self, data):
        pass

    def get_resident_event(self, data):
        pass

    def register_resident_event(self, data):
        pass

    def edit_resident_event(self, data):
        pass

    def delete_resident_event(self, data):
        pass

    def get_all_warning(self, data):
        pass

    def get_warning(self, data):
        pass

    def register_warning(self, data):
        pass

    def edit_warning(self, data):
        pass

    def delete_warning(self, data):
        pass

    def get_all_rule(self, data):
        pass

    def get_rule(self, data):
        pass

    def register_rule(self, data):
        pass

    def edit_rule(self, data):
        pass

    def delete_rule(self, data):
        pass

    def get_all_shop(self, data):
        pass

    def get_shop(self, data):
        pass

    def register_shop(self, data):
        pass

    def edit_shop(self, data):
        pass

    def delete_shop(self, data):
        pass

    def get_all_item(self, shop, data):
        pass

    def get_item(self, shop, data):
        pass

    def register_item(self, shop, data):
        pass

    def edit_item(self, shop, data):
        pass

    def delete_item(self, shop, data):
        pass

    def get_all_service(self, data):
        pass

    def get_service(self, data):
        pass

    def register_service(self, data):
        pass

    def edit_service(self, data):
        pass

    def delete_service(self, data):
        pass

    def get_all_service_day(self, data):
        pass

    def get_service_day(self, data):
        pass

    def register_service_day(self, data):
        pass

    def edit_service_day(self, data):
        pass

    def delete_service_day(self, data):
        pass
