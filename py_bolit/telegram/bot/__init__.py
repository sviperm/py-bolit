import json
import requests
from re import match
from pprint import pprint


def debug_response(fun):
    def wrapper(*args, **kwargs):
        response = fun(*args, **kwargs)
        pprint(json.loads(response.text))
        return response
    return wrapper


def request_to_dict(request):
    return json.loads(request.body)


def response_to_dict(response):
    return json.loads(response.text).get('result')


def is_command(message):
    entities = message.get('entities')
    if entities:
        return bool([e for e in entities if e['type'] == 'bot_command'])
    return False


class TelegramBot:
    # DEV
    # TODO: move to settings (split dev and prod)
    __URL = "https://vast-refuge-73990.herokuapp.com/https://api.telegram.org/bot"

    def __init__(self, TOKEN):
        self._TOKEN = TOKEN

    @property
    def URL(self):
        return self.__URL

    @property
    def TOKEN(self):
        return self._TOKEN

    def send_message(self, chat_id, text, **kwargs):
        data = {
            "chat_id": chat_id,
            "text": text,
            **kwargs,
        }

        response = requests.post(
            f"{self.URL}{self.TOKEN}/sendMessage",
            data={key: value for key, value in data.items() if value},
        )
        return response

    def answer_callback_query(self, callback_query_id, **kwargs):
        response = requests.post(
            f"{self.URL}{self.TOKEN}/answerCallbackQuery",
            data={
                "callback_query_id": callback_query_id,
                **kwargs
            },
        )
        return response

    def edit_message_text(self,
                          text,
                          chat_id=None,
                          message_id=None,
                          inline_message_id=None,
                          reply_markup=None,
                          **kwargs):
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
            **kwargs,
        }
        response = requests.post(
            f"{self.URL}{self.TOKEN}/editMessageText",
            data={key: value for key, value in data.items() if value},
        )
        return response

    def edit_message_reply_markup(self,
                                  chat_id=None,
                                  message_id=None,
                                  inline_message_id=None,
                                  reply_markup=None):
        data = {
            "chat_id": chat_id,
            "message_id": message_id,
            "inline_message_id": inline_message_id,
            "reply_markup": reply_markup,
        }
        response = requests.post(
            f"{self.URL}{self.TOKEN}/editMessageReplyMarkup",
            data={key: value for key, value in data.items() if value},
        )
        return response

    def delete_webhook(self):
        response = requests.get(f"{self.URL}{self.TOKEN}/deleteWebhook")
        print(json.loads(response.text))

    def init_webhook(self, webhook):
        response = requests.get(f"{self.URL}{self.TOKEN}/setWebhook?url={webhook}")
        print(json.loads(response.text))

    # DECORATORS
    @staticmethod
    def message_handler(request, commands=None, command_regexp=None):
        def wrapper(func):
            message = request_to_dict(request).get('message')
            if message:
                text = message.get('text')
                if (commands or command_regexp) and is_command(message):
                    if commands:
                        cmd = match(r"^\/(\d+|\w+)$", text)
                        if cmd:
                            cmds = [cmd.group(0), cmd.group(1)]
                            is_intersacted = bool([x for x in cmds if x in commands])
                            if is_intersacted:
                                return func(message)
                    elif command_regexp and match(command_regexp, text):
                        return func(message)
                else:
                    return func(message)
        return wrapper

    @staticmethod
    def poll_answer_handler(request):
        def wrapper(func):
            poll_answer = request_to_dict(request).get('poll_answer')
            if poll_answer:
                func(poll_answer)
        return wrapper

    def callback_query_handler(self,
                               request,
                               callbacks=None,
                               callback_regexp=None,
                               ignore_old=True,
                               remove=False):
        def wrapper(func):
            callback_query = request_to_dict(request).get('callback_query')
            if callback_query:
                id = callback_query.get('id')
                data = callback_query.get('data')
                message = callback_query.get('message')
                user = callback_query.get('from')
                if ignore_old and not message:
                    TelegramBot.answer_callback_query(
                        callback_query_id=id,
                        text="Сообщение слишком старое",
                        show_alert=True
                    )
                elif not (callbacks or callback_regexp):
                    if remove:
                        self.edit_message_reply_markup(
                            chat_id=message['chat']['id'],
                            message_id=message['message_id'],
                            reply_markup=InlineKeyboardMarkup().to_json()
                        )
                    return func(id, user, message)
                elif (callbacks and data in callbacks) or (callback_regexp and match(callback_regexp, data)):
                    if remove:
                        self.edit_message_reply_markup(
                            chat_id=message['chat']['id'],
                            message_id=message['message_id'],
                            reply_markup=InlineKeyboardMarkup().to_json()
                        )
                    return func(id, user, message)
        return wrapper


# OTHER CLASSES

class InlineKeyboardMarkup:
    def __init__(self, inline_keyboard=[], **kwargs):
        self.inline_keyboard = inline_keyboard

    def to_json(self):
        keyboard = []
        for row in self.inline_keyboard:
            keyboard.append([button.get_dict() for button in row])
        return json.dumps({'inline_keyboard': keyboard})


class InlineKeyboardButton:
    def __init__(self,
                 text,
                 url=None,
                 callback_data=None,
                 switch_inline_query=None,
                 switch_inline_query_current_chat=None,
                 callback_game=None,
                 pay=None,
                 login_url=None,
                 **kwargs):
        self.text = text
        self.url = url
        self.login_url = login_url
        self.callback_data = callback_data
        self.switch_inline_query = switch_inline_query
        self.switch_inline_query_current_chat = switch_inline_query_current_chat
        self.callback_game = callback_game
        self.pay = pay

    def get_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}
