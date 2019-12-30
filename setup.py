import secrets
import pathlib
from flask import Flask
from flask_socketio import SocketIO
from model.database import db_location, setup_database

setup_database()

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['SECRET_KEY'] = secrets.token_urlsafe(10)
app.config['SQLALCHEMY_DATABASE_URI'] = db_location

socket = SocketIO(app)


@app.route('/login', methods=['POST'])
def login():
    return {'data': {}}, 200


@app.route('/user', methods=['GET'])
def get_user():
    return {'data': {}}, 200


@app.route('/user', methods=['POST'])
def post_user():
    return {'data': {}}, 204


@app.route('/user', methods=['DELETE'])
def delete_user():
    return {'data': {}}, 205


@app.route('/user', methods=['PUT'])
def put_user():
    return {'data': {}}, 204


@app.route('/event', methods=['GET'])
def get_events():
    return {'data': {}}, 200


@app.route('/event', methods=['POST'])
def post_event():
    return {'data': {}}, 204


@app.route('/event', methods=['DELETE'])
def delete_event():
    return {'data': {}}, 205


@app.route('/warning', methods=['GET'])
def get_warnings():
    return {'data': {}}, 200


@app.route('/warning', methods=['POST'])
def post_warning():
    return {'data': {}}, 204


@app.route('/warning', methods=['DELETE'])
def delete_warning():
    return {'data': {}}, 205


@app.route('/<shop>/items', methods=['GET'])
def get_items(shop):
    return {'data': {}}, 200


@app.route('/<shop>/items', methods=['POST'])
def post_item(shop):
    return {'data': {}}, 204


@app.route('/<shop>/items', methods=['DELETE'])
def delete_item(shop):
    return {'data': {}}, 205


if __name__ == '__main__':
    socket.run(app)
