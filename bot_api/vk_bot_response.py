from itertools import groupby
import time

from bot_api.methods import send_message, create_keyboard
from bot_api.connection import vk_session
from db_utils.select_db import select_menu, get_search, select_inheritances
from db_utils.database import Replace
from main import db


def menus(inher, response=None):
    menu_id_ancestor = inher

    menu_ids_descendant = [inheritances.menu_id_descendant for inheritances in menu_id_ancestor]
    menu_ids_descendant.extend([inheritances.menu_id_ancestor for inheritances in menu_id_ancestor])
    menu_ids = [el for el, _ in groupby(menu_ids_descendant)]
    if response:
        while response[0].id in menu_ids:
            menu_ids.remove(response[0].id)
    return select_menu({'menu_ids': list(menu_ids)})


def bot_response(peer_id, user_request):
    user_request = user_request.replace('[club194566616|@public194566616], ', '')
    response = select_menu({'menu_names': user_request})
    user_status = Replace.query.filter(Replace.name == str(peer_id)).all()
    print(user_request)
    if user_status:
        if user_request != 'Главное меню' and user_request != 'Партнеры':
            if user_status[0].value == 'помощь':
                problem_message = f'От: https://vk.com/id{peer_id}.\n' \
                                  f'Проблема: {user_request}'
                response_message = 'Спасибо, ваша жалоба передана Студенческому совету СПбГУТ. ' \
                                   'Вам ответят в ближайшее время, если этого не произошло, ' \
                                   'напишите Председателю Студенческого совета - @ksilligan'
                send_message(session=vk_session, peer_id=83886028, message=problem_message)
                send_message(session=vk_session, peer_id=peer_id, message=response_message)
            else:
                partner_message = f'От: https://vk.com/id{peer_id}.\n' \
                                  f'Заявка: {user_request}'
                response_message = 'Спасибо, ваша заявка передана в Комитет по внешним связям СПбГУТ. ' \
                                   'Вам ответят в ближайшее время, если этого не произошло, ' \
                                   'напишите - @catherinka_pro'
                send_message(session=vk_session, peer_id=89187609, message=partner_message)
                send_message(session=vk_session, peer_id=83886028, message=partner_message)
                send_message(session=vk_session, peer_id=147736000, message=partner_message)
                send_message(session=vk_session, peer_id=peer_id, message=response_message)

        try:
            db.session.delete(user_status[0])
            db.session.commit()
            bot_response(peer_id=peer_id, user_request='Главное меню')
        except Exception as error:
            send_message(session=vk_session, peer_id=peer_id, message=f'Возникла ошибка в работе бота, '
                                                                      f'перешлите это сообщение @pavel.json,\n'
                                                                      f'Он все починит \n\n{error}')
    else:
        if user_request == 'Помощь':
            inher = select_inheritances({'menu_id': str(response[0].id)})
            if inher:
                all_menus = menus(inher, response)
                name_arr = [menu.name for menu in all_menus]
                keyboard = create_keyboard(name_arr=name_arr, inline=False)
            problem = Replace(name=peer_id, value='помощь')
            send_message(session=vk_session,
                         peer_id=peer_id,
                         message='Опишите в чем заключается проблема, '
                                 'одним сообщением.',
                         user_keyboard=keyboard, )
            try:
                db.session.add(problem)
                db.session.commit()
            except Exception as error:
                send_message(session=vk_session,
                             peer_id=peer_id,
                             message=f'Возникла ошибка в работе бота, '
                                     f'перешлите это сообщение @pavel.json,\n'
                                     f'Он все починит \n\n{error}')
        elif isinstance(response, list) and response:
            keyboard = None
            attachment = None

            message = response[0].text

            if response[0].attachment.all():
                if response[0].attachment[0].vk_active:
                    attachment = response[0].attachment[0].vk_attachment

            inher = select_inheritances({'menu_id': str(response[0].id)})
            if inher:
                all_menus = menus(inher, response)
                name_arr = [menu.name for menu in all_menus]
                if 'Анкета' in name_arr:
                    name_arr.remove('Анкета')
                    if peer_id > 2000000000:
                        print('БЕСЕДА')
                        keyboard = create_keyboard(name_arr=name_arr,
                                                   inline=True,
                                                   link_button={'label': 'Анкета',
                                                                'link': 'https://vk.com/app5619682_-194566616#537797'})
                    else:
                        keyboard = create_keyboard(name_arr=name_arr,
                                                   inline=False,
                                                   link_button={'label': 'Анкета',
                                                                'link': 'https://vk.com/app5619682_-194566616#537797'})

                else:
                    if peer_id > 2000000000:
                        print('БЕСЕДА')
                        keyboard = create_keyboard(name_arr=name_arr, inline=True)
                    else:
                        keyboard = create_keyboard(name_arr=name_arr, inline=False)
            send_message(session=vk_session,
                         peer_id=peer_id,
                         message=message,
                         user_keyboard=keyboard,
                         user_attachment=attachment)
        else:
            response = sorted(get_search({'text': user_request}), key=lambda obj: obj['rating'])
            response.reverse()
            message = response[0]['menu'].text
            send_message(session=vk_session, peer_id=peer_id, message=message)


if __name__ == '__main__':
    tmp = time.time()
    bot_response(peer_id=83886028, user_request='Партнеры')
    print(time.time() - tmp)
    # send_message(session=vk_session,
    #              peer_id=83886028,
    #              message=f'1',
    #              user_keyboard=create_keyboard(link_button={'label': 'тест', 'link': 'https://vk.com/public194566616'}))
