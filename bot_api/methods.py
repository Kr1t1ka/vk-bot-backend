import vk_api
import random
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def send_message(session, peer_id, message=None, user_attachment=None, user_keyboard=None, template=None):
    """
    :param template: обьект описывающий шаблон сообщения
    :type session: сессия вк устававлимая через токен
    :type peer_id: id пользователя
    :type message: сообщение для пользователя
    :type user_attachment: вложения для пользователя
    :type user_keyboard: клавиатура для пользователя
    """
    session.method('messages.send', {
        'peer_id': peer_id,
        'message': message,
        'random_id': random.randint(-2147483648, +2147483648),
        "attachment": user_attachment,
        'keyboard': user_keyboard,
        'dont_parse_links': 1,
        'template': template
    })


def create_keyboard(name_arr=None, inline=False, one_time=True, link_button: dict = None):
    """
    (len(name_arr_descendant) <= 10) - должно быть
    :param link_button: добавляет кнопку со ссылкой
    :param one_time: исчезает ли клавиатура после нажатия (по умолчанию исчезает)
    :param inline:  встроеная клавиатура в сообщение (по умолчанию нет)
    :type name_arr: массив названий кнопок потомков
    """
    user_keyboard = VkKeyboard(one_time=one_time, inline=inline)
    count = 0
    if name_arr is not None:
        for name in name_arr:
            if count == 12:
                break
            count += 1
            if name == name_arr[-1] and len(name_arr) != 1:
                if link_button is not None:
                    user_keyboard.add_openlink_button(label=link_button['label'], link=link_button['link'])
                user_keyboard.add_button(name, color=VkKeyboardColor.NEGATIVE)
            else:
                user_keyboard.add_button(name, color=VkKeyboardColor.PRIMARY)
            if (count % 2 == 0) and (name != name_arr[-1]) and (count <= 10):
                user_keyboard.add_line()
    user_keyboard = user_keyboard.get_keyboard()
    return user_keyboard
