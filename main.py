from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters
import telegram
import random
import subprocess
import logging
import wikipediaapi
import json

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)

photos = {
        "metacircular": 'AgADBQADV6gxGyA9KVdv8KmmmPgtsjRW2zIABBah2Y1WNNV7JzkBAAEC',
        }

simple_replies_filename = 'simple_replies.json'
simple_replies = json.load(open(simple_replies_filename, 'r'))
def save_simple_replies():
    json_replies = json.dumps(simple_replies, indent='\t', sort_keys=True, ensure_ascii=False)
    with open(simple_replies_filename, 'w') as f:
        f.write(json_replies)
        f.write('\n')

save_simple_replies()

wikiwiki = wikipediaapi.Wikipedia('en')

def randomcmd(bot, update):
    update.message.reply_text('{0:.3f}'.format(random.random()))

def hoogle(bot, update):
    update.message.reply_text("Hoogle doesn't work on this server... :(")
    # query = update.message.text[len('/hoogle'):]
    # result = subprocess.check_output(['hoogle', '--', query]).decode('utf-8')
    # update.message.reply_text(result)

def mancmd(bot, update):
    query = update.message.text.split()[1]
    result = subprocess.run(['man', '--', query], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.decode('utf-8').splitlines()
    if len(result) == 1:
        update.message.reply_text(result[0])
    else:
        name = -1
        description = -1
        reply = ""
        for i, l in enumerate(result):
            if l == 'NAME':
                name = i
            elif l == 'DESCRIPTION':
                description = i
        if name >= 0:
            reply += 'NAME: '
            reply += result[name+1].strip()
            reply += '\n'
        if description >= 0:
            reply += 'DESCRIPTION: '
            reply += result[description+1].strip()
            reply += '\n'
        if reply == "":
            reply += "Man page exists but someone fucked up when writing the manpage so... sorry :("
        update.message.reply_text(reply)

def mce(bot, update):
    update.message.reply_photo(photos["metacircular"])

def shutupandleave(bot, update):
    bot.leave_chat(update.message.chat_id)

def photocmd(bot, update):
    print(update)

def addcmd(bot, update):
    if update.message.from_user.id == 414604698:
        _, cmdname, reply = update.message.text.split(maxsplit=2)
        simple_replies[cmdname] = reply
        save_simple_replies()
    else:
        print(update)

def rmcmd(bot, update):
    if update.message.from_user.id == 414604698:
        _, cmdname, *_ = update.message.text.split(maxsplit=2)
        del simple_replies[cmdname]
        save_simple_replies()
    else:
        print(update)

def evaluatescheme(bot, update):
    _, code = update.message.text.split(maxsplit=1)
    # code = sexpr.parse(code)
    print(code)

def wiki(bot, update):
    _, query = update.message.text.split(maxsplit=1)
    page = wikiwiki.page(query)
    update.message.reply_text(f'''{page.fullurl}''')

def wikipedia(bot, update):
    _, query = update.message.text.split(maxsplit=1)
    page = wikiwiki.page(query)
    update.message.reply_text(f'''{page.summary}

{page.fullurl}''')

def simple(bot, update):
    if update.message.entities[0].type == telegram.MessageEntity.BOT_COMMAND:
        command = update.message.parse_entity(update.message.entities[0]).split('@', maxsplit=1)[0][1:]
        if command in simple_replies:
            update.message.reply_markdown(simple_replies[command])

def main():
    updater = Updater('723571546:AAEPw61TLAhXYbVuOQgfsUScGrxFLNa2s0I')
    updater.dispatcher.add_handler(CommandHandler('random', randomcmd))
    updater.dispatcher.add_handler(CommandHandler('hoogle', hoogle))
    updater.dispatcher.add_handler(CommandHandler('man', mancmd))
    updater.dispatcher.add_handler(CommandHandler('mce', mce))
    updater.dispatcher.add_handler(CommandHandler('addcmd', addcmd))
    updater.dispatcher.add_handler(CommandHandler('rmcmd', rmcmd))
    updater.dispatcher.add_handler(CommandHandler('shutupandleave', shutupandleave))
    # updater.dispatcher.add_handler(CommandHandler('eval', evaluatescheme))
    updater.dispatcher.add_handler(CommandHandler('wiki', wiki))
    updater.dispatcher.add_handler(CommandHandler('wikipedia', wikipedia))

    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photocmd))

    updater.dispatcher.add_handler(MessageHandler(Filters.command, simple))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
