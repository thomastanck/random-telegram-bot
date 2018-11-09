from telegram.ext import Updater, CommandHandler
import random
import subprocess
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Meh')

def randomcmd(bot, update):
    update.message.reply_text('{0:.3f}'.format(random.random()))

def thenaesh(bot, update):
    update.message.reply_text('Oh Thenaesh, how are you?')

def stars(bot, update):
    update.message.reply_text('A star is type of astronomical object consisting of a luminous spheroid of plasma held together by its own gravity. The nearest star to Earth is the Sun. Many other stars are visible to the naked eye from Earth during the night, appearing as a multitude of fixed luminous points in the sky due to their immense distance from Earth. Historically, the most prominent stars were grouped into constellations and asterisms, the brightest of which gained proper names. Astronomers have assembled star catalogues that identify the known stars and provide standardized stellar designations. However, most of the stars in the Universe, including all stars outside our galaxy, the Milky Way, are invisible to the naked eye from Earth. Indeed, most are invisible from Earth even through the most powerful telescopes.')

def hoogle(bot, update):
    update.message.reply_text("Hoogle doesn't work on this server... :(")
    # query = update.message.text[len('/hoogle'):]
    # result = subprocess.check_output(['hoogle', '--', query]).decode('utf-8')
    # update.message.reply_text(result)

def opencmd(bot, update):
    update.message.reply_markdown('`int fd = open("/home/cs-ay1819/src/cancer/README.md", RD_ONLY);`')

def closecmd(bot, update):
    update.message.reply_markdown('`close(fd);`')

def reddit(bot, update):
    update.message.reply_text('https://news.ycombinator.com/')

def hackernews(bot, update):
    update.message.reply_text('https://www.reddit.com/')

def bestmodules(bot, update):
    update.message.reply_text('Here are the best modules: psmouse, rfkill, acpi_call, ip_tables')

def helpcmd(bot, update):
    update.message.reply_text('https://doc.rust-lang.org/stable/book/')

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

def main():
    updater = Updater('723571546:AAEPw61TLAhXYbVuOQgfsUScGrxFLNa2s0I')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('random', randomcmd))
    updater.dispatcher.add_handler(CommandHandler('thenaesh', thenaesh))
    updater.dispatcher.add_handler(CommandHandler('stars', stars))
    updater.dispatcher.add_handler(CommandHandler('hoogle', hoogle))
    updater.dispatcher.add_handler(CommandHandler('open', opencmd))
    updater.dispatcher.add_handler(CommandHandler('close', closecmd))
    updater.dispatcher.add_handler(CommandHandler('reddit', reddit))
    updater.dispatcher.add_handler(CommandHandler('hackernews', hackernews))
    updater.dispatcher.add_handler(CommandHandler('help', helpcmd))
    updater.dispatcher.add_handler(CommandHandler('man', mancmd))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
