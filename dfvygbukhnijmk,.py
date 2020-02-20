from model.notification import Notification
from model.employee import Employee
from helpers.handler import Handler
from setup import db
import time
import datetime
import bcrypt


def performance_test():
    batch = 100000
    for i in range(1, 11):
        objs = [Notification(type=1,
                             title='Corredor Torre 1',
                             text='Corredor da torre 1 está interdidato até semana que vem',
                             finish_date=datetime.datetime.strptime('2020-02-10', '%Y-%m-%d'),
                             condominium_id=1) for _ in range(batch - 2000)]

        objs.extend([Notification(type=1,
                                  title='Corredor Torre 1',
                                  text='Corredor da torre 1 está interdidato até semana que vem end',
                                  finish_date=datetime.datetime.strptime('2020-02-10', '%Y-%m-%d'),
                                  condominium_id=1) for _ in range(2000)])

        db.session.bulk_save_objects(objs)
        db.session.commit()

        print('Best query i can make')
        start = time.time()
        result = Notification.query.\
            with_entities(Notification.id,
                          Notification.type,
                          Notification.title,
                          Notification.text,
                          Notification.finish_date,
                          Notification.condominium_id)\
            .join(Employee, Notification.condominium_id == Employee.condominium_id)\
            .filter(Employee.id == 1).all()
        end = time.time()
        print(f'Time for {i * batch} values: {end - start} || {len(result)} == {(i * batch)}: {len(result) == (i * batch)}')

        # print('Fetching from employee')
        # start = time.time()
        # result = Employee.query.filter_by(id=1).first().condominium.notifications
        # end = time.time()
        # print(f'Time for {i * batch} values: {end - start} || {len(result)} == {(i * batch)}: {len(result) == (i * batch)}')
        #
        # print('Fetching from notifications')
        # start = time.time()
        # result = Notification.query.join(Condominium).join(Employee).filter(Employee.id == 1).all()
        # end = time.time()
        # print(f'Time for {i * batch} values: {end - start} || {len(result)} == {(i * batch)}: {len(result) == (i * batch)}')

        # print('Fetching from notifications without condominium table')
        # start = time.time()
        # result = Notification.query.join(Employee, Notification.condominium_id == Employee.condominium_id).filter(Employee.id == 1).all()
        # end = time.time()
        # print(f'Time for {i * batch} values: {end - start} || {len(result)} == {(i * batch)}: {len(result) == (i * batch)}')

        # print('Filtering on text')
        # start = time.time()
        # result = Notification.query.filter(Notification.text.like('%end')).all()
        # end = time.time()
        # print(f'Time for {i * batch} values: {end - start} || {len(result)} == {(i * batch)}: {len(result) == (i * batch)}')

        print('\n\n')


if __name__ == '__main__':

    # import secrets
    #
    # list_batata = []
    # first = secrets.token_urlsafe(10)
    # list_batata.append(first)
    # for i in range(100000):
    #     list_batata.append(secrets.token_urlsafe(10))
    #
    # start = time.time()
    # print(first in list_batata)
    # end = time.time()
    # print(end - start)
    #
    # set_batata = set()
    # first = secrets.token_urlsafe(10)
    # set_batata.add(first)
    # for i in range(100000):
    #     set_batata.add(secrets.token_urlsafe(10))
    #
    # start = time.time()
    # print(first in set_batata)
    # end = time.time()
    # print(end - start)
    #
    # exit()

    handler = Handler()
    handler.permission_manager.register_key('super_user', 1)
    handler.permission_manager.register_key('resident', 2)

    print('\nINSERTIONS\n')
    print(handler.permission_manager.address_controller.register_address_by_names('rua', 'bairro', 'cidade', 'estado', 'pais'))
    print(handler.permission_manager.condominium_controller.register_condominium('condominio', 23, None, 1))
    print(handler.permission_manager.condominium_controller.register_tower('t1', 1))
    print(handler.permission_manager.condominium_controller.register_apartment(100, 1))
    print(handler.permission_manager.condominium_controller.register_apartment(200, 1))

    print(handler.permission_manager.register_employee(2, 'employee', bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()), 'cpf', 'name', '1999-06-11', None, 'role', 1, 1))
    print(handler.permission_manager.register_resident_user('resident', bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()), 1, 1, 1))
    print(handler.permission_manager.register_resident('cpf', 'name', '1999-06-11', None, 1, 2))
    print(handler.permission_manager.notification_controller.register_notification(1, 'Titulo', 'Texto', '1999-06-11', 1, 1))

    performance_test()

    # print(a.register_notification(1, 'Corredor T1', 'Corredor da torre 1 está interdidato', '2020-02-10', 1))
    # print(a.register_rule('Proibido fumar dentro das torres e apartamentos', 1))
    # print(a.register_guest('joaozinho', '2020-02-03 14:00', 1))
    # print(a.register_service('encanador', 'pedro alberto', '2020-02-03 14:00', 1))
    # print(a.register_service('pizza', None, '2020-02-03 14:00', 2))

    # print('\n\n\nSELECTS\n')
    # print(a.get_country_states('sistema', None, 1))
    # print(a.get_state_cities('sistema', None, 1))
    # print(a.get_city_addresses('sistema', None, 1))
    # print(a.get_address_by_id('sistema', None, 1))
    # print(a.get_condominium_by_id('sistema', 1))
    # print(a.get_condominium_employees('sistema', 1))
    # print(a.get_condominium_rules('sistema', 1))
    # print(a.get_condominium_towers('sistema', 1))
    # print(a.get_tower_apartments('sistema', 1))
    # print(a.get_apartment_residents('sistema', 1))
    # print(a.get_notification_by_id('sistema', 1))
    # print(a.get_rule_by_id('sistema', 1))
    # print(a.get_guest_by_id(1))
    # print(a.get_guests_by_date(1, '2020-02-01', '2020-02-30'))
    # print(a.get_service_by_id(1))
    # print(a.get_service_by_date(1, '2020-02-01', '2020-02-30'))

    # print('\n\n\nDELETES\n')
    # print(a.remove_address_by_id(1))
    # # print(a.remove_condominium(1))
    # # print(a.remove_tower(1))
    # # print(a.remove_apartment(1))
    # # print(a.remove_notification(1))
    # # print(a.remove_rule(1))
    # # print(a.remove_guest(1))
    # # print(a.remove_service(1))
    #
    # print('\n\n\nSELECTS\n')
    # print(a.get_address_by_id('sistema', None, 1))
    # print(a.get_condominium_by_id('sistema', 1))
    # print(a.get_condominium_rules('sistema', 1))
    # print(a.get_condominium_towers('sistema', 1))
    # print(a.get_tower_apartments('sistema', 1))
    # print(a.get_apartment_residents('sistema', 1))
    # print(a.get_notification_by_id('sistema', 1))
    # print(a.get_rule_by_id('sistema', 1))
    # print(a.get_guest_by_id(1))
    # print(a.get_guests_by_date(1, '2020-02-01', '2020-02-30'))
    # print(a.get_service_by_id(1))
    # print(a.get_service_by_date(1, '2020-02-01', '2020-02-30'))
