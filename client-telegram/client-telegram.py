BOT_KEY = "1958569576:AAHdYq6PiPQ9QnUFJR_qCzbvp3sqQtYAS00"
from telegram.ext import *
import telegram
import requests
import json

#telegram bot logging/debugging
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def bot_responses(text, update, chat_id):
    print('text:', text)
    r = requests.post("http://server:1234/getmask", json=text)
    res = r.json()['result']
    #return res[0]
    resp = ''
    print(res)
    #return res[0]['MASK']
    for d in res:
        print(d['MASK'])
        print(d['weights:'])
        resp = resp + d['MASK'] + ":" + str(round(d['weights:'],2)) + '\n'
    return resp

def start_command(update, context):
  update.message.reply_text('Give me text with a missed word using [MASK], do not forget a punctuation at the end of the sentence. For example, "My [MASK] is so cute."')

def help_command(update, context):
  update.message.reply_text('Give me text with a missed word using [MASK], do not forget a punctuation at the end of the sentence. For example, "My [MASK] is so cute."')


def handle_message(update, context):
  chat_id = update.message.chat_id
  print(update, context)
  print(update.message, context)
  text = str(update.message.text)
  response = bot_responses(text, update, chat_id)
  print(response)
  update.message.reply_text(str(response))

def error(update, context):
  print(f'Update {update} caused error {context.error}')

def main():
  updater = Updater(BOT_KEY, use_context = True)
  dp = updater.dispatcher
  dp.add_handler(CommandHandler('start', start_command))
  dp.add_handler(CommandHandler('help', help_command))
  dp.add_handler(MessageHandler(Filters.text, handle_message))
  dp.add_error_handler(error)
  updater.start_polling()
  logger = logging.getLogger()
  logger.setLevel(logging.INFO)
  updater.idle()

main()
