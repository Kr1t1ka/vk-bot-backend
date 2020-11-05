from bot_api.methods import send_message, create_keyboard
from bot_api.connection import vk_session
from db_utils.select_db import select_menu, get_search, select_inheritances
import time


def menus(inher, response=None):
    menu_id_ancestor = inher

    menu_ids_descendant = [inheritances.menu_id_descendant for inheritances in menu_id_ancestor]
    menu_ids_descendant.extend([inheritances.menu_id_ancestor for inheritances in menu_id_ancestor])
    menu_ids = set(menu_ids_descendant)

    if response:
        if response[0].id in menu_ids:
            menu_ids.remove(response[0].id)
    return select_menu({'menu_ids': list(menu_ids)})


def bot_response(peer_id, user_request):
    response = select_menu({'menu_names': user_request})
    if isinstance(response, list) and response:
        keyboard = None
        attachment = None

        message = response[0].name + '\n' + response[0].text

        if response[0].attachment.all():
            if response[0].attachment[0].vk_active:
                attachment = response[0].attachment[0].vk_attachment

        inher = select_inheritances({'menu_id': str(response[0].id)})
        if inher:
            all_menus = menus(inher, response)
            name_arr = [menu.name for menu in all_menus]
            keyboard = create_keyboard(name_arr=name_arr, inline=False)

        send_message(session=vk_session,
                     peer_id=peer_id,
                     message=message,
                     user_keyboard=keyboard,
                     user_attachment=attachment)

    else:
        response = sorted(get_search({'text': user_request}), key=lambda obj: obj['rating'])
        response.reverse()
        message = response[0]['menu'].name + '\n' + response[0]['menu'].text
        send_message(session=vk_session, peer_id=peer_id, message=message)


if __name__ == '__main__':
    tmp = time.time()
    bot_response(peer_id=83886028, user_request='иксс')
    print(time.time() - tmp)
