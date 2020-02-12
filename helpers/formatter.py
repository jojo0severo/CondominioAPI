import base64


class JSONFormatter:
    def format_resident_connection(self, result, info):
        if result:
            return {
                'result': True,
                'event': 'Resident successfully logged',
                'data': {
                    'resident': self.format_resident(info[0]),
                    'apartment': self.format_apartment(info[1]),
                    'tower': self.format_tower(info[2]),
                    'condominium': self.format_condominium(info[3]),
                    'address': self.format_address(info[4])
                }
            }

        return {'result': False, 'event': 'Resident could not be logged', 'data': {}}

    def format_employee_connection(self, result, info):
        if result:
            return {
                'result': True,
                'event': 'Resident successfully logged',
                'data': {
                    'employee': self.format_employee(info[0]),
                    'condominium': self.format_condominium(info[1]),
                    'address': self.format_address(info[2])
                }
            }

        return {'result': False, 'event': 'Employee could not be logged', 'data': {}}

    @staticmethod
    def format_resident(resident):
        return {'id': base64.urlsafe_b64encode(str(resident.id).encode('ascii')).decode('ascii'),
                'CPF': resident.cpf,
                'Name': resident.name,
                'Birthday': resident.birthday.strftime("%Y-%m-%d"),
                'PhotoLocation': resident.photo_location}

    @staticmethod
    def format_employee(employee):
        return {'id': base64.urlsafe_b64encode(str(employee.id).encode('ascii')).decode('ascii'),
                'CPF': employee.cpf,
                'Name': employee.name,
                'Birthday': employee.birthday.strftime("%Y-%m-%d"),
                'Role': employee.role,
                'PhotoLocation': employee.photo_location}

    @staticmethod
    def format_apartment(apartment):
        return {'Number': apartment.apt_number}

    @staticmethod
    def format_tower(tower):
        return {'Name': tower.name}

    @staticmethod
    def format_condominium(condominium):
        return {'Name': condominium.name, 'PhotoLocation': condominium.photo_location}

    @staticmethod
    def format_address(address):
        return {'Street': address.street_name, 'Neighbourhood': address.neighbourhood, 'City': address.city.name}
