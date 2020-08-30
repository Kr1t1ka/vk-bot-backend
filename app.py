from flask import Flask, render_template, request, redirect, json

from bot_api.connection import confirmation_token
from bot_api.vk_bot_response import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


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

        bot_response(peer_id=peer_id, user_reques=text)

        return 'ok'


@app.route('/test')
def hello_world():
    # args = {'text': 'медпункт'}
    # # tmp = get_search(args)
    return 'tmp'


if __name__ == '__main__':
    app.run(debug=False)
