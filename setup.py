import json
import secrets
import datetime
from functools import wraps
from flask import Flask, request, session, jsonify
from flask_socketio import SocketIO, emit, join_room, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
# from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(20)
app.config['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/api.db'

app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 10000
app.config['SESSION_COOKIE_HTTPONLY'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=3)

# Session(app)
CORS(app)

db = SQLAlchemy(app)
socket = SocketIO(app)

keys = []
system_key = secrets.token_urlsafe(40)


def session_decorator(function):
    @wraps(function)
    def session_checker(*args):
        session_key = session.get('KEY')

        if not session_key:
            return {'status': 401, 'result': False, 'event': 'User is not logged or session expired', 'data': {}}, 401

        data = request.get_json(force=True)
        if 'key' not in [str(key).lower() for key in data.keys()]:
            return {'status': 400, 'result': False, 'event': 'Missing information', 'data': {}}, 400

        key = data['key']

        if key != session_key:
            return {'status': 403, 'result': False, 'event': 'Invalid key', 'data': {}}, 403

        elif key not in keys:
            return {'status': 401, 'result': False, 'event': 'Key not recognized', 'data': {}}, 401

        else:
            return function(*args)

    return session_checker


@app.before_request
def session_configuration():
    session.modified = True
    session.permanent = True
    if 'datetime' in session:
        datetime_diff = session['datetime'] - datetime.datetime.now()
        if datetime_diff.days < 1:
            session['datetime'] = datetime.datetime.now()
        else:
            handler.drop_session(session['type'], session['KEY'])
            keys.remove(session['KEY'])
            del session['KEY']
            del session['room']
            del session['datetime']
            disconnect()


@socket.on('connect')
def verify_connection():
    session_key = session.get('KEY')

    if not session_key:
        raise ConnectionRefusedError

    key = request.get_json(force=True)['key']
    if key != session_key:
        raise ConnectionRefusedError

    elif key not in keys:
        raise ConnectionRefusedError

    if not session.get('room') or not session.get('login'):
        del session['KEY']
        del session['datetime']
        raise ConnectionRefusedError

    if session['login'] != 'resident' and session['login'] != 'employee':
        raise ConnectionRefusedError

    join_room(session['room'] + '_' + session['login'], request.sid)


@app.route('/login/<login_type>', methods=['POST'])
def login(login_type):
    if session.get('KEY') is not None:
        status = 409
        response = {'status': 409, 'result': False, 'event': 'User already logged', 'data': {}}

    else:
        try:
            data = request.get_json(force=True)
            if login_type == 'resident':
                status, response, room = handler.login_resident(data, system_key)
    
            elif login_type == 'employee':
                status, response, room = handler.login_employee(data, system_key)
    
            else:
                status = 400
                response = {'status': 400, 'result': False, 'event': 'Invalid login type', 'data': {}}
    
            if status == 200:
                key = secrets.token_urlsafe(20)
    
                keys.append(key)
                response['key'] = key
                session['KEY'] = key
                session['login'] = login_type
                session['room'] = room
                session['datetime'] = datetime.datetime.now()
                
        except json.JSONDecodeError:
            status = 422
            response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return jsonify(response), status


@app.route('/register/<registration_type>')
def register(registration_type):
    if session.get('KEY') is not None:
        status = 409
        response = {'status': 409, 'result': False, 'event': 'User already logged', 'data': {}}

    else:
        try:
            data = request.get_json(force=True)
            if str(registration_type).lower() == 'resident':
                status, response, room = handler.register_resident(data, system_key)

            elif str(registration_type).lower() == 'employee':
                status, response, room = handler.register_employee(data, system_key)

            else:
                status = 400
                response = {'status': 400, 'result': False, 'event': 'Invalid registration type', 'data': {}}

            if status == 201:
                key = secrets.token_urlsafe(20)

                keys.append(key)
                response['key'] = key
                session['KEY'] = key
                session['login'] = registration_type
                session['room'] = room
                session['datetime'] = datetime.datetime.now()

        except json.JSONDecodeError:
            status = 422
            response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return jsonify(response), status


@app.route('/employee', methods=['GET'])
@session_decorator
def employee():
    try:
        data = request.get_json(force=True)
        status, response = handler.get_employees(data, system_key, session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return response, status


@app.route('/condominium', methods=['GET'])
@session_decorator
def condominium():
    data = request.get_json(force=True)
    response = handler.get_condominium(data)

    return response, 200


@app.route('/tower', methods=['GET'])
@session_decorator
def tower():
    data = request.get_json(force=True)
    response = handler.get_towers(data)

    return response, 200


@app.route('/apartment', methods=['GET'])
@session_decorator
def apartment():
    data = request.get_json(force=True)
    response = handler.get_apartments(data)

    return response, 200


@app.route('/event', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def event():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response, room = handler.get_events(data)

    elif request.method == 'POST':
        response, room = handler.register_event(data)
        emit('event', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('event', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response, room = handler.remove_event(data)
        emit('event', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('event', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/notification', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def notification():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_notifications(data)

    elif request.method == 'POST':
        response = handler.register_notification(data)
        emit('notification', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('notification', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = handler.remove_notification(data)
        emit('notification', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('notification', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/guest', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def guest():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_guests(data)

    elif request.method == 'POST':
        response = handler.register_guest(data)
        emit('guest', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = handler.remove_guest(data)
        emit('guest', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/service', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def service():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_services(data)

    elif request.method == 'POST':
        response = handler.register_service(data)
        emit('service', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = handler.remove_service(data)
        emit('service', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


@app.route('/rule', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def rule():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_rules(data)

    elif request.method == 'POST':
        response = handler.register_rule(data)
        emit('rule', {'type': 'registration', 'data': data}, room=session['room'] + '_resident')
        emit('rule', {'type': 'registration', 'data': data}, room=session['room'] + '_employee')

    else:
        response = handler.remove_rule(data)
        emit('rule', {'type': 'deletion', 'data': data}, room=session['room'] + '_resident')
        emit('rule', {'type': 'deletion', 'data': data}, room=session['room'] + '_employee')

    return response, 204


if __name__ == '__main__':
    from helpers.handler import Handler

    handler = Handler(system_key)

    # import database_cleaner
    # handler.permission_manager.add_session('sistema', 1)
    #
    # print('\nINSERTIONS\n')
    # print(handler.permission_manager.address_controller.register_address_by_names('rua', 'bairro', 'cidade', 'estado', 'pais'))
    # print(handler.permission_manager.condominium_controller.register_condominium('condominio', 23, None, 1))
    # print(handler.permission_manager.condominium_controller.register_tower('t1', 1))
    # print(handler.permission_manager.condominium_controller.register_apartment(100, 1))
    #
    # print(handler.permission_manager.register_resident('username', 'password', 'cpf', 'name', '1999-06-11', None, 1, system_key))
    # print(handler.permission_manager.register_employee('username', 'password', 'cpf', 'name', '1999-06-11', None, 'role', 1, system_key))

    socket.run(app)
