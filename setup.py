from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from flask_cors import CORS
# from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
# from flask_socketio import SocketIO, join_room, disconnect, ConnectionRefusedError
from flask import Flask, request, session, jsonify, abort, make_response
from functools import wraps
import datetime
import time
import secrets
import json
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# Session(app)
CORS(app)
# limiter = Limiter(app, key_func=get_remote_address, default_limits=['1000/day', '400/hour', '30/minute', '2/second'])

db = SQLAlchemy(app)
# socket = SocketIO(app)

keys = set()
blocked_sessions = set()

super_user_url = app.config['SUPER_USER_URL']
print('\n', '===', super_user_url, '===', '\n')

handler = None


def set_handler():
    global handler

    if handler is None:
        from helpers.handler import Handler

        handler = Handler()


def session_decorator(function):
    @wraps(function)
    def session_checker(*args, **kwargs):
        session_key = session.get('KEY')

        if not session_key:
            return {'status': 401, 'result': False, 'event': 'User is not logged or session expired', 'data': {}}, 401

        if session_key not in keys:
            blocked_sessions.add(session['KEY'])
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


def first_login_decorator(function):
    @wraps(function)
    def first_login_checker(*args, **kwargs):
        first_login = session.get('NEW')
        if first_login:
            return {'status': 403, 'result': False, 'event': 'User is not registered', 'data': {}}, 403

        return function(*kwargs.values())

    return first_login_checker


# @socket.on('connect')
# def verify_connection():
#     session_key = session.get('KEY')
#
#     if not session_key:
#         raise ConnectionRefusedError('User not logged')
#
#     key = request.get_json(force=True)['key']
#     if key != session_key:
#         blocked_sessions.add(session_key)
#         raise ConnectionRefusedError('User altered the key. Session is being blocked')
#
#     elif key not in keys:
#         raise ConnectionRefusedError('Key not registered')
#
#     if not all([dict_key in session for dict_key in ['ID', 'ROOM', 'DATETIME', 'NEW', 'TYPE']]):
#         blocked_sessions.add(session_key)
#         raise ConnectionRefusedError('User altered the session. Session is being blocked')
#
#     if session['TYPE'] != 'resident' and session['TYPE'] != 'employee':
#         blocked_sessions.add(session_key)
#         raise ConnectionRefusedError('User altered the session. Session is being blocked')
#
#     join_room(session['ROOM'] + '_' + session['TYPE'], request.sid)


@app.before_request
def session_configuration():
    if 'KEY' in session and session['KEY'] in blocked_sessions:
        abort(make_response(jsonify({'status': 401, 'result': False, 'event': 'User blocked due to attempt to fake data'}), 401))

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
            del session['NEW']
            del session['TYPE']

            # disconnect()


@app.route(f'/login/{super_user_url}', methods=['POST'])
def login_super_user():
    set_handler()

    before = time.time()

    try:
        data = request.get_json(force=True)

        status, response, id_, db_time = handler.login_super_user(data)

        if session.get('KEY') is not None and status == 200:
            status = 206
            response = {'status': 206, 'result': False, 'event': 'Key recovered', 'data': {}, 'key': session['KEY']}

        elif session.get('KEY') is not None:
            status = 409
            response = {'status': 409, 'result': False, 'event': 'User already logged', 'data': {}, 'key': session['KEY']}

            return status, response

        elif status == 200:
            key = secrets.token_urlsafe(20)

            keys.add(key)
            response['key'] = key

            session['KEY'] = key
            session['ID'] = id_
            session['ROOM'] = 'system'
            session['DATETIME'] = datetime.datetime.now()
            session['NEW'] = False
            session['TYPE'] = 'employee'

            handler.register_key('super_user', key)

        response['db_time'] = db_time

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return jsonify(response), status


