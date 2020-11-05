from flask import Flask, request, json, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from bot_api.connection import confirmation_token
from bot_api.vk_bot_response import *
from main import db, app
from db_utils.database import Menu, Attachment, Inheritances
from db_utils.select_db import select_inheritances


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


@app.route('/')
def hello_world():
    return render_template('index.html')


# TODO: возможно возникнет проблеиа подключение бота, надо сделать отдельный url адрес для него


@app.route('/all_events')
def all_events():
    events = Menu.query.order_by(Menu.id).all()
    return render_template('all_events.html', events=events)


@app.route('/event/<int:id>')
def event(id):
    event = Menu.query.get(id)
    inher_event = menus(select_inheritances({'menu_id': event.id}), response=[event])
    return render_template('event_details.html', event=event, inher_event=inher_event)


@app.route('/event/<int:id>/inher', methods=['POST', 'GET'])
def event_inher(id):
    event = Menu.query.get(id)
    events_inherinase = select_inheritances({'menu_id': event.id})
    inher_event = [[menus([el], [event])[0], el] for el in events_inherinase]
    if request.method == 'POST':
        if request.form['index'] == '2':
            inher = request.form['name']
            new_inher = Inheritances(menu_id_ancestor=inher, menu_id_descendant=event.id)
            try:
                db.session.add(new_inher)
                db.session.commit()
                return redirect('/event/'+str(event.id)+'/inher')
            except Exception as error:
                return f'При добавлении статьи произошла ошибка: {str(error)}'
        else:
            return redirect('/del_inher/' + str(request.form['index']))
    return render_template('event_inher.html', event=event, inher_event=inher_event)


@app.route('/del_inher/<int:id>')
def del_inher(id):
    inher = Inheritances.query.filter(Inheritances.id_inher == id).all()
    redir = inher[0].menu_id_descendant
    try:
        db.session.delete(inher[0])
        db.session.commit()
        print('pop')
        return redirect('/event/'+str(redir)+'/inher')
    except Exception as error:
        return f'При добавлении статьи произошла ошибка: {str(error)}'


@app.route('/event/<int:id>/del')
def del_event(id):
    event = Menu.query.get_or_404(id)

    try:
        db.session.delete(event)
        db.session.commit()
        return redirect('/all_events')
    except Exception as error:
        return f'При добавлении статьи произошла ошибка: {str(error)}'


@app.route('/event/<int:id>/update', methods=['POST', 'GET'])
def update_event(id):
    event = Menu.query.get_or_404(id)
    if request.method == 'POST':
        event.name = request.form['name']
        event.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/all_events')
        except Exception as error:
            return f'При редактировании статьи произошла ошибка: {str(error)}'
    else:
        return render_template('update_events.html', event=event)


@app.route('/create_events', methods=['POST', 'GET'])
def create_events():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']

        event = Menu(name=name, text=text)
        try:
            db.session.add(event)
            db.session.commit()
            return redirect('/')
        except Exception as error:
            return f'При добавлении статьи произошла ошибка: {str(error)}'

    else:
        return render_template('create_events.html')


@app.route('/create_type_of_event')
def create_type_of_event():
    return render_template('create_type_of_event.html')


if __name__ == '__main__':
    app.run(debug=False)
