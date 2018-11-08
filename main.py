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
    query = update.message.text[len('/hoogle'):]
    result = subprocess.check_output(['hoogle', '--', query]).decode('utf-8')
    update.message.reply_text(result)

def main():
    updater = Updater('723571546:AAEPw61TLAhXYbVuOQgfsUScGrxFLNa2s0I')

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('random', randomcmd))
    updater.dispatcher.add_handler(CommandHandler('thenaesh', thenaesh))
    updater.dispatcher.add_handler(CommandHandler('stars', stars))
    updater.dispatcher.add_handler(CommandHandler('hoogle', hoogle))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
