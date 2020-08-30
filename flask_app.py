from flask import Flask, request, json
from flask_sqlalchemy import SQLAlchemy

from bot_api.connection import confirmation_token
from bot_api.vk_bot_response import *
from main import db, app


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db_utils'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)


@app.route('/', methods=['POST'])
def processing():
    # Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        text = str(data['object']['message']['text'])
        peer_id = str(data['object']['message']['peer_id'])
        bot_response(peer_id=peer_id, user_request=text)
        return 'ok'


@app.route('/admin')
def hello_world():
    return 'Hello admin!'


# if __name__ == '__main__':
#     app.run(debug=False)