@app.route(f'/condominium/{super_user_url}', methods=['POST'])
@session_decorator
def register_condominium_super_user():
    before = time.time()

    try:
        condominium_schema = request.get_json(force=True)['schema']
        status, response = handler.build_condominium_schema(condominium_schema, session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return jsonify(response), status


@app.route('/login/<login_type>', methods=['POST'])
def login(login_type):
    before = time.time()

    login_type = str(login_type).lower()

    try:
        data = request.get_json(force=True)
        if login_type == 'resident':
            status, response, room, id_ = handler.login_resident(data)

            if session.get('KEY') is not None and status == 200:
                status = 206
                response = {'status': 206, 'result': False, 'event': 'Key recovered', 'data': {}, 'key': session['KEY']}

            elif session.get('KEY') is not None:
                status = 409
                response = {'status': 409, 'result': False, 'event': 'User already logged logging out', 'data': {}}

            elif status == 200 or (status == 404 and login_type == 'resident'):

                key = secrets.token_urlsafe(20)

                keys.add(key)
                response['key'] = key

                session['KEY'] = key
                session['ID'] = id_
                session['ROOM'] = room
                session['DATETIME'] = datetime.datetime.now()
                session['TYPE'] = login_type
                if status == 404:
                    session['NEW'] = True
                else:
                    session['NEW'] = False

                handler.register_key(login_type, key)

        elif login_type == 'employee':
            status, response, room, id_, login_type = handler.login_employee(data)

            if session.get('KEY') is not None and status == 200:
                status = 206
                response = {'status': 206, 'result': False, 'event': 'Key recovered', 'data': {}, 'key': session['KEY']}

            elif session.get('KEY') is not None:
                status = 409
                response = {'status': 409, 'result': False, 'event': 'User already logged, logging out', 'data': {}}

            elif status == 200:
                key = secrets.token_urlsafe(20)

                keys.add(key)
                response['key'] = key

                session['KEY'] = key
                session['ID'] = id_
                session['ROOM'] = room
                session['DATETIME'] = datetime.datetime.now()
                session['TYPE'] = login_type
                session['NEW'] = False

                handler.register_key(login_type, key)

        else:
            status = 404
            response = {'status': 404, 'result': False, 'event': 'Unknown login type', 'data': {}}

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return jsonify(response), status


@app.route('/register/<registration_type>', methods=['POST'])
@session_decorator
def register(registration_type):
    before = time.time()

    registration_type = str(registration_type).lower()
    try:
        data = request.get_json(force=True)
        if registration_type == 'user':
            status, response = handler.register_resident_user(data, session['ID'], session['KEY'])

        elif registration_type == 'resident':
            status, response = handler.register_resident(data, session['ID'], session['KEY'])

            if status == 201:
                session['NEW'] = False

        elif registration_type == 'employee':
            status, response = handler.register_employee(data, session['ID'], session['KEY'])

        else:
            status = 400
            response = {'status': 400, 'result': False, 'event': 'Invalid registration type', 'data': {}}

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return jsonify(response), status


@app.route('/employees', methods=['GET'])
@session_decorator
@first_login_decorator
def employees():
    before = time.time()

    try:
        status, response = handler.get_employees(session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return response, status


@app.route('/residents', methods=['GET'])
@session_decorator
@first_login_decorator
def residents():
    before = time.time()

    try:
        data = request.get_json(force=True)
        status, response = handler.get_residents(data, session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return response, status


@app.route('/notification/', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def notification():
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        status, response = handler.get_notifications(session['ID'], session['KEY'])

        if status == 190:
            status = 400
            blocked_sessions.add(session['KEY'])

    elif request.method == 'POST':
        status, response = handler.register_notification(data, session['ID'], session['KEY'])

        # if status == 201:
        #     socket.emit('notification', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
        #     socket.emit('notification', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        status, response = handler.remove_notification(data)

        # if status == 201:
        #     socket.emit('notification', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
        #     socket.emit('notification', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    after = time.time()
    response['time'] = after - before

    return response, status


@app.route('/guest', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def guest():
    before = time.time()
    data = request.get_json(force=True)
    if request.method == 'GET':
        status, response = handler.get_guests(data, session['ID'], session['KEY'])

    elif request.method == 'POST':
        status, response = handler.register_guest(data, session['ID'], session['KEY'])
        # socket.emit('guest', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        status, response = handler.remove_guest(data)
        # socket.emit('guest', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    after = time.time()
    response['time'] = after - before

    return response, status


@app.route('/service', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def service():
    before = time.time()

    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_services(session['ID'], session['KEY'])

    elif request.method == 'POST':
        response = handler.register_service(data, session['ID'], session['KEY'])
        # socket.emit('service', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        response = handler.remove_service(data, session['ID'], session['KEY'])
        # socket.emit('service', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    after = time.time()
    response['time'] = after - before

    return response, 204


@app.route('/rule', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def rule():
    before = time.time()
    data = request.get_json(force=True)
    if request.method == 'GET':
        response = handler.get_rules(data)

    elif request.method == 'POST':
        response = handler.register_rule(data)
        # socket.emit('rule', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
        # socket.emit('rule', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

    else:
        response = handler.remove_rule(data)
        # socket.emit('rule', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
        # socket.emit('rule', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    after = time.time()
    response['time'] = after - before

    return response, 204


@app.route('/event_type', methods=['GET'])
@session_decorator
@first_login_decorator
def event_type():
    before = time.time()

    try:
        status, response = handler.get_event_types(session['ID'], session['KEY'])

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return response, status


@app.route('/event', methods=['GET', 'POST', 'DELETE'])
@session_decorator
@first_login_decorator
def event():
    before = time.time()

    try:
        data = request.get_json(force=True)
        if request.method == 'GET':
            status, response = handler.get_events(data, session['ID'], session['KEY'])

        elif request.method == 'POST':
            status, response = handler.register_event(data, session['ID'], session['KEY'])
            # socket.emit('event', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_resident')
            # socket.emit('event', {'type': 'registration', 'data': data}, room=session['ROOM'] + '_employee')

        else:
            status, response = handler.remove_event(data, session['ID'], session['KEY'])
            # socket.emit('event', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_resident')
            # socket.emit('event', {'type': 'deletion', 'data': data}, room=session['ROOM'] + '_employee')

    except json.JSONDecodeError:
        status = 422
        response = {'status': 422, 'result': False, 'event': 'Unable to process the data, not JSON formatted', 'data': {}}

    after = time.time()
    response['time'] = after - before

    return response, status


@app.errorhandler(429)
def handle_too_many_requests(e):
    return jsonify({'status': 429, 'result': False, 'event': f'Too many requests made: {e.description}', 'data': {}})


if __name__ == '__main__':
    # Clear previous run data
    # import database_cleaner
    # redis_db.flushall()
    app.run()
    # socket.run(app)
