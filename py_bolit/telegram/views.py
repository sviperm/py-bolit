import json

import requests
from django.http import JsonResponse
from django.views import View

from py_bolit.settings.telegram import BOT_TOKEN, BOT_WEBHOOK

from . import templates
from .bot import TelegramBot
from .bot.keyboards import get_node_keyboard, get_reply_keyboard
from .models import Chat, Node

bot = TelegramBot(BOT_TOKEN)
bot.delete_webhook()
bot.init_webhook(BOT_WEBHOOK)

MDSS_API = "http://0.0.0.0:8000/api"
DEFAULT_RESPONSE = JsonResponse({"ok": "POST request processed"})


class BotView(View):

    def post(self, request, *args, **kwargs):
        try:
            chat = Chat()

            @bot.message_handler(request)
            def init_chat(message, *args, **kwargs):
                print('init')
                nonlocal chat
                chat, _ = Chat.objects.get_or_create(id=message['chat']['id'])

            @bot.message_handler(request, commands=['start'])
            def start_command(message):
                print('start')
                Node.objects.filter(chat=chat).delete()
                nodes = json.loads(requests.get(f"{MDSS_API}/get_nodes/").content)
                names = [n['name'] for n in nodes if n['type'] != 'diagnosis']
                chat.set_start_status()
                bot.send_message(chat.id,
                                 templates.start_message,
                                 reply_markup=get_reply_keyboard(names))

            def ask_prediction(chat=chat):
                nodes = (Node.objects
                         .filter(chat=chat)
                         .values_list('code', 'state'))
                data = {key: state for key, state in nodes}
                resp = requests.post(f"{MDSS_API}/predict/", data=data)
                if resp:
                    pred = json.loads(resp.content)
                    return pred
                else:
                    bot.send_message(chat.id, templates.something_wrong)

            def ask_symptom(pred, chat=chat):
                symptoms = [p for p in pred if p['type'] != 'diagnosis']
                if symptoms:
                    sym = symptoms[0]
                    sym['states'] = sym['states'].keys()
                    chat.set_result_status()
                    bot.send_message(chat.id,
                                     sym['name'],
                                     reply_markup=get_node_keyboard(sym))
                else:
                    bot.send_message(chat.id,
                                     templates.prediction_to_text(pred))

            @bot.message_handler(request, commands=['result'])
            def result_command(message):
                print('result')
                pred = ask_prediction()
                if pred:
                    ask_symptom(pred)

            @bot.message_handler(request, commands=['force_result'])
            def force_result_command(message):
                print('force_result')
                pred = ask_prediction()
                if pred:
                    bot.send_message(chat.id,
                                     templates.prediction_to_text(pred))

            @bot.message_handler(request, ignore_commands=True)
            def ask_node(message, *args, **kwargs):
                print('ask_node')
                text = message['text']
                resp = requests.post(f"{MDSS_API}/get_node/",
                                     data={"name": text})
                if resp:
                    resp = json.loads(resp.content)
                    bot.send_message(message['chat']['id'],
                                     resp['name'],
                                     reply_markup=get_node_keyboard(resp))
                else:
                    bot.send_message(message['chat']['id'],
                                     templates.node_not_found)

            @bot.callback_query_handler(request, callback_regexp=r"\w+\$[А-яёЁ]+")
            def save_node(callback_id, user, message, data, *args, **kwargs):
                print('save_node')
                chat = Chat.objects.get(id=message['chat']['id'])
                code, state = data.split('$')
                bot.answer_callback_query(callback_id,
                                          text=f"{message['text']}: {state}")
                node, _ = Node.objects.update_or_create(
                    chat=chat, code=code,
                    defaults={'state': state},
                )
                if chat.is_result_status:
                    pred = ask_prediction(chat)
                    if pred:
                        ask_symptom(pred, chat)
        except Exception as e:
            print(e)
        return DEFAULT_RESPONSE
