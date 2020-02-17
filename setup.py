import json
import secrets
import datetime
from functools import wraps
from flask import Flask, request, session, jsonify, abort, make_response
from flask_socketio import SocketIO, emit, join_room, disconnect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
# from flask_session import Session


app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(30)
app.config['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/api.db'

app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_THRESHOLD'] = 10000
app.config['SESSION_COOKIE_HTTPONLY'] = False
# app.config['SESSION_COOKIE_SECURE'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=2)

# Session(app)
CORS(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=['1000/day', '400/hour', '30/minute', '2/second'])

db = SQLAlchemy(app)
socket = SocketIO(app)

keys = set()
blocked_sessions = set()

super_user_url = secrets.token_urlsafe(36)


def session_decorator(function):
    @wraps(function)
    def session_checker(*args, **kwargs):
        session_key = session.get('KEY')

        if not session_key:
            return {'status': 401, 'result': False, 'event': 'User is not logged or session expired', 'data': {}}, 401

        if session_key not in keys:
            blocked_sessions.add(session_key)
            abort(make_response(jsonify({'status': 401, 'result': False, 'event': 'User blocked due to attempt to fake identity'}), 401))

        data = request.get_json(force=True)
        if 'key' not in [str(key).lower() for key in data.keys()]:
            return {'status': 400, 'result': False, 'event': 'Missing information', 'data': {}}, 400

        key = data['key']

        if key != session_key:
            return {'status': 403, 'result': False, 'event': 'Invalid key', 'data': {}}, 403

        elif key not in keys:
            return {'status': 401, 'result': False, 'event': 'Key not recognized', 'data': {}}, 401

        else:
            return function(*kwargs.values())

    return session_checker


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
        del session['DATETIME']
        raise ConnectionRefusedError

    if session['login'] != 'resident' and session['login'] != 'employee':
        raise ConnectionRefusedError

    join_room(session['room'] + '_' + session['login'], request.sid)


@app.before_request
def session_configuration():
    if 'KEY' in session and session['KEY'] in blocked_sessions:
        abort(make_response(jsonify({'status': 401, 'result': False, 'event': 'User blocked due to attempt to fake identity'}), 401))

    session.modified = True

    if 'DATETIME' in session:
        datetime_diff = session['DATETIME'] - datetime.datetime.now()
        if datetime_diff.days < 1:
            session['DATETIME'] = datetime.datetime.now()
        else:
            handler.drop_session(session['KEY'])
            keys.remove(session['KEY'])
            del session['KEY']
            del session['ID']
            del session['ROOM']
            del session['DATETIME']

            disconnect()


@app.route(f'/{super_user_url}', methods=['POST'])
def login_super_user():
    if session.get('KEY') is not None:
        status = 409
        response = {'status': 409, 'result': False, 'event': 'User already logged', 'data': {}}

    else:
        try:
            data = request.get_json(force=True)
            status, response, id_ = handler.login_super_user(data)

            if status == 200:
                key = secrets.token_urlsafe(20)

                keys.add(key)
                response['key'] = key

                session['KEY'] = key
                session['ID'] = id_
                session['DATETIME'] = datetime.datetime.now()

                handler.register_key('super_user', key)

        except json.JSONDecodeError:
            status = 422
            response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return jsonify(response), status


@app.route('/login/<login_type>', methods=['POST'])
def login(login_type):
    if session.get('KEY') is not None:
        status = 409
        response = {'status': 409, 'result': False, 'event': 'User already logged', 'data': {}}

    else:
        try:
            data = request.get_json(force=True)
            if login_type == 'resident':
                status, response, room, id_ = handler.login_resident(data)

            elif login_type == 'employee':
                status, response, room, id_, login_type = handler.login_employee(data)
    
            else:
                status = 400
                response = {'status': 400, 'result': False, 'event': 'Invalid login type', 'data': {}}
    
            if status == 200:
                key = secrets.token_urlsafe(20)
    
                keys.add(key)
                response['key'] = key

                session['KEY'] = key
                session['ID'] = id_
                session['ROOM'] = room
                session['DATETIME'] = datetime.datetime.now()

                handler.register_key(login_type, key)
                
        except json.JSONDecodeError:
            status = 422
            response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return jsonify(response), status


@app.route('/register/<registration_type>', methods=['POST'])
@session_decorator
def register(registration_type):
    try:
        data = request.get_json(force=True)
        if str(registration_type).lower() == 'user':
            status, response = handler.register_user(data, session['KEY'])

        elif str(registration_type).lower() == 'resident':
            status, response = handler.register_resident(data, session['ID'], session['KEY'])

        elif str(registration_type).lower() == 'employee':
            status, response = handler.register_employee(data, session['ID'], session['KEY'])

        else:
            status = 400
            response = {'status': 400, 'result': False, 'event': 'Invalid registration type', 'data': {}}

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return jsonify(response), status


@app.route('/employees', methods=['GET'])
@session_decorator
def employees():
    try:
        data = request.get_json(force=True)
        status, response = handler.get_employees(data, session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return response, status


@app.route('/residents', methods=['GET'])
@session_decorator
def residents():
    try:
        data = request.get_json(force=True)
        status, response = handler.get_residents(data, session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return response, status


@app.route('/notification/', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def notification():
    data = request.get_json(force=True)
    if request.method == 'GET':
        status, response = handler.get_notifications(session['ID'], session['KEY'])

        if status == 190:
            status = 400
            blocked_sessions.add(session['KEY'])

    elif request.method == 'POST':
        status, response = handler.register_notification(data, session['ID'], session['KEY'])

        if status == 201:
            socket.emit('notification', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
            socket.emit('notification', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        status, response = handler.remove_notification(data)

        if status == 201:
            socket.emit('notification', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
            socket.emit('notification', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    return response, status


@app.route('/guest', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def guest():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_guests(data)

    elif request.method == 'POST':
        response = handler.register_guest(data)
        emit('guest', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        response = handler.remove_guest(data)
        emit('guest', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    return response, 204


@app.route('/service', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def service():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_services(data)

    elif request.method == 'POST':
        response = handler.register_service(data)
        emit('service', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        response = handler.remove_service(data)
        emit('service', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    return response, 204


@app.route('/rule', methods=['GET', 'POST', 'DELETE'])
@session_decorator
def rule():
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_rules(data)

    elif request.method == 'POST':
        response = handler.register_rule(data)
        emit('rule', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
        emit('rule', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        response = handler.remove_rule(data)
        emit('rule', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
        emit('rule', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    return response, 204


@app.route('/event/<user_type>/<search_type>', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def event(user_type, search_type):
    try:
        data = request.get_json(force=True)
        if request.method == 'GET':
            status, response = handler.get_events(data, user_type, search_type, session['KEY'])

        elif request.method == 'POST':
            status, response = handler.register_event(data)
            socket.emit('event', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
            socket.emit('event', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

        else:
            status, response = handler.remove_event(data)
            socket.emit('event', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
            socket.emit('event', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    return response, status


@app.errorhandler(429)
def handle_too_many_requests(e):
    return jsonify({'status': 429, 'result': False, 'event': f'Too many requests made: {e.description}', 'data': {}})


if __name__ == '__main__':
    from helpers.handler import Handler

    handler = Handler()
    print(super_user_url)

    # import database_cleaner
    # import bcrypt
    # handler.permission_manager.register_key('super_user', 1)
    # handler.permission_manager.register_key('resident', 2)
    #
    # print('\nINSERTIONS\n')
    # print(handler.permission_manager.address_controller.register_address_by_names('rua', 'bairro', 'cidade', 'estado', 'pais'))
    # print(handler.permission_manager.condominium_controller.register_condominium('condominio', 23, None, 1))
    # print(handler.permission_manager.condominium_controller.register_tower('t1', 1))
    # print(handler.permission_manager.condominium_controller.register_apartment(100, 1))
    # print(handler.permission_manager.condominium_controller.register_apartment(200, 1))
    #
    # print(handler.permission_manager.register_employee(2, 'employee', bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()), 'cpf', 'name', '1999-06-11', None, 'role', 1, 1))
    # print(handler.permission_manager.register_resident_user('resident', bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()), 1, 1, 1))
    # print(handler.permission_manager.register_resident('cpf', 'name', '1999-06-11', None, 1, 2))
    # print(handler.permission_manager.notification_controller.register_notification(1, 'Titulo', 'Texto', '1999-06-11', 1, 1))

    socket.run(app)
