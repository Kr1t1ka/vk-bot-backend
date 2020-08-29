from app.vk_api.methods import send_message, create_keyboard
from app.connection import vk_session
from app.library_api.methods import *
import time


def bot_response(peer_id, user_request):
    response = get_menu(menu_names=user_request)

    if isinstance(response, list) and response:
        keyboard = None
        attachment = None

        message = response[0]['name'] + '\n' + response[0]['text']

        if response[0]['attachment']:
            if response[0]['attachment'][0]['vk_active']:
                attachment = response[0]['attachment'][0]['vk_attachment']

        if response[0]['inheritances']:
            menu_id_ancestor = response[0]['inheritances']

            menu_ids_descendant = [inheritances['menu_id_descendant'] for inheritances in menu_id_ancestor]
            menu_ids_descendant.extend([inheritances['menu_id_ancestor'] for inheritances in menu_id_ancestor])
            menu_ids = set(menu_ids_descendant)

            if response[0]['id'] in menu_ids:
                menu_ids.remove(response[0]['id'])

            menus = get_menu(menu_ids=list(menu_ids))
            name_arr = [menu['name'] for menu in menus]
            keyboard = create_keyboard(name_arr=name_arr, inline=False)

        send_message(session=vk_session,
                     peer_id=peer_id,
                     message=message,
                     user_keyboard=keyboard,
                     user_attachment=attachment)

    else:
        response = sorted(get_search(text=user_request), key=lambda obj: obj['rating'])
        response.reverse()
        message = response[0]['menu']['name'] + '\n' + response[0]['menu']['text']
        send_message(session=vk_session, peer_id=peer_id, message=message)


if __name__ == '__main__':
    tmp = time.time()
    bot_response(peer_id=83886028, user_request='Где')
    print(time.time() - tmp)
